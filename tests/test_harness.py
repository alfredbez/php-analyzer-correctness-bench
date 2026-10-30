"""Harness self-test.

The benchmark's output is only as good as the parsing behind it, so the adapters
and the classification run against captured tool output. The fixtures are real
output, not hand-written snippets: see tests/fixtures/ for provenance.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "harness"))

from bench import adapters, classify  # noqa: E402
from bench.case import Case  # noqa: E402
from bench.runner import ROOT  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def fixture(name: str) -> str:
    with open(os.path.join(FIXTURES, name), "r", encoding="utf-8") as handle:
        return handle.read()


def make_case(expect: dict, **overrides) -> Case:
    data = {
        "id": "narrowing/example",
        "title": "example",
        "domain": "narrowing",
        "rule_class": "impossible-condition",
        "ground_truth": {"basis": "php_semantics", "statement": "is_int on a string is always false"},
        "expect": expect,
    }
    data.update(overrides)
    return Case(path=os.path.join(FIXTURES, "..", "..", "cases", "narrowing", "is-int-on-string"), data=data)


class AdapterTest(unittest.TestCase):
    def test_phpstan_reports_identifier_and_line(self):
        parsed = adapters.parse_phpstan(fixture("phpstan-impossible-type.json"), "")
        self.assertEqual(parsed["tool_error"], None)
        self.assertEqual(len(parsed["diagnostics"]), 1)
        diagnostic = parsed["diagnostics"][0]
        self.assertEqual(diagnostic["code"], "function.impossibleType")
        self.assertEqual(diagnostic["line"], 15)
        self.assertTrue(diagnostic["file"].endswith("cases/narrowing/is-int-on-string/src/repro.php"))
        self.assertFalse(os.path.isabs(diagnostic["file"]))

    def test_psalm_reports_type_and_one_based_line(self):
        parsed = adapters.parse_psalm(fixture("psalm-type-does-not-contain.json"), "")
        self.assertEqual(len(parsed["diagnostics"]), 1)
        self.assertEqual(parsed["diagnostics"][0]["code"], "TypeDoesNotContainType")
        self.assertEqual(parsed["diagnostics"][0]["line"], 15)

    def test_mago_shifts_zero_based_lines(self):
        parsed = adapters.parse_mago(fixture("mago-impossible-type.json"), "")
        self.assertEqual(len(parsed["diagnostics"]), 2)
        lines = {diagnostic["line"] for diagnostic in parsed["diagnostics"]}
        # mago's JSON says 14 for a call that sits on line 15.
        self.assertEqual(lines, {15})
        self.assertEqual({d["code"] for d in parsed["diagnostics"]},
                         {"impossible-type-comparison", "impossible-condition"})

    def test_psalm_noise_is_a_tool_error_not_an_empty_result(self):
        parsed = adapters.parse_psalm("Could not find any composer autoloaders in /bench", "")
        self.assertIsNotNone(parsed["tool_error"])

    def test_phpstan_internal_error_is_surfaced(self):
        parsed = adapters.parse_phpstan('{"totals":{"errors":1},"files":{},"errors":["Internal error"]}', "")
        self.assertEqual(parsed["tool_error"], "Internal error")

    def test_pzoom_requires_complete_counts_and_keeps_one_based_locations(self):
        captured = json.loads(fixture('pzoom-stub-scan-error.json'))
        self.assertIsNotNone(adapters.parse_pzoom(captured['stdout'], captured['stderr'])['tool_error'])
        output = ('ERROR: InvalidOperand - src/probe.php:5:12 - Cannot use bitwise not on type bool\n'
                  'INFO: MixedAssignment - src/probe.php:9:3 - Mixed assignment\n'
                  '1 errors found\n1 other issues found.\n'
                  'Checks took 0.25 seconds and used 53.613MB of memory\n')
        parsed = adapters.parse_pzoom(output, '')
        self.assertIsNone(parsed['tool_error'])
        self.assertEqual([(d['code'], d['line'], d['file'], d['severity'])
                          for d in parsed['diagnostics']],
                         [('InvalidOperand', 5, 'src/probe.php', 'error'),
                          ('MixedAssignment', 9, 'src/probe.php', 'info')])
        for broken, stderr in ((output.split('Checks took')[0], ''),
                               (output.replace('1 errors found', '2 errors found'), ''),
                               (output.replace('1 other issues found.', ''), ''),
                               (output, 'Scan error in stubs/extensions/sockets.phpstub'),
                               ('No errors found!', '')):
            with self.subTest(output=broken, stderr=stderr):
                self.assertIsNotNone(adapters.parse_pzoom(broken, stderr)['tool_error'])
        clean = 'No errors found!\nChecks took 0.25 seconds and used 53.613MB of memory\n'
        self.assertEqual(adapters.parse_pzoom(clean, ''), {'diagnostics': [], 'tool_error': None})


class AnalyzerExitStatusTest(unittest.TestCase):
    def test_timeout_with_valid_partial_json_is_not_a_successful_measurement(self):
        from bench import execute

        class TimedOutRunner:
            mode = "native"

            def exec(self, argv, cwd, timeout):
                return {"stdout": '{"issues": []}', "stderr": "timed out",
                        "exit_code": 124, "duration_s": 0.1}

        case = make_case({"mago": {"mode": "clean"}})
        record = execute.run_case(case, TimedOutRunner(), tools=["mago"], php_version="8.3.35")
        result = record["results"]["mago"]
        self.assertEqual(result["verdict"], "tool_error")
        self.assertIn("124", result["detail"])
        self.assertEqual(result["exit_code"], 124)


class ClassificationTest(unittest.TestCase):
    def test_pzoom_is_opt_in_and_unreviewed_results_are_not_scored(self):
        from bench import execute
        self.assertEqual({spec.name for spec in execute.selected_tools()}, {'phpstan', 'psalm', 'mago'})
        self.assertEqual([spec.name for spec in execute.selected_tools(['pzoom'])], ['pzoom'])
        case = make_case({'psalm': {'mode': 'clean'}})
        result = classify.classify(case, 'pzoom', {'diagnostics': []}, '8.4')
        self.assertEqual(result['verdict'], 'skipped')
        result = classify.classify(case, 'pzoom', {'tool_error': 'truncated report'}, '8.4')
        self.assertEqual(result['verdict'], 'tool_error')
        case.data['expect']['pzoom'] = {'mode': 'diagnostics', 'required': [{'code': 'InvalidOperand'}]}
        result = classify.classify(case, 'pzoom', {'diagnostics': []}, '8.4')
        self.assertEqual(result['verdict'], 'false_negative')

    def _classify(self, expect: dict, diagnostics: list[dict], tool: str = "phpstan"):
        case = make_case(expect)
        output = {"diagnostics": diagnostics, "tool_error": None, "exit_code": 1}
        return classify.classify(case, tool, output, "8.3.35")

    def test_required_diagnostic_matches(self):
        expect = {"phpstan": {"mode": "diagnostics",
                              "required": [{"code": "function.impossibleType", "line": 15}]}}
        result = self._classify(expect, [{"code": "function.impossibleType", "line": 15, "message": ""}])
        self.assertEqual(result["verdict"], "ok")

    def test_missing_required_diagnostic_is_a_false_negative(self):
        expect = {"phpstan": {"mode": "diagnostics", "required": [{"code": "function.impossibleType"}]}}
        result = self._classify(expect, [])
        self.assertEqual(result["verdict"], "false_negative")

    def test_unclaimed_diagnostic_is_a_false_positive(self):
        expect = {"phpstan": {"mode": "diagnostics", "required": [{"code": "function.impossibleType"}]}}
        result = self._classify(expect, [{"code": "function.impossibleType", "line": 15, "message": ""},
                                         {"code": "deadCode.unreachable", "line": 16, "message": ""}])
        self.assertEqual(result["verdict"], "false_positive")
        self.assertIn("deadCode.unreachable@16", result["unexpected"])

    def test_allowed_diagnostic_is_acknowledged_not_counted(self):
        expect = {"phpstan": {"mode": "diagnostics",
                              "required": [{"code": "function.impossibleType", "line": 15}],
                              "allowed": [{"code": "deadCode.unreachable", "reason": "same root cause"}]}}
        result = self._classify(expect, [{"code": "function.impossibleType", "line": 15, "message": ""},
                                         {"code": "deadCode.unreachable", "line": 16, "message": ""}])
        self.assertEqual(result["verdict"], "ok")
        self.assertEqual(result["acknowledged"], ["deadCode.unreachable@16"])

    def test_clean_case_reports_a_false_positive(self):
        expect = {"phpstan": {"mode": "clean"}}
        result = self._classify(expect, [{"code": "someRule", "line": 3, "message": ""}])
        self.assertEqual(result["verdict"], "false_positive")

    def test_unsupported_becomes_a_divergence_with_citation(self):
        expect = {"phpstan": {"mode": "unsupported", "reason": "not implemented",
                              "citation": "https://example.invalid/doc"}}
        result = self._classify(expect, [])
        self.assertEqual(result["verdict"], "divergence")
        self.assertEqual(result["citation"], "https://example.invalid/doc")

    def test_line_tolerance_is_honoured(self):
        expect = {"phpstan": {"mode": "diagnostics",
                              "required": [{"code": "x", "line": 15, "line_tolerance": 1}]}}
        result = self._classify(expect, [{"code": "x", "line": 16, "message": ""}])
        self.assertEqual(result["verdict"], "ok")

    def test_line_tolerance_exceeded_fails_match(self):
        expect = {"phpstan": {"mode": "diagnostics",
                              "required": [{"code": "x", "line": 15, "line_tolerance": 1}]}}
        result = self._classify(expect, [{"code": "x", "line": 17, "message": ""}])
        self.assertEqual(result["verdict"], "mixed")
        self.assertIn("x", result["missing"])
        self.assertIn("x@17", result["unexpected"])

    def test_php_version_skip(self):
        case = make_case({"phpstan": {"mode": "clean"}})
        case.data["php"] = {"min": "8.4"}
        output = {"diagnostics": [], "tool_error": None, "exit_code": 0}
        result = classify.classify(case, "phpstan", output, "8.3.35")
        self.assertEqual(result["verdict"], "skipped")


class RuntimeProofGateTest(unittest.TestCase):
    """A case whose own runtime proof fails must not judge any tool."""

    class StubRunner:
        mode = "native"

        def __init__(self, proof_exit_code: int):
            self.proof_exit_code = proof_exit_code
            self.tool_calls = 0

        def runtime_path(self, path: str) -> str:
            return path

        def php(self, args, cwd, timeout=300, env=None):
            if any(str(arg).endswith("check.php") for arg in args):
                return {"exit_code": self.proof_exit_code, "stdout": "", "stderr": "boom",
                        "duration_s": 0.0, "argv": args, "cwd": cwd}
            self.tool_calls += 1
            return {"exit_code": 0, "stdout": '{"totals":{"errors":0},"files":{},"errors":[]}',
                    "stderr": "", "duration_s": 0.0, "argv": args, "cwd": cwd}

        def exec(self, argv, cwd, timeout=300, env=None):
            self.tool_calls += 1
            return {"exit_code": 0, "stdout": '{"issues":[]}', "stderr": "",
                    "duration_s": 0.0, "argv": argv, "cwd": cwd}

    def _case(self):
        from bench import case as case_mod
        return case_mod.load(os.path.join(ROOT, "cases", "narrowing", "is-int-on-string"))

    def test_failed_proof_marks_every_tool_as_case_error(self):
        from bench import execute
        runner = self.StubRunner(proof_exit_code=7)
        record = execute.run_case(self._case(), runner, tools=["mago"], php_version="8.3.35")
        self.assertEqual(record["results"]["mago"]["verdict"], "case_error")
        self.assertEqual(runner.tool_calls, 0, "no tool may run when the proof fails")

    def test_successful_proof_lets_the_tools_run(self):
        from bench import execute
        runner = self.StubRunner(proof_exit_code=0)
        record = execute.run_case(self._case(), runner, tools=["mago"], php_version="8.3.35")
        self.assertEqual(runner.tool_calls, 1)
        self.assertNotEqual(record["results"]["mago"]["verdict"], "case_error")

    def test_incompatible_php_skips_a_case_even_when_its_runtime_would_fail(self):
        from bench import execute
        for bounds in ({"min": "8.4"}, {"max": "8.2.99"}):
            with self.subTest(bounds=bounds):
                case = self._case()
                case.data["php"] = bounds
                runner = self.StubRunner(proof_exit_code=255)
                record = execute.run_case(case, runner, php_version="8.3.35")
                self.assertEqual({result["verdict"] for result in record["results"].values()},
                                 {"skipped"})
                self.assertNotIn("runtime_proof", record)

    def test_missing_real_dependencies_cannot_be_replaced_with_a_stub(self):
        from bench import execute
        with tempfile.TemporaryDirectory() as root:
            case = self._case()
            case.path = root
            case.data['composer'] = {'install': True}
            record = execute.run_case(case, self.StubRunner(0), php_version='8.3.35')
            self.assertEqual({result['verdict'] for result in record['results'].values()}, {'case_error'})
            self.assertTrue(all('dependencies' in result['detail'] for result in record['results'].values()))
            self.assertFalse(os.path.exists(os.path.join(root, 'vendor/autoload.php')))


class ReportTest(unittest.TestCase):
    def test_gap_report_does_not_claim_success_without_judged_cases(self):
        from bench import report
        for verdict in ('tool_error', 'skipped', 'ok'):
            with self.subTest(verdict=verdict):
                payload = report.summarise([
                    {'case': 'assignability/example', 'domain': 'assignability',
                     'results': {'pzoom': {'verdict': verdict}}}],
                    {'run_id': 'experiment', 'tools': {'pzoom': 'pzoom pinned'}, 'php_version': '8.4'})
                text = report.render_gaps(payload, 'pzoom')
                if verdict == 'ok':
                    self.assertIn('matched every case', text)
                else:
                    self.assertIn('No cases were judged', text)
                    self.assertNotIn('matched every case', text)


class ContractTest(unittest.TestCase):
    def test_validator_rejects_an_unsupported_expectation_without_citation(self):
        from bench import case as case_mod
        for tool in ('phpstan', 'pzoom'):
            with self.subTest(tool=tool):
                case = make_case({tool: {"mode": "unsupported", "reason": "no"}})
                problems = case_mod.validate(case)
                self.assertTrue(any(f"expect.{tool}" in problem and "citation" in problem
                                    for problem in problems))

    def test_validator_rejects_an_allowed_entry_without_reason(self):
        case = make_case({"phpstan": {"mode": "diagnostics",
                                      "required": [{"code": "x"}],
                                      "allowed": [{"code": "y"}]}})
        from bench import case as case_mod
        problems = case_mod.validate(case)
        self.assertTrue(any("allowed entry needs a 'reason'" in problem for problem in problems))

    def test_validator_rejects_invalid_line_tolerance(self):
        from bench import case as case_mod
        for bad_tolerance in (-1, "one", 1.5, True):
            with self.subTest(tolerance=bad_tolerance):
                case = make_case({"phpstan": {"mode": "diagnostics",
                                              "required": [{"code": "x", "line": 10, "line_tolerance": bad_tolerance}]}})
                problems = case_mod.validate(case)
                self.assertTrue(any("line_tolerance must be a non-negative integer" in p for p in problems))

    def test_validator_rejects_line_tolerance_without_line(self):
        from bench import case as case_mod
        case = make_case({"phpstan": {"mode": "diagnostics",
                                      "required": [{"code": "x", "line_tolerance": 2}]}})
        problems = case_mod.validate(case)
        self.assertTrue(any("line_tolerance requires 'line' to be specified" in p for p in problems))

    def test_corpus_is_valid(self):
        from bench import case as case_mod
        broken = {case.id: case.diagnostics for case in case_mod.discover() if case.diagnostics}
        self.assertEqual(broken, {})


class PsalmConfigTest(unittest.TestCase):
    def test_generated_config_resolves_targets_from_its_own_directory(self):
        from bench import execute
        with tempfile.TemporaryDirectory() as root:
            targets = ["src", "lib/nested"]
            for target in targets:
                os.makedirs(os.path.join(root, target))
            case = Case(path=root, data={"targets": targets})
            config = execute.ensure_psalm_config(case)
            xml = ET.parse(config).getroot()
            base = os.path.dirname(config)
            resolved = [os.path.normpath(os.path.join(base, node.attrib["name"]))
                        for node in xml.findall("projectFiles/directory")]
            self.assertEqual(resolved, [os.path.join(root, target) for target in targets])
            self.assertEqual(os.path.normpath(os.path.join(base, xml.attrib["cacheDirectory"])),
                             os.path.join(root, ".generated", "psalm-cache"))


if __name__ == "__main__":
    unittest.main()
