#!/usr/bin/env python3
"""Inventory source leads without executing or importing upstream test code."""

import argparse
from collections import defaultdict, deque
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = {'providerValidCodeParse', 'providerInvalidCodeParse'}
TOKEN = re.compile(r"\s+|//[^\n]*|/\*[\s\S]*?\*/|'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|[A-Za-z_$][\w$]*|=>|.", re.S)
HEREDOC = re.compile(r'''<<<[ \t]*(?:'([A-Za-z_]\w*)'|"([A-Za-z_]\w*)"|([A-Za-z_]\w*))[ \t]*\r?\n''')


def digest(value):
    return hashlib.sha256(value).hexdigest()


def tokens(source):
    """Keep quoted PHP programs opaque, including heredoc/nowdoc bodies."""
    result, position, line = [], 0, 1
    while position < len(source):
        heredoc = HEREDOC.match(source, position)
        if heredoc:
            label = next(group for group in heredoc.groups() if group)
            end = re.search(r'^[ \t]*' + re.escape(label) + r'\b', source[heredoc.end():], re.M)
            if not end:
                raise ValueError('unterminated heredoc in source inventory')
            stop = heredoc.end() + end.end()
            value = source[position:stop]
        else:
            match = TOKEN.match(source, position)
            value, stop = match.group(), match.end()
        if not value.isspace() and not value.startswith(('//', '/*')):
            result.append((value, position, line))
        line += value.count('\n')
        position = stop
    return result


def psalm_datasets(source):
    """Extract provider dataset names, never inner PHP array keys."""
    items = tokens(source)
    found = []
    index = 0
    while index + 2 < len(items):
        if items[index][0] != 'function' or items[index + 1][0] not in PROVIDERS:
            index += 1
            continue
        provider = items[index + 1][0]
        while index < len(items) and items[index][0] not in ('{', ';'):
            index += 1
        if index == len(items) or items[index][0] == ';':
            continue
        braces, arrays = 1, 0
        index += 1
        while braces and index + 2 < len(items):
            value, offset, line = items[index]
            previous = items[index - 1][0]
            if (value.startswith(("'", '"')) and items[index + 1][0] == '=>'
                    and items[index + 2][0] == '['
                    and ((arrays == 0 and previous == 'yield') or arrays == 1)):
                depth, stop = 1, index + 3
                while depth and stop < len(items):
                    depth += (items[stop][0] == '[') - (items[stop][0] == ']')
                    stop += 1
                program = next((token[0] for token in items[index + 3:stop]
                                if token[0].lstrip("'\"").startswith('<?php') or token[0].startswith('<<<')), None)
                if program:
                    found.append({'title': value[1:-1], 'provider': provider, 'line': line,
                                  'probe_sha256': digest(program.encode())})
            braces += (value == '{') - (value == '}')
            arrays += (value == '[') - (value == ']')
            index += 1
    return found


def domain_for(title):
    name = title.lower()
    groups = {
        'enums': ('enum',), 'nullability': ('null', 'nullable'),
        'callables': ('callable', 'closure', 'callback'),
        'generics': ('template', 'generic', 'covariant', 'contravariant'),
        'exceptions': ('exception', 'throw', 'catch', 'finally'),
        'dead-code': ('unreachable', 'redundant', 'unused', 'deadcode'),
        'phpstan-extensions': ('phpstan', 'asserttype', 'typealias'),
        'phpdoc-extensions': ('psalm', 'annotation', 'phpdoc'),
        'arrays': ('array', 'list', 'shape', 'offset', 'foreach', 'destructur'),
        'narrowing': ('instanceof', 'reconcil', 'narrow', 'assert', 'is-int', 'is-string'),
        'legacy-patterns': ('magic', 'loose', 'empty', 'isset', 'dynamic', 'legacy'),
        'assignability': ('assign', 'return', 'coerc', 'signature', 'typehint', 'argument'),
        'objects': ('object', 'class', 'method', 'property', 'trait', 'inherit', 'readonly'),
    }
    return next((domain for domain, words in groups.items() if any(word in name for word in words)), 'type-inference')


def revision(root):
    ref = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if subprocess.run(['git', '-C', str(root), 'diff', '--quiet', 'HEAD', '--', 'tests'], check=False).returncode:
        raise ValueError(f'{root}/tests contains tracked changes; immutable citations would be misleading')
    return ref


