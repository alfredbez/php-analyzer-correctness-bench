"""Unit tests for tools/audit_expectations.py."""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "harness"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))

from audit_expectations import (
    audit_case_expectations,
    codes_semantically_similar,
    format_markdown_table,
    normalize_code,
    Asymmetry,
)


class AuditExpectationsTest(unittest.TestCase):
    def test_normalize_and_semantic_similarity(self):
        self.assertEqual(normalize_code("MixedReturnStatement"), "mixedreturnstatement")
        self.assertEqual(normalize_code("mixed-return-statement"), "mixedreturnstatement")
        self.assertTrue(codes_semantically_similar("MixedReturnStatement", "mixed-return-statement"))
        self.assertTrue(codes_semantically_similar("UnusedVariable", "unused-variable"))
        self.assertTrue(codes_semantically_similar("TypeDoesNotContainType", "impossible-condition"))
        self.assertFalse(codes_semantically_similar("MixedReturnStatement", "UndefinedMethod"))

    def test_symmetrical_case_has_no_asymmetry(self):
        case_data = {
            "id": "test/symmetric",
            "expect": {
                "phpstan": {
                    "mode": "diagnostics",
                    "required": [{"code": "some.code", "line": 10, "file": "src/test.php"}],
                    "allowed": [{"code": "some.secondary", "line": 10, "reason": "secondary"}],
                },
                "psalm": {
                    "mode": "diagnostics",
                    "required": [{"code": "SomeCode", "line": 10, "file": "src/test.php"}],
                    "allowed": [{"code": "SomeSecondary", "line": 10, "reason": "secondary"}],
                },
                "mago": {
                    "mode": "diagnostics",
                    "required": [{"code": "some-code", "line": 10, "file": "src/test.php"}],
                    "allowed": [{"code": "some-secondary", "line": 10, "reason": "secondary"}],
                },
            },
        }
        findings = audit_case_expectations(case_data)
        self.assertEqual(findings, [])

    def test_detects_allowed_asymmetry(self):
        # ac60f1cdd2c628cc61fc pattern: psalm has allowed, mago does not
        case_data = {
            "id": "narrowing/catalog-mago-ac60f1cdd2c628cc61fc",
            "expect": {
                "phpstan": {
                    "mode": "diagnostics",
                    "required": [{"code": "method.notFound", "line": 7}],
                },
                "psalm": {
                    "mode": "diagnostics",
                    "required": [{"code": "UndefinedMethod", "line": 7}],
                    "allowed": [{"code": "MixedReturnStatement", "line": 7, "reason": "secondary"}],
                },
                "mago": {
                    "mode": "diagnostics",
                    "required": [{"code": "non-existent-method", "line": 7}],
                },
            },
        }
        findings = audit_case_expectations(case_data)
        categories = [f.category for f in findings]
        self.assertIn("allowed_presence_asymmetry", categories)
        self.assertIn("allowed_entry_missing", categories)

    def test_detects_line_and_count_asymmetry(self):
        case_data = {
            "id": "test/asymmetric-lines",
            "expect": {
                "phpstan": {
                    "mode": "diagnostics",
                    "required": [{"code": "err1", "line": 5}, {"code": "err2", "line": 6}],
                },
                "psalm": {
                    "mode": "diagnostics",
                    "required": [{"code": "err1", "line": 10}],
                },
                "mago": {
                    "mode": "diagnostics",
                    "required": [{"code": "err1", "line": 5}],
                },
            },
        }
        findings = audit_case_expectations(case_data)
        categories = [f.category for f in findings]
        self.assertIn("required_count_asymmetry", categories)
        self.assertIn("required_line_deviation", categories)

    def test_detects_mode_asymmetry(self):
        case_data = {
            "id": "test/mode-diff",
            "expect": {
                "phpstan": {"mode": "diagnostics", "required": [{"code": "err", "line": 5}]},
                "psalm": {"mode": "diagnostics", "required": [{"code": "err", "line": 5}]},
                "mago": {"mode": "unsupported", "reason": "unsupported feature"},
            },
        }
        findings = audit_case_expectations(case_data)
        categories = [f.category for f in findings]
        self.assertIn("mode_asymmetry", categories)

    def test_detects_runtime_followup_match(self):
        case_data = {
            "id": "narrowing/catalog-mago-ac60f1cdd2c628cc61fc",
            "expect": {
                "phpstan": {"mode": "diagnostics", "required": [{"code": "method.notFound", "line": 7}]},
                "psalm": {
                    "mode": "diagnostics",
                    "required": [{"code": "UndefinedMethod", "line": 7}],
                    "allowed": [{"code": "MixedReturnStatement", "line": 7}],
                },
                "mago": {"mode": "diagnostics", "required": [{"code": "non-existent-method", "line": 7}]},
            },
        }
        tool_results = {
            "phpstan": {"verdict": "ok", "unexpected": []},
            "psalm": {"verdict": "ok", "unexpected": []},
            "mago": {"verdict": "false_positive", "unexpected": ["mixed-return-statement@7"]},
        }
        findings = audit_case_expectations(case_data, tool_results)
        categories = [f.category for f in findings]
        self.assertIn("runtime_followup_unallowed", categories)

    def test_format_markdown_table(self):
        asym = Asymmetry(
            case_id="test/case",
            category="allowed_entry_missing",
            tools=["psalm", "mago"],
            summary="test summary",
        )
        md = format_markdown_table([asym])
        self.assertIn("| `test/case` |", md)
        self.assertIn("psalm, mago", md)


if __name__ == "__main__":
    unittest.main()
