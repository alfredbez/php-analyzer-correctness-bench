"""Aggregation and rendering.

The report is the product of this repository, so the two things it must never do
are (a) present a number without its denominator and (b) hide a divergence behind
an aggregate. Both are enforced here.
"""

from __future__ import annotations

import json
import os
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
    lines.append("")
    lines.append("`agreement` = ok / (ok + false positives + false negatives). Cases whose ground truth "
                 "is a by-design divergence, a tool error or a skip are excluded and listed separately.")
    lines.append("")
    lines.append("| Tool | Cases | ok | false positive | false negative | mixed | by-design | tool error | agreement |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for tool, summary in sorted(report["summary"].items()):
        agreement = "n/a" if summary["agreement"] is None else f"{summary['agreement']}%"
        lines.append(
            f"| {tool} | {summary['cases']} | {summary['ok']} | {summary['false_positive']} | "
            f"{summary['false_negative']} | {summary['mixed']} | {summary['divergence']} | "
            f"{summary['tool_error']} | {agreement} |")
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


def write_report(run_dir: str, report: dict) -> None:
    with open(os.path.join(run_dir, "report.json"), "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    with open(os.path.join(run_dir, "SUMMARY.md"), "w", encoding="utf-8") as handle:
        handle.write(render_summary(report))
    with open(os.path.join(run_dir, "MATRIX.md"), "w", encoding="utf-8") as handle:
        handle.write(render_matrix(report))


def publish(report: dict, run_dir: str) -> None:
    """Refresh results/latest so that links into the repository stay stable."""
    latest = os.path.join(ROOT, "results", "latest")
    os.makedirs(latest, exist_ok=True)
    for name in ("report.json", "SUMMARY.md", "MATRIX.md"):
        with open(os.path.join(run_dir, name), "r", encoding="utf-8") as source:
            content = source.read()
        with open(os.path.join(latest, name), "w", encoding="utf-8") as target:
            target.write(content)
