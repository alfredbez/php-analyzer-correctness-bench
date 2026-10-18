"""Version comparisons must not manufacture improvements from incomparable data."""

import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'harness'))
import compare
from bench.case import Case, fingerprint

site_spec = importlib.util.spec_from_file_location('benchmark_site', Path(compare.__file__).with_name('site.py'))
benchmark_site = importlib.util.module_from_spec(site_spec)
site_spec.loader.exec_module(benchmark_site)


def measured(verdicts):
    return {'meta': {'corpus_fingerprint': 'same-source', 'php_version': '8.3.35',
                     'runner': 'docker', 'image': 'php:8.3-cli', 'tool_sha256': {'mago': 'abc'},
                     'tools': {'mago': 'mago 1.57.0'}},
            'cases': [{'case': f'arrays/{name}', 'results': {'mago': {'verdict': verdict}}}
                      for name, verdict in verdicts.items()]}


class ComparisonTest(unittest.TestCase):
    def test_fixes_regressions_and_unmeasured_results_stay_distinct(self):
        before = measured({'fixed': 'false_positive', 'regressed': 'ok', 'open': 'false_negative',
                           'scope': 'divergence', 'failed': 'false_positive', 'mixed': 'mixed', 'clean': 'ok'})
        after = measured({'fixed': 'ok', 'regressed': 'false_negative', 'open': 'false_positive',
                          'scope': 'ok', 'failed': 'tool_error', 'mixed': 'ok', 'clean': 'ok'})
        result = compare.compare_reports([{'id': 'historical', 'report': before}, {'id': 'stable', 'report': after}])
        pair = result['comparisons'][0]
        self.assertEqual(pair['problems'], [])
        self.assertEqual(pair['counts'], {'fixed': 2, 'regressed': 1, 'still_open': 1,
                                          'not_comparable': 2, 'still_ok': 1})
        by_case = {row['case']: row['transition'] for row in pair['cases']}
        self.assertEqual(by_case['arrays/failed'], 'not_comparable')
        self.assertEqual(by_case['arrays/scope'], 'not_comparable')

    def test_changed_source_runtime_or_cohort_cannot_count_as_a_fix(self):
        before = measured({'example': 'false_positive'})
        fresh = measured({'example': 'ok'})
        variants = []
        for key, value in [('corpus_fingerprint', 'changed'), ('php_version', '8.4.0'),
                           ('tool_sha256', {}), ('tools', {'mago': 'unknown'})]:
            candidate = copy.deepcopy(fresh)
            candidate['meta'][key] = value
            variants.append(candidate)
        missing_case = copy.deepcopy(fresh)
        missing_case['cases'] = []
        variants.append(missing_case)
        for candidate in variants:
            with self.subTest(candidate=candidate):
                result = compare.compare_reports([{'id': 'historical', 'report': before}, {'id': 'stable', 'report': candidate}])
                pair = result['comparisons'][0]
                self.assertTrue(pair['problems'])
                self.assertEqual(pair['counts'], {'not_comparable': 1})

    def test_main_profile_requires_an_immutable_commit(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'profiles.json'
            profile = {'id': 'stable', 'label': 'main', 'kind': 'commit', 'ref': 'main', 'binary': 'mago'}
            path.write_text(json.dumps({'schema_version': 1, 'profiles': [profile]}))
            with self.assertRaisesRegex(ValueError, 'immutable'):
                compare.profiles_from(path)
            profile['ref'] = 'a' * 40
            path.write_text(json.dumps({'schema_version': 1, 'profiles': [profile]}))
            self.assertEqual(compare.profiles_from(path)[0]['ref'], 'a' * 40)


class EvidenceTest(unittest.TestCase):
    def test_report_controls_remain_offline_and_secondary_content_starts_closed(self):
        class ReportElements(HTMLParser):
            def __init__(self):
                super().__init__()
                self.elements = []

            def handle_starttag(self, tag, attrs):
                self.elements.append((tag, dict(attrs)))

        parser = ReportElements()
        parser.feed(benchmark_site.render({'schema_version': 1, 'profiles': [{'id': 'stable'}], 'cases': []}))
        ids = [attrs['id'] for _, attrs in parser.elements if 'id' in attrs]
        for control in ('search', 'domain', 'finding', 'pair', 'reset', 'download',
                        'matrix', 'case-detail', 'report-data', 'catalog'):
            self.assertEqual(ids.count(control), 1)
        details = [attrs for tag, attrs in parser.elements if tag == 'details']
        self.assertTrue(details)
        self.assertTrue(all('open' not in attrs for attrs in details))
        for tag, attrs in parser.elements:
            if tag in ('script', 'img', 'iframe', 'link'):
                self.assertNotIn('src', attrs)
                self.assertNotIn('href', attrs)
        self.assertIn(('html', {'lang': 'en'}), parser.elements)

    def test_source_fingerprint_is_portable_but_changes_with_case_semantics(self):
        with tempfile.TemporaryDirectory() as temporary:
            cases = []
            for directory in ('left', 'right'):
                root = Path(temporary) / directory
                (root / 'src').mkdir(parents=True)
                (root / 'src/repro.php').write_text('<?php function result(): int { return 3; }')
                (root / 'case.json').write_text('{"expect":"clean"}')
                cases.append(Case(str(root), {'id': 'arrays/example'}))
            expected = fingerprint([cases[0]])
            self.assertEqual(expected, fingerprint([cases[1]]))
            root = Path(cases[1].path)
            (root / 'vendor').mkdir()
            (root / 'vendor/autoload.php').write_text('generated')
            self.assertEqual(expected, fingerprint([cases[1]]))
            (root / 'src/repro.php').write_text('<?php function result(): int { return "wrong"; }')
            self.assertNotEqual(expected, fingerprint([cases[1]]))
            expected = fingerprint([cases[1]])
            (root / 'composer.lock').write_text('{"packages":[{"version":"1.0.0"}]}')
            self.assertNotEqual(expected, fingerprint([cases[1]]))

    def test_embedded_source_cannot_close_the_json_script(self):
        payload = {'schema_version': 1, 'profiles': [{'id': 'stable'}], 'cases': [],
                   'hostile_source': '</script><script>window.injected = true</script>'}
        html = benchmark_site.render(payload)
        self.assertNotIn(payload['hostile_source'], html)
        encoded = html.split('<script id="report-data" type="application/json">', 1)[1].split('</script>', 1)[0]
        self.assertEqual(json.loads(encoded)['hostile_source'], payload['hostile_source'])
