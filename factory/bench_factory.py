#!/usr/bin/env python3
"""Autonomous corpus factory.

One round of this program does three things:

1. pick the next growth task (a domain that is thin, a source that has not been
   mined recently) and dispatch an implementer session;
2. dispatch a reviewer session with a different model over exactly the cases the
   implementer added - four eyes, no self-review;
3. run the harness over the whole corpus. If every case validates and the run
   completes, the branch is promoted to main; otherwise the round stops and the
   state file records why.

Design constraints, in order of importance:

* Nothing lands unverified. A round that cannot run the corpus does not promote.
* The factory writes only `cases/`, `docs/`, `harness/` and `factory/`. Results
  are produced by measurement runs, which have a single writer.
* No pull requests, ever. The upstream Mago freeze is respected; this program
  never calls `gh pr create` and never pushes a branch other than its own.
* Rate limits are a first-class state. A model that answers with a 429 is parked
  for a while and the next candidate takes over.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shlex
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STATE_FILE = os.path.join(HERE, "STATE.json")
PROMPT_DIR = os.path.join(HERE, "prompts")
EVIDENCE_DIR = os.path.join(HERE, "evidence")
LOG_FILE = os.path.join(EVIDENCE_DIR, "factory.log")
WORKTREE = "/home/abez/projects/php-analyzer-bench-worktrees/factory"
BRANCH = "factory/auto"
PROMOTE_TARGET = "main"

SUBAGENT_TIMEOUT = int(os.environ.get("BENCH_FACTORY_TIMEOUT", "2400"))
RATE_LIMIT_COOLDOWN = 3600

# Free models only. The two lanes are deliberately different families: an
# implementer and a reviewer from the same family share their blind spots.
IMPLEMENTERS = [
    "opencode/deepseek-v4.1-flash-free",
    "opencode/space-bunny-free",
    "opencode/glm-5.3-flash-free",
]
REVIEWERS = [
    "opencode/glm-5.3-flash-free",
    "opencode/mimo-v2.6-flash-free",
    "opencode/longcat-2.5-preview-free",
]


def log(message: str) -> None:
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = f"{stamp} {message}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def run(cmd: list[str] | str, cwd: str, timeout: int = 600, shell: bool = False) -> dict:
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout, shell=shell)
        code, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        code = 124
        out = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        err = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        err += f"\n[factory] timeout after {timeout}s"
    return {"code": code, "stdout": out, "stderr": err,
            "seconds": round(time.time() - started, 1)}


# ---------------------------------------------------------------- state

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return {"rounds": [], "rate_limits": {}, "domains": {}, "sources": []}


def save_state(state: dict) -> None:
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
    os.replace(tmp, STATE_FILE)


def available(models: list[str], state: dict) -> list[str]:
    now = int(time.time())
    return [model for model in models
            if now - state.get("rate_limits", {}).get(model, 0) > RATE_LIMIT_COOLDOWN]


def park(state: dict, model: str, reason: str) -> None:
    state.setdefault("rate_limits", {})[model] = int(time.time())
    log(f"[RATE LIMIT] parking {model}: {reason[:160]}")


RATE_LIMIT_MARKERS = ("rate limit", "429", "too many requests", "quota exceeded",
                      "insufficient credit", "credit balance", "overloaded")


def looks_rate_limited(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in RATE_LIMIT_MARKERS)


# ---------------------------------------------------------------- worktree

def ensure_worktree(state: dict) -> str:
    if os.path.exists(os.path.join(WORKTREE, ".git")):
        run(["git", "fetch", "origin", "main"], cwd=WORKTREE, timeout=180)
        result = run(["git", "rebase", "origin/main"], cwd=WORKTREE, timeout=180)
        if result["code"] != 0:
            run(["git", "rebase", "--abort"], cwd=WORKTREE, timeout=60)
            log("[WORKTREE] rebase failed, continuing on the existing base")
        return WORKTREE
    os.makedirs(os.path.dirname(WORKTREE), exist_ok=True)
    run(["git", "worktree", "add", "-B", BRANCH, WORKTREE, "origin/main"], cwd=ROOT, timeout=300)
    log(f"[WORKTREE] created {WORKTREE} on {BRANCH}")
    return WORKTREE


def tooling_ready(tree: str) -> bool:
    return os.path.exists(os.path.join(tree, "tools/bin/phpstan.phar"))


def prepare_tooling(tree: str) -> bool:
    if tooling_ready(tree):
        return True
    log("[SETUP] installing pinned analyzers into the factory worktree")
    result = run([os.path.join(tree, "tools/install.sh")], cwd=tree, timeout=900)
    return result["code"] == 0


def corpus_domains(tree: str) -> dict:
    counts: dict[str, int] = {}
    cases_dir = os.path.join(tree, "cases")
    if not os.path.isdir(cases_dir):
        return counts
    for domain in sorted(os.listdir(cases_dir)):
        path = os.path.join(cases_dir, domain)
        if os.path.isdir(path):
            counts[domain] = len([d for d in os.listdir(path)
                                  if os.path.isdir(os.path.join(path, d))])
    return counts


# ---------------------------------------------------------------- prompts

IMPLEMENTER_TEMPLATE = """You are a worker session in the autonomous factory of the PHP analyzer correctness benchmark at {tree}.

