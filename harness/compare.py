#!/usr/bin/env python3
"""Measure immutable Mago versions on one corpus; retain evidence for review."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from bench import case as case_mod, report as report_mod
from bench.runner import ROOT

DEFECTS = {'false_positive', 'false_negative', 'mixed'}
JUDGED = DEFECTS | {'ok'}


def profiles_from(path: str | Path) -> list[dict]:
    config = json.loads(Path(path).read_text())
    profiles = config.get('profiles', [])
    if config.get('schema_version') != 1 or not profiles:
        raise ValueError('a version-1 config with profiles is required')
    ids = [profile.get('id', '') for profile in profiles]
    if len(set(ids)) != len(ids) or 'stable' not in ids:
        raise ValueError('profile IDs must be unique and include stable')
    for profile in profiles:
        if not re.fullmatch(r'[a-z][a-z0-9-]*', profile['id']):
            raise ValueError('profile IDs must be safe directory names')
        if profile.get('kind') == 'commit':
            if not re.fullmatch(r'[a-f0-9]{40}', profile.get('ref', '')):
                raise ValueError('a main/source profile requires an immutable full commit SHA')
        elif profile.get('kind') != 'release' or not re.fullmatch(r'\d+\.\d+\.\d+', profile.get('ref', '')):
            raise ValueError('a release profile requires an exact version')
        if not profile.get('binary') or not profile.get('label'):
            raise ValueError('each profile needs a binary and a label')
    return profiles


def compatibility(before: dict, after: dict) -> list[str]:
    problems = []
    for key in ('corpus_fingerprint', 'php_version', 'runner', 'image'):
        left, right = before['meta'].get(key), after['meta'].get(key)
        if not left or not right or left == 'unknown' or right == 'unknown' or left != right:
            problems.append(f'{key} differs or is not recorded')
    if {row['case'] for row in before['cases']} != {row['case'] for row in after['cases']}:
        problems.append('the measured case cohort differs')
    for payload in (before, after):
        if not payload['meta'].get('tool_sha256', {}).get('mago'):
            problems.append('Mago binary checksum is missing')
        if payload['meta'].get('tools', {}).get('mago', 'unknown') == 'unknown':
            problems.append('Mago version probe failed')
    return sorted(set(problems))


def transition(before: str | None, after: str | None) -> str:
    if before not in JUDGED or after not in JUDGED:
        return 'not_comparable'
    if before in DEFECTS and after == 'ok':
        return 'fixed'
    if before == 'ok' and after in DEFECTS:
        return 'regressed'
    return 'still_open' if after in DEFECTS else 'still_ok'


def compare_reports(profiles: list[dict]) -> dict:
    """Compare measured verdicts, never infer a fix from a failed measurement."""
    comparisons = []
    for before, after in zip(profiles, profiles[1:]):
        left, right = before['report'], after['report']
        problems = compatibility(left, right)
        old = {row['case']: row['results'].get('mago', {}) for row in left['cases']}
        new = {row['case']: row['results'].get('mago', {}) for row in right['cases']}
        changes = []
        for case_id in sorted(set(old) | set(new)):
            a, b = old.get(case_id, {}), new.get(case_id, {})
            changes.append({'case': case_id, 'before': a.get('verdict'), 'after': b.get('verdict'),
                            'transition': 'not_comparable' if problems else transition(a.get('verdict'), b.get('verdict'))})
        comparisons.append({'before': before['id'], 'after': after['id'], 'problems': problems,
                            'counts': dict(Counter(row['transition'] for row in changes)), 'cases': changes})
    return {'schema_version': 1, 'profiles': profiles, 'comparisons': comparisons,
            'alignment': 'Benchmark expectations have not been submitted for maintainer agreement.'}


def render_markdown(payload: dict) -> str:
    lines = ['# Mago version comparison', '',
             'Same-case correctness measurements, not a speed benchmark or general quality ranking.', '',
             'Not every expectation is desirable for every tool. FP/FN mean disagreement with the declared baseline, '
             'including warning-policy differences. External reproducers and corrections are welcome.', '',
             '| Profile | Observed version | Source | ok / judged | FP | FN | mixed | excluded |',
             '| --- | --- | --- | --- | --- | --- | --- | --- |']
    for profile in payload['profiles']:
        measured = profile['report']
        summary = measured['summary'].get('mago', {})
        excluded = sum(summary.get(key, 0) for key in ('divergence', 'tool_error', 'case_error', 'skipped'))
        lines.append(f"| {profile['label']} | {measured['meta']['tools'].get('mago', 'unknown')} | "
                     f"`{profile['ref']}` | {summary.get('ok', 0)} / {summary.get('judged', 0)} | "
                     f"{summary.get('false_positive', 0)} | {summary.get('false_negative', 0)} | "
                     f"{summary.get('mixed', 0)} | {excluded} |")
    for pair in payload['comparisons']:
        lines += ['', f"## {pair['before']} → {pair['after']}", '']
        if pair['problems']:
            lines += ['Not comparable: ' + '; '.join(pair['problems']), '']
        lines += ['| Case | Before | After | Transition |', '| --- | --- | --- | --- |']
        lines += [f"| `{row['case']}` | {row['before']} | {row['after']} | {row['transition']} |"
                  for row in pair['cases'] if row['transition'] != 'still_ok']
    lines += ['', payload['alignment'], '']
    return '\n'.join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='tools/mago-matrix.json')
    parser.add_argument('--out', required=True, help='new output directory, retained without automatic pruning')
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args(argv)
    profiles = profiles_from(args.config)
    for profile in profiles:
        binary = Path(ROOT) / profile['binary']
        receipt = binary.with_name(binary.name + '.provenance.json')
        if not binary.is_file() or not receipt.is_file():
            parser.error(f"missing {profile['binary']} or its provenance; run tools/prepare-mago.py first")
        proof = json.loads(receipt.read_text())
        if proof.get('ref') != profile['ref'] or proof.get('sha256') != hashlib.sha256(binary.read_bytes()).hexdigest():
            parser.error(f"{profile['id']} binary does not match its recorded source identity")
        profile['provenance'] = proof
    destination = Path(args.out).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    failed = False
    for profile in profiles:
        env = {**os.environ, 'BENCH_TOOL_MAGO': str(Path(ROOT) / profile['binary'])}
        command = [sys.executable, str(Path(ROOT) / 'harness/bench.py'), 'run',
                   '--output', str(destination / profile['id']), '--jobs', str(args.jobs)]
        if profile['id'] != 'stable':
            command += ['--tool', 'mago']
        print(f"Measuring {profile['label']} ({profile['ref']})", flush=True)
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        (destination / f"{profile['id']}.log").write_text(result.stdout + result.stderr)
        path = destination / profile['id'] / 'report.json'
        if not path.is_file():
            raise RuntimeError(f"{profile['id']} produced no report; see its log")
        profile['report'] = json.loads(path.read_text())
        profile['audit'] = report_mod.audit(profile['report'])
        failed |= bool(result.returncode or profile['audit'])
    payload = compare_reports(profiles)
    measured_ids = {row['case'] for profile in profiles for row in profile['report']['cases']}
    measured_cases = [case for case in case_mod.discover() if case.id in measured_ids]
    if any(case_mod.fingerprint(measured_cases) != profile['report']['meta']['corpus_fingerprint']
           for profile in profiles):
        raise RuntimeError('case source changed between measurements; do not publish this comparison')
    payload['cases'] = []
    for case in measured_cases:
        root = Path(case.path)
        files = {str(path.relative_to(root)): path.read_text()
                 for path in sorted(root.rglob('*')) if path.is_file()
                 and not set(path.relative_to(root).parts) & {'vendor', '.generated', '__pycache__'}}
        payload['cases'].append({'id': case.id, 'manifest': case.data, 'files': files})
    catalog = Path(ROOT) / 'factory/catalog.json'
    if catalog.is_file():
        payload['catalog'] = json.loads(catalog.read_text())
    else:
        payload['catalog'] = {'target_criteria': 120, 'candidates': []}
    assessment = Path(ROOT) / 'factory/assessment.json'
    if assessment.is_file():
        payload['catalog_assessment'] = json.loads(assessment.read_text())
    (destination / 'comparison.json').write_text(json.dumps(payload, indent=2) + '\n')
    markdown = render_markdown(payload)
    (destination / 'COMPARISON.md').write_text(markdown)
    print(markdown)
    return int(failed or any(pair['problems'] for pair in payload['comparisons']))


if __name__ == '__main__':
    raise SystemExit(main())
