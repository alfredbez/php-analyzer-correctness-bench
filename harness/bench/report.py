"""Aggregation and rendering.

The report is the product of this repository, so the two things it must never do
are (a) present a number without its denominator and (b) hide a divergence behind
an aggregate. Both are enforced here.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import time

from .runner import ROOT

VERDICT_ORDER = ("ok", "false_positive", "false_negative", "mixed", "divergence",
                 "tool_error", "case_error", "skipped")
SYMBOLS = {
    "ok": "ok",
    "false_positive": "**FP**",
    "false_negative": "**FN**",
    "mixed": "**FP+FN**",
    "divergence": "n/a",
    "tool_error": "ERR",
    "case_error": "BAD",
    "skipped": "skip",
}


def new_run_dir(label: str = "") -> str:
    stamp = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime())
    name = f"{stamp}-{label}" if label else stamp
    path = os.path.join(ROOT, "results", "runs", name)
    os.makedirs(path, exist_ok=True)
    return path


def summarise(records: list[dict], meta: dict) -> dict:
    report = {"meta": meta, "cases": records, "summary": {}, "divergences": []}
    meta["runtime_proven"] = sum(1 for record in records
                                 if (record.get("runtime_proof") or {}).get("confirmed"))
    meta["runtime_proof_failed"] = [record["case"] for record in records
                                    if record.get("runtime_proof")
                                    and not record["runtime_proof"]["confirmed"]]
    tools = sorted({tool for record in records for tool in record["results"]})
    for tool in tools:
        counters = {verdict: 0 for verdict in VERDICT_ORDER}
        domains: dict[str, dict] = {}
        for record in records:
            result = record["results"].get(tool)
            if not result:
                continue
            counters[result["verdict"]] = counters.get(result["verdict"], 0) + 1
            domain = domains.setdefault(record["domain"], {verdict: 0 for verdict in VERDICT_ORDER})
            domain[result["verdict"]] += 1
            if result["verdict"] == "divergence":
                report["divergences"].append({
                    "case": record["case"], "tool": tool,
                    "reason": result.get("detail", ""), "citation": result.get("citation", ""),
                })
        judged = counters["ok"] + counters["false_positive"] + counters["false_negative"] + counters["mixed"]
        report["summary"][tool] = {
            **counters,
            "judged": judged,
            "cases": sum(counters.values()),
            "agreement": round(counters["ok"] / judged * 100, 1) if judged else None,
            "defects": counters["false_positive"] + counters["false_negative"] + counters["mixed"],
            "by_domain": domains,
        }
    return report


def render_summary(report: dict) -> str:
    meta = report["meta"]
    lines = ["# Correctness summary", ""]
    lines.append(f"- Run: `{meta['run_id']}`")
    lines.append(f"- Started: {meta['started']} (UTC)")
    for name, version in meta["tools"].items():
        lines.append(f"- {name}: {version}")
    lines.append(f"- PHP: {meta['php_version']}")
    lines.append(f"- Cases: {meta['case_count']} (valid: {meta['valid_cases']})")
    lines.append(f"- Runtime checks passed: "
                 f"{meta.get('runtime_proven', 0)}/{meta['case_count']}")
    if meta.get("runtime_proof_failed"):
        lines.append(f"- **Runtime proofs that failed: {', '.join(meta['runtime_proof_failed'])}** - "
                     "those cases are excluded and must be repaired")
    lines.append("")
    lines.append("`agreement` = ok / judged, where judged = ok + false positives + false negatives + mixed. "
                 "By-design divergences, tool errors, case errors and skips are excluded and listed separately.")
    lines.append("")
    lines.append("| Tool | Cases | Judged | ok | FP | FN | mixed | by-design | tool error | case error | skipped | agreement |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for tool, summary in sorted(report["summary"].items()):
        agreement = "n/a" if summary["agreement"] is None else f"{summary['agreement']}%"
        lines.append(
            f"| {tool} | {summary['cases']} | {summary['judged']} | {summary['ok']} | {summary['false_positive']} | "
            f"{summary['false_negative']} | {summary['mixed']} | {summary['divergence']} | "
            f"{summary['tool_error']} | {summary['case_error']} | {summary['skipped']} | {agreement} |")
    lines.append("")
    lines.append("## Per domain")
    lines.append("")
    lines.append("| Domain | Tool | Cases | ok | FP | FN | by-design |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for tool, summary in sorted(report["summary"].items()):
        for domain, counters in sorted(summary["by_domain"].items()):
            total = sum(counters.values())
            lines.append(f"| {domain} | {tool} | {total} | {counters['ok']} | "
                         f"{counters['false_positive']} | {counters['false_negative']} | "
                         f"{counters['divergence']} |")
    if report["divergences"]:
        lines.append("")
        lines.append("## Recorded by-design divergences")
        lines.append("")
        lines.append("| Case | Tool | Reason | Citation |")
        lines.append("| --- | --- | --- | --- |")
        for item in report["divergences"]:
            lines.append(f"| `{item['case']}` | {item['tool']} | {item['reason']} | {item['citation']} |")
    lines.append("")
    return "\n".join(lines)


def render_matrix(report: dict) -> str:
    tools = sorted(report["summary"].keys())
    lines = ["# Correctness matrix", "",
             "| Case | Domain | Rule class | Ground truth | " + " | ".join(tools) + " |",
             "| --- | --- | --- | --- | " + " | ".join("---" for _ in tools) + " |"]
    for record in report["cases"]:
        basis = record.get("basis", "")
        if record.get("runtime_proof", {}).get("confirmed"):
            basis += " (runtime)"
        cells = []
        for tool in tools:
            result = record["results"].get(tool) or {}
            cell = SYMBOLS.get(result.get("verdict", ""), "?")
            if result.get("verdict") in ("false_positive", "false_negative", "mixed") and result.get("detail"):
                cell += f" <sub>{_clip(result['detail'])}</sub>"
            cells.append(cell)
        lines.append(f"| `{record['case']}` | {record['domain']} | {record['rule_class']} | {basis} | "
                     + " | ".join(cells) + " |")
    lines.append("")
    lines.append("Legend: `ok` matches the case, **FP** false positive, **FN** false negative, "
                 "`n/a` by-design divergence, `ERR` tool error, `BAD` invalid case, `skip` not applicable.")
    lines.append("")
    return "\n".join(lines)


def _clip(text: str, limit: int = 70) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def audit(report: dict) -> list[str]:
    """Report-level invariants. Anything here makes a row unreadable or unfounded."""
    problems = []
    for record in report["cases"]:
        if not record.get("basis"):
            problems.append(f"{record['case']}: no ground truth basis recorded")
        for tool, result in record["results"].items():
            verdict = result.get("verdict")
            if verdict in ("false_positive", "false_negative", "mixed") and not result.get("detail"):
                problems.append(f"{record['case']} / {tool}: {verdict} without a detail")
            if verdict in ("false_positive", "false_negative", "mixed") and not result.get("diagnostics") \
                    and verdict == "false_positive":
                problems.append(f"{record['case']} / {tool}: false positive without any reported diagnostic")
            if verdict == "divergence" and not result.get("citation"):
                problems.append(f"{record['case']} / {tool}: divergence without a citation")
            if verdict == "tool_error":
                problems.append(f"{record['case']} / {tool}: tool error - {result.get('detail', '')[:80]}")
            if verdict == "case_error":
                problems.append(f"{record['case']} / {tool}: case error - {result.get('detail', '')[:80]}")
    for tool, summary in report["summary"].items():
        if summary["judged"] == 0:
            problems.append(f"{tool}: no case judged this run; the agreement column is empty")
    return problems


def render_gaps(report: dict, tool: str) -> str:
    """A per-tool work list: everything this analyzer got wrong, with evidence."""
    lines = [f"# Gaps for {tool}", "",
             f"From run `{report['meta']['run_id']}` "
             f"({report['meta']['tools'].get(tool, 'unknown version')}, PHP {report['meta']['php_version']}).",
             "",
             "Each entry is a case file a maintainer (or their agent) can run directly; the raw "
             "tool output of the run is in the run directory next to this report.",
             ""]
    for record in report["cases"]:
        result = record["results"].get(tool)
        if not result or result["verdict"] not in ("false_positive", "false_negative", "mixed"):
            continue
        lines.append(f"## `{record['case']}` - {result['verdict']}")
        lines.append("")
        lines.append(f"- rule class: `{record['rule_class']}`, domain: `{record['domain']}`")
        lines.append(f"- ground truth basis: `{record.get('basis')}`")
        if result.get("detail"):
            lines.append(f"- what the tool did: {result['detail']}")
        if result.get("missing"):
            lines.append(f"- missing: {', '.join(f'`{item}`' for item in result['missing'])}")
        if result.get("unexpected"):
            lines.append(f"- reported but not justified: {', '.join(f'`{item}`' for item in result['unexpected'])}")
        lines.append(f"- run it: `python3 harness/bench.py run --case {record['case']} --tool {tool}` "
                     f"(case directory: `{record['path']}`)")
        lines.append("")
    if len(lines) <= 7:
        if report['summary'][tool]['judged'] == 0:
            lines.append("No cases were judged; no quality conclusion is available.")
        else:
            lines.append("Nothing to report: this analyzer matched every case it was judged against.")
        lines.append("")
    return "\n".join(lines)


def write_report(run_dir: str, report: dict) -> None:
    with open(os.path.join(run_dir, "report.json"), "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    with open(os.path.join(run_dir, "SUMMARY.md"), "w", encoding="utf-8") as handle:
        handle.write(render_summary(report))
    with open(os.path.join(run_dir, "MATRIX.md"), "w", encoding="utf-8") as handle:
        handle.write(render_matrix(report))
    for tool in sorted(report["summary"]):
        with open(os.path.join(run_dir, f"GAPS-{tool}.md"), "w", encoding="utf-8") as handle:
            handle.write(render_gaps(report, tool))


def publish(report: dict, run_dir: str, keep: int = 20) -> None:
    """Refresh the local convenience copy and prune old run directories.

    `results/latest/` is regenerated on every publish and therefore not tracked;
    the committed history is `results/runs/<run>/`. Pruning keeps the newest
    `keep` runs in the working tree - the older ones stay in git history, so
    nothing is lost, and a fresh checkout does not carry a hundred snapshots.
    """
    latest = os.path.join(ROOT, "results", "latest")
    os.makedirs(latest, exist_ok=True)
    for name in os.listdir(run_dir):
        if not name.endswith((".md", ".json")):
            continue
        with open(os.path.join(run_dir, name), "r", encoding="utf-8") as source:
            content = source.read()
        with open(os.path.join(latest, name), "w", encoding="utf-8") as target:
            target.write(content)

    runs_dir = os.path.join(ROOT, "results", "runs")
    runs = sorted((entry for entry in os.listdir(runs_dir)
                   if os.path.isdir(os.path.join(runs_dir, entry))), reverse=True)
    for stale in runs[keep:]:
        shutil.rmtree(os.path.join(runs_dir, stale), ignore_errors=True)