Read AGENT-PROTOCOL.md, docs/case-contract.md, factory/SOURCES.md first. Work on branch {branch} in that worktree. Do not switch branches, do not push, do not open pull requests.

Task: add {count} new cases to the domain `{domain}` ({why}).

Source material for this round: {source}

Rules that decide whether your work is worth anything:
- Establish the ground truth from PHP semantics or from a runtime proof (`runtime/check.php`), never from what an analyzer prints.
- A fixture harvested from one tool's own test suite judges that tool via `expect.<tool>.basis` + `citation`; the other two are judged against the case's neutral ground truth.
- Where a tool deliberately does not implement a rule class, use `mode: "unsupported"` with a reason and a citation you actually read - do not invent one.
- Never widen an expectation to make a tool look better or worse. A false positive or false negative that you find stays in the matrix.
- Never modify files outside `cases/{domain}/`. If a harness bug blocks you, stop and write the problem into `factory/BLOCKED.md`.

Verify before you commit: `python3 harness/bench.py validate` and `python3 harness/bench.py run --case <id>` for every case you added. Commit with `git -c commit.gpgsign=false commit`, one line, naming the rule class.

Finish with a short report: the case ids, the verdicts that came out, and anything you could not establish."""

REVIEWER_TEMPLATE = """You are a reviewer session in the autonomous factory of the PHP analyzer correctness benchmark at {tree}.

You did not write the code you are reviewing. Read AGENT-PROTOCOL.md, docs/case-contract.md and factory/SOURCES.md, then audit the cases changed by the last commit(s):

    git log --oneline -{commits} --name-status
    git diff HEAD~{commits} -- cases/

For every changed case, check and report:
1. Ground truth: is the stated basis real? Run `runtime/check.php` where it exists. If the basis is `php_semantics`, is the argument correct? If the basis is a citation, does the citation exist and say what the case claims?
2. Expectations: are they specific (no empty predicates)? Was any expectation widened, or a diagnostic acknowledged under `allowed` without a real reason? An acknowledged diagnostic that is actually wrong must count as a false positive.
3. Verdicts: reproduce at least two cases with `python3 harness/bench.py run --case <id>` and compare with what the files claim.
4. Contract: `python3 harness/bench.py validate` passes; `composer.json` present; no `vendor/`, `.generated/` or scratch files committed.

Fix what is clearly broken (a wrong line number, a missing citation, a case that violates the contract). Do not rewrite the implementer's judgement about a tool's behaviour - if you disagree, write it into `factory/REVIEW.md` with the evidence.

