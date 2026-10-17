#!/usr/bin/env python3
"""Entry point for the PHP analyzer correctness benchmark.

    python3 harness/bench.py list
    python3 harness/bench.py validate
    python3 harness/bench.py run --case narrowing/is-int-on-string
    python3 harness/bench.py run --label local --jobs 2
    python3 harness/bench.py show results/latest/SUMMARY.md
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bench import case as case_mod           # noqa: E402
from bench import execute, report            # noqa: E402
from bench.runner import ROOT, Runner        # noqa: E402


def tool_versions(runner: Runner) -> dict:
    versions = {}
    phpstan = runner.php([runner.runtime_path(os.path.join(ROOT, "tools/bin/phpstan.phar")), "--version"],
                         cwd=ROOT, timeout=120)
    versions["phpstan"] = phpstan["stdout"].strip().splitlines()[0] if phpstan["exit_code"] == 0 else "unknown"
    psalm = runner.php([runner.runtime_path(os.path.join(ROOT, "tools/bin/psalm.phar")), "--version"],
                       cwd=ROOT, timeout=120)
    versions["psalm"] = psalm["stdout"].strip().splitlines()[0] if psalm["exit_code"] == 0 else "unknown"
    mago = runner.exec([runner.runtime_path(os.path.join(ROOT, "tools/bin/mago")), "--version"],
                       cwd=ROOT, timeout=60)
    versions["mago"] = mago["stdout"].strip().splitlines()[0] if mago["exit_code"] == 0 else "unknown"
    return versions


def cmd_list(args) -> int:
    cases = case_mod.discover()
    if args.json:
        print(json.dumps([case_mod.to_json(case) for case in cases], indent=2))
        return 0
    for case in cases:
        flag = "ok " if not case.diagnostics else "BAD"
        print(f"{flag} {case.id:52s} {case.domain:14s} {case.rule_class}")
    print(f"\n{len(cases)} case(s), {sum(1 for c in cases if c.diagnostics)} invalid")
    return 0


def cmd_validate(args) -> int:
    cases = case_mod.discover()
    broken = [case for case in cases if case.diagnostics]
    for case in broken:
        print(f"INVALID {case.path}")
        for problem in case.diagnostics:
            print(f"  - {problem}")
    print(f"{len(cases)} case(s) checked, {len(broken)} invalid")
    return 1 if broken else 0


def cmd_run(args) -> int:
    cases = case_mod.discover()
    if args.case:
        wanted = set(args.case)
        cases = [case for case in cases if case.id in wanted]
        missing = wanted - {case.id for case in cases}
        if missing:
            print(f"unknown case(s): {', '.join(sorted(missing))}", file=sys.stderr)
            return 2
    if args.domain:
        cases = [case for case in cases if case.domain == args.domain]
    if args.shard:
        index, total = _parse_shard(args.shard)
        cases = [case for position, case in enumerate(cases) if position % total == index]
        print(f"shard {index + 1}/{total}: {len(cases)} case(s)")
    if not cases:
        print("no cases selected", file=sys.stderr)
        return 2

    runner = Runner(php_version=args.php)
    php_version = args.php_version or runner.php_version()
    run_dir = None if args.no_save else report.new_run_dir(args.label)
    meta = {
        "run_id": os.path.basename(run_dir) if run_dir else "ephemeral",
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runner": runner.mode,
        "image": runner.image if runner.mode == "docker" else "host",
        "php_version": php_version,
        "tools": tool_versions(runner),
        "pins": json.load(open(os.path.join(ROOT, "tools/versions.json"), encoding="utf-8"))["tools"],
        "case_count": len(cases),
        "valid_cases": sum(1 for case in cases if not case.diagnostics),
        "selected": [case.id for case in cases],
    }

    records = []
    if args.jobs > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(execute.run_case, case, runner, args.tool, php_version, run_dir)
                       for case in cases]
            for future in concurrent.futures.as_completed(futures):
                records.append(future.result())
    else:
        for case in cases:
            record = execute.run_case(case, runner, args.tool, php_version, run_dir)
            records.append(record)
            _print_progress(record)
    records.sort(key=lambda record: record["case"])

    payload = report.summarise(records, meta)
    if run_dir:
        report.write_report(run_dir, payload)
        report.publish(payload, run_dir)
    print(report.render_summary(payload))
    if run_dir:
        print(f"Artifacts: {os.path.relpath(run_dir, ROOT)}")
    return 0


def _print_progress(record: dict) -> None:
    cells = " ".join(f"{tool}={result['verdict']}"
                     for tool, result in sorted(record["results"].items()))
    print(f"  {record['case']:52s} {cells}")


def _parse_shard(value: str) -> tuple[int, int]:
    """`i/n` (one-based) -> (zero-based index, total)."""
    try:
        index_text, total_text = value.split("/", 1)
        index, total = int(index_text), int(total_text)
    except ValueError as exc:
        raise SystemExit(f"--shard expects i/n, got {value!r}") from exc
    if total < 1 or not 1 <= index <= total:
        raise SystemExit(f"--shard out of range: {value!r}")
    return index - 1, total


def cmd_gaps(args) -> int:
    path = args.report
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    tools = [args.tool] if args.tool else sorted(payload["summary"])
    for tool in tools:
        text = report.render_gaps(payload, tool)
        target = os.path.join(os.path.dirname(path), f"GAPS-{tool}.md")
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)
        print(text)
    return 0


def cmd_show(args) -> int:
    path = args.path
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    with open(path, "r", encoding="utf-8") as handle:
        print(handle.read())
    return 0


def cmd_doctor(args) -> int:
    runner = Runner(php_version=args.php)
    print(f"runner mode: {runner.mode}")
    print(f"image: {runner.image}")
    print(f"php: {runner.php_version()}")
    for name, version in tool_versions(runner).items():
        print(f"{name}: {version}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="bench", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list cases")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_validate = sub.add_parser("validate", help="check every case against the contract")
    p_validate.set_defaults(func=cmd_validate)

    p_run = sub.add_parser("run", help="run cases through the analyzers")
    p_run.add_argument("--case", action="append", help="case id (repeatable)")
    p_run.add_argument("--domain", help="only cases in this domain")
    p_run.add_argument("--tool", action="append", help="only these tools (repeatable)")
    p_run.add_argument("--php", help="PHP version for the docker image, e.g. 8.4")
    p_run.add_argument("--php-version", help="the PHP version the runner actually uses")
    p_run.add_argument("--jobs", type=int, default=int(os.environ.get("BENCH_JOBS", "1")))
    p_run.add_argument("--label", default="", help="suffix for the run directory")
    p_run.add_argument("--shard", help="run only one slice of the corpus, as i/n")
    p_run.add_argument("--no-save", action="store_true", help="do not write artifacts")
    p_run.set_defaults(func=cmd_run)

    p_show = sub.add_parser("show", help="print a report file")
    p_show.add_argument("path")
    p_show.set_defaults(func=cmd_show)

    p_gaps = sub.add_parser("gaps", help="per-tool work list from a report")
    p_gaps.add_argument("--report", default="results/latest/report.json")
    p_gaps.add_argument("--tool")
    p_gaps.set_defaults(func=cmd_gaps)

    p_doctor = sub.add_parser("doctor", help="report the execution environment")
    p_doctor.add_argument("--php")
    p_doctor.set_defaults(func=cmd_doctor)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
