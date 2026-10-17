"""Harness self-test.

The benchmark's output is only as good as the parsing behind it, so the adapters
and the classification run against captured tool output. The fixtures are real
output, not hand-written snippets: see tests/fixtures/ for provenance.
"""

from __future__ import annotations

import json
import os
import sys
import unittest

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


class ClassificationTest(unittest.TestCase):
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


class ContractTest(unittest.TestCase):
    def test_validator_rejects_an_unsupported_expectation_without_citation(self):
        case = make_case({"phpstan": {"mode": "unsupported", "reason": "no"}})
        from bench import case as case_mod
        problems = case_mod.validate(case)
        self.assertTrue(any("citation" in problem for problem in problems))

    def test_validator_rejects_an_allowed_entry_without_reason(self):
        case = make_case({"phpstan": {"mode": "diagnostics",
                                      "required": [{"code": "x"}],
                                      "allowed": [{"code": "y"}]}})
        from bench import case as case_mod
        problems = case_mod.validate(case)
        self.assertTrue(any("allowed entry needs a 'reason'" in problem for problem in problems))

    def test_corpus_is_valid(self):
        from bench import case as case_mod
        broken = {case.id: case.diagnostics for case in case_mod.discover() if case.diagnostics}
        self.assertEqual(broken, {})


if __name__ == "__main__":
    unittest.main()
