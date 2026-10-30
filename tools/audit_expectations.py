#!/usr/bin/env python3
"""Audit benchmark expectations across tools for asymmetries and inconsistencies.

Finds:
1. Allowed asymmetries: allowed entries present in one tool but absent/differing in another.
2. Required count asymmetries: differing counts of required diagnostics.
3. Required line/file deviations: differing target lines or files.
4. Mode asymmetries: differing modes (diagnostics vs clean vs unsupported).
5. Cross-tool follow-up diagnostic matches (when a run report is supplied):
   unexpected diagnostics in one tool that mirror allowed entries in another.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
import os
import re
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if os.path.join(ROOT, "harness") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "harness"))

from bench.case import Case, discover, TOOLS


@dataclass
class Asymmetry:
    case_id: str
    category: str
    tools: list[str]
    summary: str
    details: dict[str, Any] = field(default_factory=dict)


def normalize_code(code: str) -> str:
    """Normalize diagnostic code for cross-tool comparison."""
    if not code:
        return ""
    # Remove separators, make lowercase
    cleaned = re.sub(r"[-_.]+", "", code.lower())
    return cleaned


def codes_semantically_similar(code1: str, code2: str) -> bool:
    """Check if two diagnostic codes likely refer to the same type of diagnostic."""
    n1 = normalize_code(code1)
    n2 = normalize_code(code2)
    if not n1 or not n2:
        return False
    if n1 == n2 or n1 in n2 or n2 in n1:
        return True
    
    # Common semantic families
    families = [
        {"mixedreturn", "mixedreturnstatement", "mixedreturntype"},
        {"unusedvariable", "unusedvar"},
        {"unusedparameter", "unusedparam"},
        {"deadcode", "unreachable", "unreachablecode"},
        {"redundantcast", "redundantcastgivendocblocktype"},
        {"redundantcondition", "impossiblecondition", "typedoesnotcontaintype", "functionimpossibletype"},
        {"missingtype", "missingclosureparamtype", "missingparamtype"},
    ]
    for fam in families:
        if any(f in n1 for f in fam) and any(f in n2 for f in fam):
            return True
    return False


def audit_case_expectations(case_data: dict, tool_results: dict[str, Any] | None = None) -> list[Asymmetry]:
    """Audit a single case expectation dict for asymmetries between tools."""
    asymmetries: list[Asymmetry] = []
    case_id = case_data.get("id", "unknown")
    expect = case_data.get("expect", {})
    tools = [t for t in TOOLS if t in expect]

    modes = {t: expect[t].get("mode", "unsupported") for t in tools}

    # 1. Mode Asymmetry
    distinct_modes = set(modes.values())
    if len(distinct_modes) > 1:
        asymmetries.append(
            Asymmetry(
                case_id=case_id,
                category="mode_asymmetry",
                tools=tools,
                summary=f"Different expectation modes: {modes}",
                details={"modes": modes},
            )
        )

    # 2. Allowed Asymmetries
    allowed_by_tool: dict[str, list[dict]] = {
        t: expect[t].get("allowed", []) for t in tools if modes.get(t) == "diagnostics"
    }

    # Check if some tools have allowed entries while others in diagnostics mode have none
    tools_with_allowed = [t for t, a in allowed_by_tool.items() if len(a) > 0]
    tools_without_allowed = [t for t, a in allowed_by_tool.items() if len(a) == 0]

    if tools_with_allowed and tools_without_allowed:
        asymmetries.append(
            Asymmetry(
                case_id=case_id,
                category="allowed_presence_asymmetry",
                tools=tools,
                summary=(
                    f"Allowed entries defined for {tools_with_allowed} but missing for {tools_without_allowed}"
                ),
                details={
                    "tools_with_allowed": {t: allowed_by_tool[t] for t in tools_with_allowed},
                    "tools_without_allowed": tools_without_allowed,
                },
            )
        )

    # Cross-tool allowed code/line comparison
    for t1 in tools_with_allowed:
        for entry in allowed_by_tool[t1]:
            line1 = entry.get("line")
            code1 = entry.get("code")
            code_str = str(code1) if code1 else ""
            reason = entry.get("reason", "")

            # Check other tools in diagnostics mode
            for t2 in tools:
                if t1 == t2 or modes.get(t2) != "diagnostics":
                    continue
                t2_allowed = allowed_by_tool.get(t2, [])
                matching_entry = None
                for e2 in t2_allowed:
                    line2 = e2.get("line")
                    code2 = str(e2.get("code", ""))
                    if (line1 is not None and line2 is not None and line1 == line2) or codes_semantically_similar(code_str, code2):
                        matching_entry = e2
                        break
                
                if not matching_entry:
                    asymmetries.append(
                        Asymmetry(
                            case_id=case_id,
                            category="allowed_entry_missing",
                            tools=[t1, t2],
                            summary=f"{t1} allows '{code_str}' (line {line1}), but {t2} has no matching allowed entry",
                            details={
                                "tool_with_entry": t1,
                                "tool_missing_entry": t2,
                                "entry": entry,
                                "reason": reason,
                            },
                        )
                    )

    # 3. Required Count Asymmetry
    req_counts = {
        t: len(expect[t].get("required", []))
        for t in tools
        if modes.get(t) == "diagnostics"
    }
    if len(set(req_counts.values())) > 1:
        asymmetries.append(
            Asymmetry(
                case_id=case_id,
                category="required_count_asymmetry",
                tools=list(req_counts.keys()),
                summary=f"Differing required diagnostic counts: {req_counts}",
                details={"required_counts": req_counts},
            )
        )

    # 4. Required Line / File Asymmetry
    lines_by_tool: dict[str, list[int | None]] = {}
    files_by_tool: dict[str, list[str | None]] = {}
    for t in tools:
        if modes.get(t) == "diagnostics":
            reqs = expect[t].get("required", [])
            lines_by_tool[t] = [r.get("line") for r in reqs]
            files_by_tool[t] = [r.get("file") for r in reqs]

    # Compare non-empty lines
    active_lines = {t: l for t, l in lines_by_tool.items() if l}
    if len(set(tuple(l) for l in active_lines.values())) > 1:
        asymmetries.append(
            Asymmetry(
                case_id=case_id,
                category="required_line_deviation",
                tools=list(active_lines.keys()),
                summary=f"Required lines differ across tools: {active_lines}",
                details={"lines": active_lines},
            )
        )

    active_files = {t: f for t, f in files_by_tool.items() if f}
    if len(set(tuple(f) for f in active_files.values())) > 1:
        asymmetries.append(
            Asymmetry(
                case_id=case_id,
                category="required_file_deviation",
                tools=list(active_files.keys()),
                summary=f"Required files differ across tools: {active_files}",
                details={"files": active_files},
            )
        )

    # 5. Runtime correlation check (if tool results from a report are provided)
    if tool_results:
        for t, res in tool_results.items():
            unexpected = res.get("unexpected", [])
            diagnostics = res.get("diagnostics", [])
            for unexp in unexpected:
                # unexp is typically formatted like "code@line"
                unexp_code = unexp.split("@")[0] if "@" in unexp else unexp
                unexp_line = None
                if "@" in unexp:
                    try:
                        unexp_line = int(unexp.split("@")[1])
                    except ValueError:
                        pass

                # Check if another tool had this allowed or acknowledged
                for other_t, other_res in tool_results.items():
                    if other_t == t:
                        continue
                    # Check other tool's allowed in expect
                    other_allowed = expect.get(other_t, {}).get("allowed", [])
                    for ea in other_allowed:
                        ea_code = str(ea.get("code", ""))
                        ea_line = ea.get("line")
                        if codes_semantically_similar(unexp_code, ea_code) or (
                            unexp_line is not None and ea_line is not None and unexp_line == ea_line
                        ):
                            asymmetries.append(
                                Asymmetry(
                                    case_id=case_id,
                                    category="runtime_followup_unallowed",
                                    tools=[t, other_t],
                                    summary=(
                                        f"{t} emitted unexpected diagnostic '{unexp}', while {other_t} "
                                        f"has allowed entry '{ea_code}' (line {ea_line})"
                                    ),
                                    details={
                                        "tool_with_unexpected": t,
                                        "tool_with_allowed": other_t,
                                        "unexpected_diagnostic": unexp,
                                        "matching_allowed": ea,
                                    },
                                )
                            )

    return asymmetries


def audit_corpus(cases: list[Case], report_path: str | None = None) -> list[Asymmetry]:
    """Audit all cases in the corpus and return all found asymmetries."""
    report_data_by_case: dict[str, dict[str, Any]] = {}
    if report_path and os.path.isfile(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            rep = json.load(f)
            for c in rep.get("cases", []):
                case_id = c.get("case")
                if case_id:
                    report_data_by_case[case_id] = c.get("results", {})

    all_asymmetries: list[Asymmetry] = []
    for case in cases:
        case_results = report_data_by_case.get(case.id)
        findings = audit_case_expectations(case.data, case_results)
        all_asymmetries.extend(findings)

    return all_asymmetries


def format_markdown_table(asymmetries: list[Asymmetry]) -> str:
    """Format asymmetries as a Markdown table."""
    lines = [
        "# Benchmark Expectation Asymmetry Audit",
        "",
        f"Total asymmetries identified: {len(asymmetries)}",
        "",
        "| Case | Category | Tools | Summary |",
        "|---|---|---|---|",
    ]
    for asym in asymmetries:
        tools_str = ", ".join(asym.tools)
        # escape pipes in summary
        summary_esc = asym.summary.replace("|", "\\|")
        lines.append(f"| `{asym.case_id}` | `{asym.category}` | {tools_str} | {summary_esc} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit benchmark expectations for cross-tool asymmetries.")
    parser.add_argument("--report", help="Path to report.json to correlate runtime diagnostics with allowed entries.")
    parser.add_argument("--output", help="Path to write output markdown table.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format.")
    args = parser.parse_args()

    cases = discover()
    asymmetries = audit_corpus(cases, report_path=args.report)

    if args.format == "json":
        out = json.dumps([asym.__dict__ for asym in asymmetries], indent=2)
    else:
        out = format_markdown_table(asymmetries)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Audit completed: {len(asymmetries)} asymmetries found. Written to {args.output}")
    else:
        print(out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