def candidate(family, root, path, ref, repo, title=None, **extra):
    relative = path.relative_to(root).as_posix()
    raw = path.read_bytes()
    title = title or (path.parent.name if path.stem == 'repro' else path.stem)
    identity = '\0'.join((relative, extra.get('provider', ''), title))
    return {'id': family + ':' + digest(identity.encode())[:20], 'family': family,
            'domain': domain_for(title + ' ' + relative.replace('tests/PHPStan/', '')), 'title': title, 'path': relative,
            'line': 1, 'source_ref': ref or digest(raw), 'source_sha256': digest(raw),
            'probe_sha256': digest(raw), 'local_path': str(path),
            'citation': f'https://github.com/{repo}/blob/{ref}/{relative}#L{extra.get("line", 1)}' if repo else None,
            'status': 'candidate', **extra}


def select(entries, limit):
    buckets, seen = defaultdict(deque), set()
    for entry in sorted(entries, key=lambda item: (bool(re.search(r'\d{4}', item['title'])), item['path'], item['title'])):
        if entry['probe_sha256'] not in seen:
            seen.add(entry['probe_sha256'])
            buckets[entry['domain']].append(entry)
    selected = []
    while len(selected) < limit and any(buckets.values()):
        for domain in sorted(buckets):
            if buckets[domain] and len(selected) < limit:
                selected.append(buckets[domain].popleft())
    return sorted(selected, key=lambda item: item['id'])


def build(psalm, phpstan, repro, limit=40):
    roots = {name: Path(path).resolve() for name, path in
             [('psalm', psalm), ('phpstan', phpstan), ('mago', repro)]}
    if limit < 1:
        raise ValueError('limit must be positive')
    for name, path in roots.items():
        if not path.is_dir():
            raise ValueError(f'missing {name} source: {path}')
    refs = {name: revision(roots[name]) for name in ('psalm', 'phpstan')}
    repos = {'psalm': 'vimeo/psalm', 'phpstan': 'phpstan/phpstan-src'}
    entries = {name: [] for name in roots}
    ledger = roots['mago'].parent / 'COORDINATION.json'
    history = ({task['slug']: task for task in json.loads(ledger.read_text()).get('tasks', [])
                if task.get('slug')} if ledger.is_file() else {})
    for path in sorted((roots['psalm'] / 'tests').rglob('*.php')):
        for dataset in psalm_datasets(path.read_text()):
            entries['psalm'].append(candidate('psalm', roots['psalm'], path, refs['psalm'], repos['psalm'], **dataset))
    tests = roots['phpstan'] / 'tests/PHPStan'
    for path in sorted(tests.rglob('*.php')):
        relative = path.relative_to(tests)
        if relative.parts[0:2] == ('Analyser', 'nsrt') or ('Rules' in relative.parts and 'data' in relative.parts):
            entries['phpstan'].append(candidate('phpstan', roots['phpstan'], path, refs['phpstan'], repos['phpstan']))
    for path in sorted(roots['mago'].rglob('*.php')):
        entry = candidate('mago', roots['mago'], path, None, None)
        if task := history.get(path.parent.name):
            entry['historical_context'] = {key: task.get(key) for key in ('id', 'status', 'pr_url')}
        entries['mago'].append(entry)
    for name, items in entries.items():
        if len(select(items, limit)) < limit:
            raise ValueError(f'{name} has fewer than {limit} distinct source leads; refusing a partial catalogue')
    return {'schema_version': 1, 'target_criteria': 120,
            'history_ledger_sha256': digest(ledger.read_bytes()) if ledger.is_file() else None,
            'limitations': ['Candidates are not reviewed criteria. Domain tags are filename/name heuristics.',
                            'Local Mago probes have content identities, not invented upstream citations.',
                            'This inventories named literal Psalm providers and PHPStan fixture files; it does not execute or semantically review either suite.'],
            'sources': [{'family': name, 'root': str(root), 'repo': repos.get(name),
                         'ref': refs.get(name), 'discovered_candidates': len(entries[name])}
                        for name, root in roots.items()],
            'candidates': [entry for name in roots for entry in select(entries[name], limit)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build'])
    parser.add_argument('--psalm', default='/home/abez/projects/psalm-src')
    parser.add_argument('--phpstan', default='/home/abez/projects/phpstan-src')
    parser.add_argument('--repro', default='/home/abez/projects/mago-upstream-prep/repro')
    parser.add_argument('--out', type=Path, default=ROOT / 'factory/catalog.json')
    parser.add_argument('--limit-per-family', type=int, default=40)
    args = parser.parse_args()
    payload = build(args.psalm, args.phpstan, args.repro, args.limit_per_family)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print(f'{len(payload["candidates"])} unreviewed source candidates written to {args.out}')


if __name__ == '__main__':
    main()
