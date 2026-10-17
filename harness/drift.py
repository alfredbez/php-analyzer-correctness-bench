#!/usr/bin/env python3
"""Compare a fresh report against a baseline report.

Used by the nightly drift job: the pinned versions produced the baseline, the
current stable releases produced the fresh run, and the difference is the only
interesting output. A verdict that flips is either an upstream fix (defect gone)
or a regression, and both are worth a human's attention.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bench.report import ROOT  # noqa: E402


def load(path: str) -> dict:
    import json
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def verdict_map(report: dict) -> dict:
    return {record["case"]: {tool: result["verdict"] for tool, result in record["results"].items()}
            for record in report["cases"]}


def render(baseline: dict, fresh: dict) -> str:
    old, new = verdict_map(baseline), verdict_map(fresh)
    lines = ["# Analyzer drift", "",
             f"- baseline: `{baseline['meta']['run_id']}` "
             f"({', '.join(f'{k} {v.split()[-1]}' for k, v in baseline['meta']['tools'].items())})",
             f"- fresh: `{fresh['meta']['run_id']}` "
             f"({', '.join(f'{k} {v.split()[-1]}' for k, v in fresh['meta']['tools'].items())})",
             ""]
    changes = []
    for case in sorted(set(old) | set(new)):
        for tool in sorted(set(old.get(case, {})) | set(new.get(case, {}))):
            before = old.get(case, {}).get(tool)
            after = new.get(case, {}).get(tool)
            if before != after:
                changes.append((case, tool, before, after))
    if not changes:
        lines.append("No verdict changed.")
    else:
        lines += ["| Case | Tool | Baseline | Fresh |", "| --- | --- | --- | --- |"]
        lines += [f"| `{case}` | {tool} | {before} | {after} |" for case, tool, before, after in changes]
    lines.append("")
    lines.append("## Counters")
    lines.append("")
    lines.append("| Tool | Baseline ok/FP/FN | Fresh ok/FP/FN |")
    lines.append("| --- | --- | --- |")
    for tool in sorted(set(baseline["summary"]) | set(fresh["summary"])):
        old_summary = baseline["summary"].get(tool, {})
        new_summary = fresh["summary"].get(tool, {})
        lines.append(f"| {tool} | {old_summary.get('ok')}/{old_summary.get('false_positive')}/"
                     f"{old_summary.get('false_negative')} | {new_summary.get('ok')}/"
                     f"{new_summary.get('false_positive')}/{new_summary.get('false_negative')} |")
    lines.append("")
    return "\n".join(lines), changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default=os.path.join(ROOT, "results/latest/report.json"))
    parser.add_argument("--fresh", required=True)
    parser.add_argument("--out", default=os.path.join(ROOT, "drift.md"))
    parser.add_argument("--fail-on-change", action="store_true")
    args = parser.parse_args()

    text, changes = render(load(args.baseline), load(args.fresh))
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(text)
    return 1 if (changes and args.fail_on_change) else 0


if __name__ == "__main__":
    raise SystemExit(main())
