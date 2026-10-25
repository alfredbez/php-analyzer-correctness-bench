"""Source leads must be reproducible, opaque to embedded code, and unscored."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from factory import catalog

PSALM = r'''<?php
abstract class Contract {
    abstract public function providerValidCodeParse(): iterable;
}
class Examples {
    public function providerValidCodeParse(): iterable {
        yield 'a-valid' => ['code' => '<?php $a = ["inner" => ["fake-dataset" => "]"]];'];
        yield 'z-duplicate' => ['code' => '<?php $a = ["inner" => ["fake-dataset" => "]"]];'];
        yield 'b-heredoc' => ['code' => <<<'CODE'
<?php $inside = ['also-not-a-dataset' => [']', '[']];
CODE
        ];
    }
    public function providerInvalidCodeParse(): iterable {
        return ['c-invalid' => ['code' => '<?php broken();', 'error_message' => 'Example']];
    }
}
'''


class CatalogueTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.psalm, self.phpstan, self.repro = [self.root / name for name in ('psalm', 'phpstan', 'repro')]
        self.write(self.psalm / 'tests/ExamplesTest.php', PSALM)
        for index, name in enumerate(('arrays', 'callable', 'throw')):
            text = f'<?php echo {index};\n'
            self.write(self.phpstan / f'tests/PHPStan/Analyser/nsrt/{name}.php', text)
            self.write(self.repro / name / 'repro.php', text)
        self.write(self.repro / 'duplicate/repro.php', '<?php echo 0;\n')
        self.write(self.root / 'COORDINATION.json', json.dumps({'tasks': [
            {'slug': 'arrays', 'id': 'R01', 'status': 'declined',
             'pr_url': 'https://github.com/example/tool/pull/1'}]}))
        for root in (self.psalm, self.phpstan):
            for arguments in (['init', '-q', '-b', 'main'], ['add', '.'],
                              ['-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                               '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'source']):
                subprocess.run(['git', '-C', str(root), *arguments], check=True)

    def write(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_public_build_extracts_named_datasets_and_deduplicates_programs(self):
        payload = catalog.build(self.psalm, self.phpstan, self.repro, limit=3)
        entries = payload['candidates']
        self.assertEqual(len(entries), 9)
        psalm = [entry for entry in entries if entry['family'] == 'psalm']
        self.assertEqual({entry['title'] for entry in psalm}, {'a-valid', 'b-heredoc', 'c-invalid'})
        for family in ('psalm', 'phpstan', 'mago'):
            selected = [entry for entry in entries if entry['family'] == family]
            self.assertEqual(len({entry['probe_sha256'] for entry in selected}), 3)
            self.assertTrue(all(entry['status'] == 'candidate' for entry in selected))
        self.assertIn('arrays', {entry['domain'] for entry in entries if entry['family'] == 'phpstan'})
        historical = next(entry for entry in entries if entry['family'] == 'mago' and entry['title'] == 'arrays')
        self.assertEqual(historical['historical_context']['status'], 'declined')
        self.assertIsNone(historical['citation'])
        for entry in psalm:
            line = PSALM.splitlines()[entry['line'] - 1]
            self.assertIn(entry['title'], line)
            self.assertTrue(entry['citation'].endswith(f"#L{entry['line']}"))

    def test_cli_output_is_byte_identical_for_unchanged_sources(self):
        command = [sys.executable, str(Path(catalog.__file__)), 'build',
                   '--psalm', str(self.psalm), '--phpstan', str(self.phpstan),
                   '--repro', str(self.repro), '--limit-per-family', '3']
        paths = [self.root / name for name in ('one.json', 'two.json')]
        for path in paths:
            subprocess.run([*command, '--out', str(path)], check=True, capture_output=True)
        self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())
        self.assertEqual(json.loads(paths[0].read_text())['target_criteria'], 120)

    def test_incomplete_or_modified_sources_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'missing mago source'):
            catalog.build(self.psalm, self.phpstan, self.root / 'missing', limit=3)
        with self.assertRaisesRegex(ValueError, 'fewer than 4'):
            catalog.build(self.psalm, self.phpstan, self.repro, limit=4)
        self.write(self.psalm / 'tests/ExamplesTest.php', PSALM + '\n// changed\n')
        with self.assertRaisesRegex(ValueError, 'tracked changes'):
            catalog.build(self.psalm, self.phpstan, self.repro, limit=3)

    def expansion_inputs(self):
        inventory = catalog.build(self.psalm, self.phpstan, self.repro, limit=1)
        assessment = catalog.assess([[{
            'candidate_id': entry['id'], 'status': 'deferred', 'case_ids': [],
            'semantic_statement': 'Existing reviewed contract', 'reason': 'Existing decision',
            'citations': ['https://www.php.net/'],
        } for entry in inventory['candidates']]], inventory, {})
        assessment['entries'][0]['review_metadata'] = {'keep': True}
        return inventory, assessment

    def test_expansion_preserves_records_and_pending_outcomes_block_check(self):
        inventory, assessment = self.expansion_inputs()
        before = json.dumps([inventory, assessment], sort_keys=True)
        expanded, outcomes = catalog.expand(inventory, assessment, self.psalm, self.phpstan, limit=1)
        self.assertEqual(json.dumps([inventory, assessment], sort_keys=True), before)
        self.assertEqual(expanded['candidates'][:3], inventory['candidates'])
        self.assertEqual(outcomes['entries'][:3], assessment['entries'])
        self.assertEqual(expanded['target_criteria'], inventory['target_criteria'])
        self.assertEqual(expanded['sources'], inventory['sources'])
        added = expanded['candidates'][3:]
        self.assertEqual([entry['family'] for entry in added], ['psalm', 'phpstan'])
        self.assertTrue(all(entry['citation'].startswith('https://github.com/') for entry in added))
        self.assertEqual([entry['status'] for entry in outcomes['entries'][3:]], ['pending', 'pending'])
        self.assertTrue(all(not entry['criterion_ids'] and not entry['case_ids']
                            for entry in outcomes['entries'][3:]))
        with self.assertRaisesRegex(ValueError, 'unfinished candidate'):
            catalog.check_assessment(outcomes, expanded, {})
        with self.assertRaisesRegex(ValueError, 'every candidate exactly once'):
            catalog.check_assessment(assessment, expanded, {})
        for entry in outcomes['entries'][3:]:
            entry.update(status='deferred', semantic_statement='Reviewed contract', reason='Reviewed decision')
        catalog.check_assessment(outcomes, expanded, {})

    def test_expansion_excludes_prior_ids_and_hashes_including_mago(self):
        inventory, assessment = self.expansion_inputs()
        # A changed program at the same identity must not be selected again.
        old_phpstan = next(entry for entry in inventory['candidates'] if entry['family'] == 'phpstan')
        self.write(Path(old_phpstan['local_path']), '<?php echo "changed";\n')
        # A different ID with an old probe hash must also be excluded.
        self.write(self.phpstan / 'tests/PHPStan/Analyser/nsrt/array-copy.php', '<?php echo 0;\n')
        # Hash exclusion includes historical local probes, even without a public match.
        mago = next(entry for entry in inventory['candidates'] if entry['family'] == 'mago')
        mago['probe_sha256'] = catalog.digest(b'<?php echo 1;\n')
        subprocess.run(['git', '-C', str(self.phpstan), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(self.phpstan), '-c', 'user.name=Test',
                        '-c', 'user.email=test@example.invalid', '-c', 'commit.gpgsign=false',
                        'commit', '-q', '-m', 'updated source'], check=True)
        expanded, _ = catalog.expand(inventory, assessment, self.psalm, self.phpstan, limit=1)
        added = expanded['candidates'][3:]
        self.assertEqual(next(entry['title'] for entry in added if entry['family'] == 'phpstan'), 'throw')
        self.assertFalse({entry['id'] for entry in added} & {entry['id'] for entry in inventory['candidates']})
        self.assertFalse({entry['probe_sha256'] for entry in added}
                         & {entry['probe_sha256'] for entry in inventory['candidates']})

    def test_repeated_expansion_is_fresh_and_exhaustion_does_not_mutate_inputs(self):
        inventory, assessment = self.expansion_inputs()
        for _ in range(2):
            inventory, assessment = catalog.expand(inventory, assessment, self.psalm, self.phpstan, limit=1)
        self.assertEqual(len(inventory['candidates']), 7)
        self.assertEqual(len({entry['id'] for entry in inventory['candidates']}), 7)
        before = json.dumps([inventory, assessment], sort_keys=True)
        with self.assertRaisesRegex(ValueError, 'fresh distinct source leads'):
            catalog.expand(inventory, assessment, self.psalm, self.phpstan, limit=1)
        self.assertEqual(json.dumps([inventory, assessment], sort_keys=True), before)
        for limit in (0, -1):
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, 'positive'):
                catalog.expand(inventory, assessment, self.psalm, self.phpstan, limit=limit)
        with self.assertRaisesRegex(ValueError, 'every candidate exactly once'):
            catalog.expand(inventory, dict(assessment, entries=[]), self.psalm, self.phpstan, limit=1)

    def test_expand_cli_is_deterministic_without_mago_and_check_rejects_pending(self):
        inventory, assessment = self.expansion_inputs()
        inventory_path, assessment_path = self.root / 'inventory.json', self.root / 'assessment.json'
        self.write(inventory_path, json.dumps(inventory))
        self.write(assessment_path, json.dumps(assessment))
        command = [sys.executable, str(Path(catalog.__file__)), 'expand',
                   '--psalm', str(self.psalm), '--phpstan', str(self.phpstan),
                   '--repro', str(self.root / 'nonexistent'), '--limit-per-family', '1',
                   '--inventory', str(inventory_path), '--assessment', str(assessment_path)]
        outputs = []
        for index in range(2):
            out, assessment_out = self.root / f'out-{index}.json', self.root / f'assessment-{index}.json'
            subprocess.run([*command, '--out', str(out), '--assessment-out', str(assessment_out)],
                           check=True, capture_output=True)
            outputs.append((out.read_bytes(), assessment_out.read_bytes()))
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(json.loads(inventory_path.read_text()), inventory)
        self.assertEqual(json.loads(assessment_path.read_text()), assessment)
        checked = subprocess.run([sys.executable, str(Path(catalog.__file__)), 'check',
                                  '--inventory', str(out), '--assessment', str(assessment_out)],
                                 capture_output=True, text=True)
        self.assertNotEqual(checked.returncode, 0)
        self.assertIn('unfinished candidate', checked.stderr)
        # With no output overrides, expand updates the supplied pair in place.
        subprocess.run(command, check=True, capture_output=True)
        self.assertEqual(inventory_path.read_bytes(), outputs[0][0])
        self.assertEqual(assessment_path.read_bytes(), outputs[0][1])
        before = inventory_path.read_bytes(), assessment_path.read_bytes()
        failed = subprocess.run([*command, '--limit-per-family', '3'], capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual((inventory_path.read_bytes(), assessment_path.read_bytes()), before)

    def test_assessment_accounts_for_every_lead_without_inventing_criteria(self):
        inventory = {'candidates': [{'id': 'source:new'}, {'id': 'source:covered'}, {'id': 'source:deferred'}]}
        cases = {'arrays/new': {'criterion_id': 'arrays/shared', 'source_candidate_id': 'source:new'},
                 'arrays/existing': {'criterion_id': 'arrays/shared'}}
        entries = [{'candidate_id': 'source:' + name, 'status': status, 'case_ids': ids,
                    'semantic_statement': 'A stated contract', 'reason': 'A source-backed explanation',
                    'citations': ['https://www.php.net/']}
                   for name, status, ids in [('new', 'measured', ['arrays/new']),
                                            ('covered', 'covered', ['arrays/existing']),
                                            ('deferred', 'deferred', [])]]
        result = catalog.assess([entries], inventory, cases)
        self.assertEqual([entry['criterion_ids'] for entry in result['entries']],
                         [['arrays/shared'], [], ['arrays/shared']])
        for bad_entries in (entries[:-1], entries + [entries[0]],
                            [dict(entries[0], case_ids=['arrays/absent']), *entries[1:]],
                            [dict(entries[0], status='deferred'), *entries[1:]]):
            with self.subTest(entries=bad_entries), self.assertRaises((ValueError, KeyError)):
                catalog.assess([bad_entries], inventory, cases)
        result['entries'][0]['criterion_ids'] = ['arrays/invented']
        with self.assertRaisesRegex(ValueError, 'criterion IDs disagree'):
            catalog.check_assessment(result, inventory, cases)


if __name__ == '__main__':
    unittest.main()