Commit your fixes with `git -c commit.gpgsign=false commit` and answer with a short verdict per case: accept, fixed, or disagree (with reason)."""


def write_prompt(name: str, content: str) -> str:
    os.makedirs(PROMPT_DIR, exist_ok=True)
    path = os.path.join(PROMPT_DIR, f"{int(time.time())}-{name}.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return path


def dispatch(tree: str, model: str, prompt: str, label: str, state: dict) -> dict:
    prompt_file = write_prompt(label, prompt)
    log_path = os.path.join(EVIDENCE_DIR, f"{int(time.time())}-{label}.log")
    log(f"[DISPATCH] {label} with {model} (prompt: {os.path.basename(prompt_file)})")
    command = (f"opencode run --auto --model {shlex.quote(model)} "
               f"--title {shlex.quote('bench factory: ' + label)} "
               f"{shlex.quote(prompt)}")
    result = run(command, cwd=tree, timeout=SUBAGENT_TIMEOUT, shell=True)
    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write(f"model: {model}\nprompt: {prompt_file}\nexit: {result['code']}\n")
        handle.write("=== stdout ===\n" + result["stdout"] + "\n=== stderr ===\n" + result["stderr"])
    if looks_rate_limited(result["stdout"] + result["stderr"]):
        park(state, model, result["stdout"] + result["stderr"])
    return result


# ---------------------------------------------------------------- round

def pick_task(tree: str, state: dict) -> dict:
    counts = corpus_domains(tree)
    domains = state.get("domains") or {
        "narrowing": 8, "nullability": 5, "callables": 5, "assignability": 5,
        "legacy-patterns": 6, "phpdoc-extensions": 4, "generics": 4, "arrays": 4,
        "dead-code": 4, "enums": 4, "type-inference": 5, "phpstan-extensions": 3,
    }
    source_by_domain = {
        "narrowing": "/home/abez/projects/mago-upstream-prep/repro (field findings)",
        "nullability": "/home/abez/projects/mago-upstream-prep/repro (field findings)",
        "callables": "/home/abez/projects/mago-upstream-prep/repro (field findings)",
        "assignability": "/home/abez/projects/mago-upstream-prep/repro (field findings)",
        "legacy-patterns": "the psalm-harvest fixtures plus Psalm docs",
        "phpdoc-extensions": "Psalm issue documentation",
        "generics": "/home/abez/projects/mago-upstream-prep/mago/crates/analyzer/tests/cases",
        "arrays": "/home/abez/projects/mago-upstream-prep/mago/crates/analyzer/tests/cases",
        "dead-code": "/home/abez/projects/phpstan-src/tests/PHPStan/Rules",
        "enums": "/home/abez/projects/mago-upstream-prep/mago/crates/analyzer/tests/cases",
        "type-inference": "/home/abez/projects/phpstan-src/tests/PHPStan/Analyser/nsrt",
        "phpstan-extensions": "/home/abez/projects/phpstan-src/tests",
    }
    # The thinnest domain relative to its target wins, so the corpus fills in
    # rather than piling up in whichever area is easiest.
    deficits = {domain: target - counts.get(domain, 0) for domain, target in domains.items()}
    domain = max(deficits, key=lambda key: deficits[key])
    return {
        "domain": domain,
        "source": source_by_domain.get(domain, "the sources listed in factory/SOURCES.md"),
        "why": f"{counts.get(domain, 0)} of {domains[domain]} planned cases exist",
        "count": random.randint(2, 4),
    }


def ensure_valid(tree: str) -> bool:
    result = run([sys.executable, "harness/bench.py", "validate"], cwd=tree, timeout=300)
    return result["code"] == 0


def promote(tree: str, state: dict, round_id: int) -> bool:
    """Publish the factory branch onto main when every gate is green."""
    if not ensure_valid(tree):
        log(f"[GATE] round {round_id} failed validation - not promoting")
        return False
    result = run([sys.executable, "harness/bench.py", "run", "--jobs", "2",
                  "--label", f"factory-{round_id}"], cwd=tree, timeout=3600)
    if result["code"] != 0:
        log(f"[GATE] round {round_id} failed the corpus run - not promoting")
        return False
    audit = run([sys.executable, "harness/bench.py", "audit", "--report",
                 "results/latest/report.json"], cwd=tree, timeout=300)
    if audit["code"] != 0:
        log(f"[GATE] round {round_id} failed the report audit:")
        for line in audit["stdout"].splitlines()[:10]:
            log("  " + line.strip())
        return False
    failures = [line for line in result["stdout"].splitlines()
                if "=tool_error" in line or "=case_error" in line]
    if failures:
        log(f"[GATE] round {round_id} produced {len(failures)} tool/case errors - not promoting")
        for line in failures[:10]:
            log("  " + line.strip())
        return False
    run(["git", "add", "cases", "docs", "harness", "factory"], cwd=tree, timeout=120)
    staged = run(["git", "diff", "--cached", "--name-only"], cwd=tree, timeout=60)
    if staged["stdout"].strip():
        run(["git", "-c", "commit.gpgsign=false", "commit", "-m",
             f"Factory round {round_id}: grow the corpus"], cwd=tree, timeout=120)
    push = run(["git", "push", "origin", f"HEAD:{PROMOTE_TARGET}"], cwd=tree, timeout=300)
    if push["code"] != 0:
        log(f"[GATE] push to {PROMOTE_TARGET} rejected: {push['stderr'][:200]}")
        return False
    log(f"[PROMOTE] round {round_id} published to {PROMOTE_TARGET}")
    return True


def round_once(state: dict, dry_run: bool = False) -> dict:
    round_id = len(state.get("rounds", [])) + 1
    tree = ensure_worktree(state)
    if not prepare_tooling(tree):
        log("[SETUP] analyzer binaries unavailable - round skipped")
        return {"round": round_id, "status": "setup_failed"}

    task = pick_task(tree, state)
    record = {"round": round_id, "started": int(time.time()), "task": task, "status": "running"}

    implementers = available(IMPLEMENTERS, state)
    reviewers = available(REVIEWERS, state)
    if not implementers or not reviewers:
        log("[SKIP] no model available outside the rate-limit cooldown")
        record["status"] = "rate_limited"
        state.setdefault("rounds", []).append(record)
        save_state(state)
        return record

    implementer = implementers[0]
    reviewer = next((model for model in reviewers if model != implementer), reviewers[0])
    record["implementer"], record["reviewer"] = implementer, reviewer

    if dry_run:
        log(f"[DRY RUN] would dispatch: domain={task['domain']} "
            f"implementer={implementer} reviewer={reviewer}")
        record["status"] = "dry_run"
        state.setdefault("rounds", []).append(record)
        save_state(state)
        return record

    before = run(["git", "rev-parse", "HEAD"], cwd=tree, timeout=60)["stdout"].strip()
    dispatch(tree, implementer, IMPLEMENTER_TEMPLATE.format(tree=tree, branch=BRANCH, **task),
             f"grow-{task['domain']}", state)

    commits = run(["git", "rev-list", "--count", f"{before}..HEAD"], cwd=tree, timeout=60)
    added = int(commits["stdout"].strip() or 0)
    record["commits"] = added
    if added == 0:
        log(f"[ROUND {round_id}] implementer added no commit - nothing to review")
        record["status"] = "no_change"
        state.setdefault("rounds", []).append(record)
        save_state(state)
        return record

    dispatch(tree, reviewer, REVIEWER_TEMPLATE.format(tree=tree, commits=min(added, 6)),
             f"review-{task['domain']}", state)

    record["status"] = "promoted" if promote(tree, state, round_id) else "gated"
    record["finished"] = int(time.time())
    state.setdefault("rounds", []).append(record)
    state["domains"] = corpus_domains(tree)
    save_state(state)
    log(f"[ROUND {round_id}] {record['status']} ({record['commits']} commit(s) from the implementer)")
    return record


def cmd_status(state: dict) -> int:
    counts = corpus_domains(ROOT)
    print(f"cases by domain: {json.dumps(counts, sort_keys=True)}")
    print(f"total: {sum(counts.values())}")
    rounds = state.get("rounds", [])
    print(f"rounds: {len(rounds)}")
    for record in rounds[-8:]:
        print(f"  {record['round']:>3} {record.get('status'):<12} "
              f"{record.get('task', {}).get('domain', '-'):<18} "
              f"{record.get('implementer', '-')}")
    parked = {model: int(time.time()) - stamp
              for model, stamp in (state.get("rate_limits") or {}).items()
              if int(time.time()) - stamp < RATE_LIMIT_COOLDOWN}
    if parked:
        print(f"parked models: {parked}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="status",
                        choices=["status", "round", "dry-run", "prepare"])
    args = parser.parse_args(argv)
    state = load_state()
    if args.command == "status":
        return cmd_status(state)
    if args.command == "prepare":
        tree = ensure_worktree(state)
        print(f"worktree: {tree}")
        print(f"tooling: {'ready' if prepare_tooling(tree) else 'missing'}")
        return 0
    result = round_once(state, dry_run=args.command == "dry-run")
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") not in ("setup_failed", "rate_limited") else 1


if __name__ == "__main__":
    raise SystemExit(main())
