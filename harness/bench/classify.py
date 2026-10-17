"""Verdicts.

The vocabulary is intentionally small so that the aggregates stay meaningful:

* ``ok``            - the tool behaved as the case requires
* ``false_positive``- the tool reports something the case forbids
* ``false_negative``- the tool stays silent where the case requires a report
* ``divergence``    - the tool does not implement the rule class by design; not
                      counted as a defect, but listed with its citation
* ``tool_error``    - the tool crashed, timed out, or produced unparseable output
* ``case_error``    - the case itself violates the contract
* ``skipped``       - the case does not apply to the running PHP version
"""

from __future__ import annotations

import re

from . import case as case_mod


def _matches(diagnostic: dict, predicate: dict) -> bool:
    codes = predicate.get("code") or []
    if isinstance(codes, str):
        codes = [codes]
    codes = [code.lower() for code in codes if code]
    if codes and (diagnostic.get("code") or "").lower() not in codes:
        return False
    pattern = predicate.get("message_regex")
    if pattern and not re.search(pattern, diagnostic.get("message") or "", re.IGNORECASE):
        return False
    if predicate.get("file") and not (diagnostic.get("file") or "").endswith(predicate["file"]):
        return False
    if predicate.get("line") is not None:
        tolerance = predicate.get("line_tolerance", 0)
        if diagnostic.get("line") is None or abs(int(diagnostic["line"]) - int(predicate["line"])) > tolerance:
            return False
    return True


def _describe(predicate: dict) -> str:
    if predicate.get("code"):
        return predicate["code"]
    return f"/{predicate.get('message_regex')}/"


def classify(case: case_mod.Case, tool: str, output: dict, php_version: str | None) -> dict:
    """Turn one tool run into a verdict record."""
    result = {
        "case": case.id,
        "tool": tool,
        "verdict": "ok",
        "detail": "",
        "missing": [],
        "unexpected": [],
        "acknowledged": [],
        "diagnostics": output.get("diagnostics", []),
        "exit_code": output.get("exit_code"),
        "duration_s": output.get("duration_s"),
        "php": php_version,
    }

    if case.diagnostics:
        result["verdict"] = "case_error"
        result["detail"] = "; ".join(case.diagnostics)
        return result

    if case.php_max and php_version and _version_tuple(php_version) > _version_tuple(case.php_max):
        result["verdict"] = "skipped"
        result["detail"] = f"case targets PHP <= {case.php_max}, running {php_version}"
        return result
    if php_version and _version_tuple(php_version) < _version_tuple(case.php_min):
        result["verdict"] = "skipped"
        result["detail"] = f"case targets PHP >= {case.php_min}, running {php_version}"
        return result

    expectation = case.expectation(tool)
    mode = expectation.get("mode")

    if mode == "unsupported":
        result["verdict"] = "divergence"
        result["detail"] = expectation.get("reason", "")
        result["citation"] = expectation.get("citation", "")
        return result

    if output.get("tool_error"):
        result["verdict"] = "tool_error"
        result["detail"] = output["tool_error"]
        return result

    diagnostics = output.get("diagnostics", [])
    required = expectation.get("required", [])
    allowed = list(expectation.get("allowed", []))
    forbidden = expectation.get("forbidden", [])

    for predicate in required:
        if not any(_matches(d, predicate) for d in diagnostics):
            result["missing"].append(_describe(predicate))
    for predicate in forbidden:
        hits = [d for d in diagnostics if _matches(d, predicate)]
        result["unexpected"].extend(_summarise(d) for d in hits)

    # Every diagnostic that no predicate claims is either acknowledged (benign
    # by declaration of the case author) or counted. Nothing is dropped silently
    # unless the case opts into a looser reading.
    claims = required + forbidden + allowed
    for diagnostic in diagnostics:
        if any(_matches(diagnostic, predicate) for predicate in claims):
            if any(_matches(diagnostic, predicate) for predicate in allowed) and \
                    not any(_matches(diagnostic, predicate) for predicate in required + forbidden):
                result["acknowledged"].append(_summarise(diagnostic))
            continue
        if expectation.get("allow_additional_diagnostics", False):
            result["acknowledged"].append(_summarise(diagnostic))
        else:
            result["unexpected"].append(_summarise(diagnostic))

    if result["unexpected"]:
        result["unexpected"] = sorted(set(result["unexpected"]))
    if result["missing"]:
        result["missing"] = sorted(set(result["missing"]))

    if result["missing"] and result["unexpected"]:
        result["verdict"] = "mixed"
        result["detail"] = (f"missing {', '.join(result['missing'])}; "
                            f"unexpected {', '.join(result['unexpected'])}")
    elif result["missing"]:
        result["verdict"] = "false_negative"
        result["detail"] = f"missing required diagnostic(s): {', '.join(result['missing'])}"
    elif result["unexpected"]:
        result["verdict"] = "false_positive"
        result["detail"] = f"unexpected diagnostic(s): {', '.join(result['unexpected'])}"
    return result


def _summarise(diagnostic: dict) -> str:
    code = diagnostic.get("code") or "(no code)"
    line = diagnostic.get("line")
    return f"{code}@{line}" if line else code


def _version_tuple(version: str) -> tuple:
    parts = []
    for chunk in str(version).split("."):
        digits = re.match(r"\d+", chunk)
        parts.append(int(digits.group()) if digits else 0)
    return tuple(parts[:3])
