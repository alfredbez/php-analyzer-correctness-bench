"""Exercise publication gates against a disposable local Git remote."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from factory import bench_factory as factory


MEASUREMENT = '''import json, pathlib, sys
root = pathlib.Path('.')
if sys.argv[1] == 'run':
    name = 'test-' + sys.argv[sys.argv.index('--label') + 1]
    payload = {'meta': {'run_id': name}, 'cases': [
        {'case': str(p.parent.relative_to('cases')), 'results': {
            tool: {'verdict': 'ok'} for tool in ('phpstan', 'psalm', 'mago')}}
        for p in sorted(root.glob('cases/*/*/case.json'))]}
    for directory in (root / 'results/latest', root / 'results/runs' / name):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'report.json').write_text(json.dumps(payload))
'''


class FactoryPublicationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.remote = Path(self.temp.name) / 'remote.git'
        self.tree = Path(self.temp.name) / 'worker'
        self.git('init', '-b', 'main')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Test')
        (self.root / '.gitignore').write_text('factory/evidence/\nresults/latest/\n')
        (self.root / 'harness').mkdir()
        (self.root / 'harness/bench.py').write_text(MEASUREMENT)
        (self.root / 'tools').mkdir()
        (self.root / 'tools/versions.json').write_text('{"pinned": true}\n')
        self.git('add', '.')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-m', 'baseline')
        self.base = self.git('rev-parse', 'HEAD')
        self.git('init', '--bare', str(self.remote))
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', 'origin', 'main')
        self.git('worktree', 'add', '-b', 'factory/auto', str(self.tree))
        binaries = self.tree / 'tools/bin'
        binaries.mkdir()
        for name in ('phpstan.phar', 'psalm.phar', 'mago'):
            (binaries / name).touch()
        with (self.root / '.git/info/exclude').open('a') as handle:
            handle.write('\ntools/bin/\n')
        evidence = self.root / 'factory/evidence'
        evidence.mkdir(parents=True)
        overrides = patch.multiple(factory, ROOT=str(self.root), WORKTREE=str(self.tree),
                                   EVIDENCE_DIR=str(evidence), STATE_FILE=str(evidence / 'STATE.json'),
                                   LOG_FILE=str(evidence / 'factory.log'),
                                   PROMPT_DIR=str(self.root / 'factory/prompts'),
                                   TARGETS={'narrowing': 1},
                                   IMPLEMENTERS=['test/author'], REVIEWERS=['test/reviewer'])
        overrides.start()
        self.addCleanup(overrides.stop)

    def git(self, *args, cwd=None):
        return subprocess.check_output(['git', *args], cwd=cwd or self.root,
                                       stderr=subprocess.DEVNULL, text=True).strip()

    def dispatch(self, tree, model, prompt, label, state):
        if label.startswith('grow-'):
            case = self.tree / 'cases/narrowing/example'
            case.mkdir(parents=True)
            (case / 'case.json').write_text('{}\n')
            self.git('add', 'cases', cwd=tree)
            self.git('-c', 'commit.gpgsign=false', 'commit', '-m', 'add candidate', cwd=tree)
        else:
            base, head = re.search(r'git diff ([a-f0-9]+)\.\.([a-f0-9]+)', prompt).groups()
            receipt = re.search(r'receipt path: (.+)', prompt).group(1)
            Path(receipt).write_text(json.dumps({
                'base': base, 'head': head, 'verdict': self.verdict,
                'cases': ['narrowing/example'], 'reason': 'Checked the candidate.'}))
            return {'code': self.review_exit}
        return {'code': 0}

    def round(self, verdict='accept', review_exit=0):
        self.verdict, self.review_exit = verdict, review_exit
        with patch.object(factory, 'dispatch', side_effect=self.dispatch):
            return factory.round_once({})

    def remote_head(self):
        return self.git('--git-dir', str(self.remote), 'rev-parse', 'main')

    def test_accepted_candidate_publishes_source_and_full_measurement(self):
        result = self.round()
        self.assertEqual(result['status'], 'promoted')
        files = self.git('--git-dir', str(self.remote), 'ls-tree', '-r', '--name-only', 'main')
        self.assertIn('cases/narrowing/example/case.json', files)
        self.assertIn('results/runs/test-factory-1/report.json', files)
        receipt = json.loads(self.git('--git-dir', str(self.remote), 'show',
                                      'main:results/runs/test-factory-1/review.json'))
        self.assertEqual(receipt['verdict'], 'accept')
        self.assertEqual(receipt['base'], self.base)
        self.assertEqual(receipt['head'], result['head'])
        self.assertEqual(receipt['reviewer'], 'test/reviewer')
        self.assertNotEqual(self.remote_head(), self.base)

    def test_failed_reviewer_cannot_publish_even_with_an_acceptance_receipt(self):
        self.assertEqual(self.round(review_exit=1)['status'], 'review_failed')
        self.assertEqual(self.remote_head(), self.base)

    def test_rejection_blocks_publication_and_is_preserved_for_inspection(self):
        self.assertEqual(self.round(verdict='reject')['status'], 'rejected')
        self.assertEqual(self.remote_head(), self.base)
        self.assertTrue((self.tree / 'cases/narrowing/example/case.json').exists())

    def test_rejected_and_uncommitted_output_survives_a_successful_fresh_round(self):
        self.assertEqual(self.round(verdict='reject')['status'], 'rejected')
        (self.tree / 'unfinished.txt').write_text('Keep this failed experiment.\n')
        rejected_head = self.git('rev-parse', 'HEAD', cwd=self.tree)
        self.verdict, self.review_exit = 'accept', 0
        state = {}
        with patch.object(factory, 'dispatch', side_effect=self.dispatch), \
                patch.object(factory, 'prepare_tooling', return_value=True):
            result = factory.round_once(state)
        self.assertEqual(result['status'], 'promoted')
        archive = Path(state['quarantines'][0]['path'])
        self.assertEqual((archive / 'unfinished.txt').read_text(), 'Keep this failed experiment.\n')
        self.assertEqual(self.git('rev-parse', 'HEAD', cwd=archive), rejected_head)
        published = self.git('--git-dir', str(self.remote), 'ls-tree', '-r', '--name-only', 'main')
        self.assertNotIn('unfinished.txt', published)
        self.assertFalse((self.tree / 'unfinished.txt').exists())

    def test_variants_do_not_increase_semantic_coverage(self):
        for slug in ('first', 'second'):
            case = self.tree / 'cases/arrays' / slug
            case.mkdir(parents=True)
            (case / 'case.json').write_text(json.dumps({
                'id': f'arrays/{slug}', 'criterion_id': 'arrays/key-preservation'}))
        self.assertEqual(factory.corpus_domains(str(self.tree)), {'arrays': 1})

    def test_catalogue_queue_skips_previously_rejected_candidates(self):
        (self.tree / 'factory').mkdir()
        entries = [{'id': f'psalm-{n}', 'domain': 'narrowing'} for n in range(3)]
        (self.tree / 'factory/catalog.json').write_text(json.dumps({'candidates': entries}))
        state = {'rounds': [{'status': 'rejected', 'task': {'candidate_ids': ['psalm-0']}}]}
        task = factory.pick_task(str(self.tree), state)
        self.assertEqual(task['candidate_ids'], ['psalm-1'])

    def test_pin_changes_are_not_published(self):
        original = self.dispatch

        def change_pin(tree, model, prompt, label, state):
            result = original(tree, model, prompt, label, state)
            if label.startswith('grow-'):
                (self.tree / 'tools/versions.json').write_text('{"pinned": false}\n')
                self.git('add', 'tools/versions.json', cwd=tree)
                self.git('-c', 'commit.gpgsign=false', 'commit', '-m', 'change pin', cwd=tree)
            return result

        with patch.object(factory, 'dispatch', side_effect=change_pin):
            result = factory.round_once({})
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(self.remote_head(), self.base)

    def test_rate_limited_implementer_falls_back_to_another_model(self):
        original = self.dispatch

        def fail_first(tree, model, prompt, label, state):
            if model == 'test/unavailable':
                return {'code': 1}
            return original(tree, model, prompt, label, state)

        self.verdict, self.review_exit = 'accept', 0
        with patch.object(factory, 'IMPLEMENTERS', ['test/unavailable', 'test/author']), \
                patch.object(factory, 'dispatch', side_effect=fail_first):
            result = factory.round_once({})
        self.assertEqual(result['status'], 'promoted')
        self.assertNotEqual(self.remote_head(), self.base)

    def test_only_rate_limit_failures_cool_down_the_next_author_round(self):
        original_run = factory.run
        responses = [
            ('62e52cd9fe3ab4429debc0eb0306057419b0a9d6 Merge pull request', False),
            ('src/repro.php:429: comparison always false', False),
            ('Error: HTTP 429', True),
            ('HTTP/1.1 429', True),
            ('status code: 429', True),
            ('Error: Rate limit exceeded. Please try again later.', True),
        ]
        for output, limited in responses:
            with self.subTest(output=output):
                def run_worker(cmd, cwd, timeout=600):
                    if cmd[0] == 'opencode':
                        return {'code': 1, 'stdout': output, 'stderr': '', 'seconds': 0}
                    return original_run(cmd, cwd, timeout)

                state = {}
                with patch.object(factory, 'run', side_effect=run_worker):
                    result = factory.round_once(state)
                self.assertEqual(result['status'], 'implementation_failed')
                next_round = factory.round_once(state, dry_run=True)
                self.assertEqual(next_round['implementers'], [] if limited else ['test/author'])
                self.assertEqual(self.remote_head(), self.base)

    def test_failed_author_changes_are_preserved_without_fallback_or_publication(self):
        original = self.dispatch

        def fail_after_writing(tree, model, prompt, label, state):
            original(tree, model, prompt, label, state)
            return {'code': 1}

        with patch.object(factory, 'dispatch', side_effect=fail_after_writing):
            result = factory.round_once({})
        self.assertEqual(result['status'], 'blocked')
        self.assertTrue((self.tree / 'cases/narrowing/example/case.json').exists())
        self.assertEqual(self.remote_head(), self.base)

    def test_non_object_receipt_cannot_publish(self):
        original = self.dispatch

        def malformed_receipt(tree, model, prompt, label, state):
            result = original(tree, model, prompt, label, state)
            if label.startswith('review-'):
                receipt = re.search(r'receipt path: (.+)', prompt).group(1)
                Path(receipt).write_text('[]')
            return result

        self.verdict, self.review_exit = 'accept', 0
        with patch.object(factory, 'dispatch', side_effect=malformed_receipt):
            result = factory.round_once({})
        self.assertEqual(result['status'], 'review_failed')
        self.assertEqual(self.remote_head(), self.base)

    def test_dry_run_does_not_create_state_or_modify_git(self):
        state = {}
        result = factory.round_once(state, dry_run=True)
        self.assertEqual(result['status'], 'dry_run')
        self.assertEqual(state, {})
        self.assertFalse(Path(factory.STATE_FILE).exists())
        self.assertEqual(self.remote_head(), self.base)


class WorkerTimeoutTest(unittest.TestCase):
    def test_timeout_stops_descendants_before_they_can_write(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / 'late-write'
            child = f"import time,pathlib; time.sleep(0.5); pathlib.Path({str(marker)!r}).touch()"
            parent = ('import subprocess,sys,time; '
                      f'subprocess.Popen([sys.executable, "-c", {child!r}]); time.sleep(5)')
            result = factory.run([sys.executable, '-c', parent], cwd=directory, timeout=0.1)
            self.assertEqual(result['code'], 124)
            time.sleep(0.6)
            self.assertFalse(marker.exists())
