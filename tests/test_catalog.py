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


if __name__ == '__main__':
    unittest.main()
