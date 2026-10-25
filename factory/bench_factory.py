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
* Workers add new cases only. A read-only reviewer must accept the exact head.
  The coordinator commits the full measurement before publishing.
* No pull requests, ever. The upstream Mago freeze is respected; this program
  never calls `gh pr create` and publishes only to this repository's origin/main.
* Rate limits are a first-class state. A model that answers with a 429 is parked
  for a while and the next candidate takes over.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROMPT_DIR = os.path.join(HERE, "prompts")
EVIDENCE_DIR = os.path.join(HERE, "evidence")
STATE_FILE = os.path.join(EVIDENCE_DIR, "STATE.json")
LOG_FILE = os.path.join(EVIDENCE_DIR, "factory.log")
WORKTREE = "/home/abez/projects/php-analyzer-bench-worktrees/factory"
BRANCH = "factory/auto"
PROMOTE_TARGET = "main"

SUBAGENT_TIMEOUT = int(os.environ.get("BENCH_FACTORY_TIMEOUT", "1800"))
RATE_LIMIT_COOLDOWN = 3600
TARGETS = {
    "narrowing": 12, "nullability": 8, "callables": 10, "assignability": 8,
    "legacy-patterns": 10, "phpdoc-extensions": 4, "generics": 12, "arrays": 14,
    "dead-code": 6, "enums": 6, "type-inference": 10, "phpstan-extensions": 4,
    "exceptions": 6, "objects": 10,
}

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


def run(cmd: list[str], cwd: str, timeout: int = 600) -> dict:
    started = time.time()
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
        code = proc.returncode
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        out, err = proc.communicate()
        code = 124
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
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
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


RATE_LIMIT_MARKERS = ("rate limit", "too many requests", "quota exceeded",
                      "insufficient credit", "credit balance", "overloaded")


def looks_rate_limited(text: str) -> bool:
    lowered = text.lower()
    return (any(marker in lowered for marker in RATE_LIMIT_MARKERS)
            or re.search(r"\b(?:http(?:/\d(?:\.\d)?)?|error|status(?: code)?)\s*[:=]?\s*429\b",
                         lowered) is not None)


# ---------------------------------------------------------------- worktree

def unfinished_files(tree: str) -> list[str]:
    tracked = run(["git", "diff", "--name-only", "HEAD"], cwd=tree)
    untracked = run(["git", "ls-files", "--others", "--exclude-standard"], cwd=tree)
    if tracked["code"] or untracked["code"]:
        raise RuntimeError("cannot inspect factory worktree")
    return [path for path in (tracked["stdout"] + untracked["stdout"]).splitlines()
            if not path.startswith("results/runs/")]


def ensure_worktree(state: dict) -> str:
    if os.path.exists(os.path.join(WORKTREE, ".git")):
        branch = run(["git", "branch", "--show-current"], cwd=WORKTREE)["stdout"].strip()
        if branch != BRANCH:
            raise RuntimeError(f"factory worktree is on unexpected branch {branch!r}")
        if run(["git", "fetch", "origin", "main"], cwd=WORKTREE, timeout=180)["code"]:
            raise RuntimeError("cannot fetch origin/main")
        ahead = run(["git", "rev-list", "--count", "origin/main..HEAD"], cwd=WORKTREE)
        if ahead["code"]:
            raise RuntimeError("cannot inspect unpublished factory commits")
        if unfinished_files(WORKTREE) or ahead["stdout"].strip() != "0":
            stamp = str(time.time_ns())
            preserved_branch = f"{BRANCH}-quarantined-{stamp}"
            preserved_path = f"{WORKTREE}-quarantined-{stamp}"
            if run(["git", "branch", "-m", preserved_branch], cwd=WORKTREE)["code"]:
                raise RuntimeError("cannot preserve the unfinished factory branch")
            moved = run(["git", "worktree", "move", WORKTREE, preserved_path], cwd=ROOT)
            if moved["code"]:
                raise RuntimeError(f"cannot move unfinished worktree; files remain at {WORKTREE}")
            state.setdefault("quarantines", []).append({"path": preserved_path,
                                                       "branch": preserved_branch})
            save_state(state)
            log(f"[QUARANTINE] preserved failed candidate at {preserved_path}")
        else:
            if run(["git", "merge", "--ff-only", "origin/main"], cwd=WORKTREE)["code"]:
                raise RuntimeError("cannot fast-forward the factory worktree")
            return WORKTREE
    os.makedirs(os.path.dirname(WORKTREE), exist_ok=True)
    result = run(["git", "worktree", "add", "-b", BRANCH, WORKTREE, "origin/main"], cwd=ROOT, timeout=300)
    if result["code"]:
        raise RuntimeError(f"cannot create factory worktree: {result['stderr'][:200]}")
    log(f"[WORKTREE] created {WORKTREE} on {BRANCH}")
    return WORKTREE


def tooling_ready(tree: str) -> bool:
    binaries_ready = all(os.path.exists(os.path.join(tree, "tools/bin", name))
                         for name in ("phpstan.phar", "psalm.phar", "mago"))
    return binaries_ready and all(
        (manifest.parent / "vendor/autoload.php").is_file()
        for manifest in Path(tree, "cases").glob("*/*/case.json")
        if json.loads(manifest.read_text()).get("composer", {}).get("install"))


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
            criteria = set()
            for slug in os.listdir(path):
                manifest = os.path.join(path, slug, "case.json")
                if os.path.isfile(manifest):
                    with open(manifest, encoding="utf-8") as handle:
                        data = json.load(handle)
                    criteria.add(data.get("criterion_id", data.get("id", f"{domain}/{slug}")))
            counts[domain] = len(criteria)
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
- Add new case directories only under `cases/{domain}/`. Do not modify existing cases or any other tracked file. If a harness bug blocks you, stop and report it in your final response.
- Add genuinely different semantic criteria, not parameter variants of existing cases. Inspect that domain first. Set `criterion_id` to a stable `<domain>/<semantic-rule>`; variants of the same rule share it and do not increase coverage.
- If the source material lists catalogue candidate IDs, record one in each new manifest as `source_candidate_id`, retaining its immutable source citation. Rewrite minimal examples; do not copy upstream test bodies.

Verify before you commit: `python3 harness/bench.py validate` and `python3 harness/bench.py run --case <id>` for every case you added. Commit with `git -c commit.gpgsign=false commit`, one line, naming the rule class.

Finish with a short report: the case ids, the verdicts that came out, and anything you could not establish."""

REVIEWER_TEMPLATE = """You are a reviewer session in the autonomous factory of the PHP analyzer correctness benchmark at {tree}.

You did not write the code you are reviewing. Read AGENT-PROTOCOL.md, docs/case-contract.md and factory/SOURCES.md, then audit the entire candidate:

    git diff {base}..{head} -- cases/

Review exactly these case ids: {cases}

For every changed case, check and report:
1. Ground truth: is the stated basis real? Run `runtime/check.php` where it exists. If the basis is `php_semantics`, is the argument correct? If the basis is a citation, does the citation exist and say what the case claims?
2. Expectations: are they specific (no empty predicates)? Was any expectation widened, or a diagnostic acknowledged under `allowed` without a real reason? An acknowledged diagnostic that is actually wrong must count as a false positive.
3. Verdicts: reproduce at least two cases with `python3 harness/bench.py run --case <id>` and compare with what the files claim.
4. Contract: `python3 harness/bench.py validate` passes; `composer.json` present; no `vendor/`, `.generated/` or scratch files committed.
5. Novelty: compare against the existing domain. Reject superficial variants, a duplicate semantic criterion, or an unsupported claim of enterprise relevance. A catalogue candidate is a lead, not an independent truth oracle.

Do not edit or commit any source file, switch branches, push, or launch other agents. Reject the batch if anything needs a correction or if a claim cannot be established.

Write your review as JSON to this exact receipt path: {receipt}
The object must contain `base` equal to "{base}", `head` equal to "{head}", `verdict` equal to "accept" or "reject", `cases` containing the exact case id list above, and `reason` explaining your verdict. Only accept when every case passes the review. A missing receipt or a rejected verdict blocks publication."""


def write_prompt(name: str, content: str) -> str:
    os.makedirs(PROMPT_DIR, exist_ok=True)
    path = os.path.join(PROMPT_DIR, f"{time.time_ns()}-{name}.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    return path


def dispatch(tree: str, model: str, prompt: str, label: str, state: dict) -> dict:
    prompt_file = write_prompt(label, prompt)
    log_path = os.path.join(EVIDENCE_DIR, f"{time.time_ns()}-{label}.log")
    log(f"[DISPATCH] {label} with {model} (prompt: {os.path.basename(prompt_file)})")
    command = ["opencode", "run", "--standalone", "--auto", "--model", model,
               "--title", "bench factory: " + label, prompt]
    result = run(command, cwd=tree, timeout=SUBAGENT_TIMEOUT)
    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write(f"model: {model}\nprompt: {prompt_file}\nexit: {result['code']}\n")
        handle.write("=== stdout ===\n" + result["stdout"] + "\n=== stderr ===\n" + result["stderr"])
    if looks_rate_limited(result["stdout"] + result["stderr"]):
        park(state, model, result["stdout"] + result["stderr"])
        result["code"] = result["code"] or 1
    return result


# ---------------------------------------------------------------- round

def pick_task(tree: str, state: dict) -> dict | None:
    counts = corpus_domains(tree)
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
    deficits = {domain: target - counts.get(domain, 0) for domain, target in TARGETS.items()
                if counts.get(domain, 0) < target}
    if not deficits:
        return None
    domain = max(deficits, key=lambda key: deficits[key])
    task = {
        "domain": domain,
        "source": source_by_domain.get(domain, "the sources listed in factory/SOURCES.md"),
        "why": f"{counts.get(domain, 0)} of {TARGETS[domain]} planned semantic criteria exist",
        "count": min(deficits[domain], 2),
    }
    catalog = os.path.join(tree, "factory/catalog.json")
    if os.path.isfile(catalog):
        used = set()
        assessment = os.path.join(tree, "factory/assessment.json")
        if os.path.isfile(assessment):
            with open(assessment, encoding="utf-8") as handle:
                used.update(entry['candidate_id'] for entry in json.load(handle)['entries']
                            if entry['status'] != 'pending')
        for previous in state.get("rounds", []):
            if previous.get("status") not in ("rate_limited", "setup_failed"):
                used.update(previous.get("task", {}).get("candidate_ids", []))
        for parent, _, files in os.walk(os.path.join(tree, "cases")):
            if "case.json" in files:
                with open(os.path.join(parent, "case.json"), encoding="utf-8") as handle:
                    used.add(json.load(handle).get("source_candidate_id"))
        with open(catalog, encoding="utf-8") as handle:
            candidates = [entry for entry in json.load(handle)["candidates"]
                          if entry["domain"] == domain and entry["id"] not in used
                          and 'SKIPPED-' not in entry.get("title", "")]
        if candidates:
            selected = candidates[:task["count"]]
            task["candidate_ids"] = [entry["id"] for entry in selected]
            task["source"] = json.dumps(selected, ensure_ascii=False)
            task["count"] = len(selected)
    return task


def ensure_valid(tree: str) -> bool:
    result = run([sys.executable, "harness/bench.py", "validate"], cwd=tree, timeout=300)
    return result["code"] == 0


def candidate_cases(tree: str, base: str, task: dict) -> list[str]:
    if unfinished_files(tree):
        raise RuntimeError("candidate has uncommitted changes outside measurement results")
    branch = run(["git", "branch", "--show-current"], cwd=tree)["stdout"].strip()
    if branch != BRANCH:
        raise RuntimeError("worker switched branches")
    changed = run(["git", "diff", "--no-renames", "--name-status", f"{base}..HEAD"], cwd=tree)
    if changed["code"]:
        raise RuntimeError("cannot inspect candidate diff")
    cases = set()
    manifests = set()
    for line in changed["stdout"].splitlines():
        status, path = line.split("\t", 1)
        parts = path.split("/")
        if (status != "A" or len(parts) < 4 or parts[:2] != ["cases", task["domain"]]
                or any(part in ("vendor", ".generated") for part in parts)):
            raise RuntimeError(f"worker changed a forbidden path: {status} {path}")
        case_id = "/".join(parts[1:3])
        existing = run(["git", "ls-tree", base, "--", "/".join(parts[:3])], cwd=tree)
        if existing["code"] or existing["stdout"].strip():
            raise RuntimeError(f"worker modified an existing case: {case_id}")
        cases.add(case_id)
        if parts[3:] == ["case.json"]:
            manifests.add(case_id)
        if os.path.islink(os.path.join(tree, path)):
            raise RuntimeError(f"candidate contains a symlink: {path}")
    if not cases or cases != manifests or len(cases) > task["count"]:
        raise RuntimeError("candidate must contain complete new cases within the round's count limit")
    new_criteria = set()
    for case_id in cases:
        with open(os.path.join(tree, "cases", case_id, "case.json"), encoding="utf-8") as handle:
            data = json.load(handle)
        if task.get("candidate_ids") and data.get("source_candidate_id") not in task["candidate_ids"]:
            raise RuntimeError("candidate must record the selected source_candidate_id")
        criterion = data.get("criterion_id", data.get("id", case_id))
        if criterion in new_criteria:
            raise RuntimeError("candidate batch repeats a semantic criterion")
        new_criteria.add(criterion)
    for parent, _, files in os.walk(os.path.join(tree, "cases")):
        case_id = os.path.relpath(parent, os.path.join(tree, "cases"))
        if "case.json" in files and case_id not in cases:
            with open(os.path.join(parent, "case.json"), encoding="utf-8") as handle:
                data = json.load(handle)
            if data.get("criterion_id", data.get("id", case_id)) in new_criteria:
                raise RuntimeError("candidate duplicates an existing semantic criterion")
    return sorted(cases)


def promote(tree: str, record: dict, review: dict) -> bool:
    """Publish the factory branch onto main when every gate is green."""
    round_id = record["round"]
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
    with open(os.path.join(tree, "results/latest/report.json"), encoding="utf-8") as handle:
        report = json.load(handle)
    expected = {f"{domain}/{slug}" for domain in corpus_domains(tree)
                for slug in os.listdir(os.path.join(tree, "cases", domain))
                if os.path.isfile(os.path.join(tree, "cases", domain, slug, "case.json"))}
    if (not report["meta"]["run_id"].endswith(f"-factory-{round_id}")
            or {row["case"] for row in report["cases"]} != expected
            or any(set(row["results"]) != {"phpstan", "psalm", "mago"}
                   for row in report["cases"])):
        log(f"[GATE] round {round_id} did not measure the complete corpus with all three tools")
        return False
    snapshot = os.path.join("results", "runs", report["meta"]["run_id"])
    with open(os.path.join(tree, snapshot, "review.json"), "w", encoding="utf-8") as handle:
        json.dump({**review, "implementer": record["implementer"],
                   "reviewer": record["reviewer"]}, handle, indent=2)
        handle.write("\n")
    if run(["git", "add", "--", snapshot], cwd=tree)["code"]:
        return False
    commit = run(["git", "-c", "commit.gpgsign=false", "commit", "-m",
                  f"Record verified factory round {round_id}"], cwd=tree, timeout=120)
    if commit["code"]:
        return False
    push = run(["git", "push", "origin", f"HEAD:{PROMOTE_TARGET}"], cwd=tree, timeout=300)
    if push["code"] != 0:
        log(f"[GATE] push to {PROMOTE_TARGET} rejected: {push['stderr'][:200]}")
        return False
    log(f"[PROMOTE] round {round_id} published to {PROMOTE_TARGET}")
    return True


def finish_round(state: dict, record: dict, status: str, detail: str = "") -> dict:
    record.update(status=status, detail=detail, finished=int(time.time()))
    state.setdefault("rounds", []).append(record)
    save_state(state)
    log(f"[ROUND {record['round']}] {status}: {detail}")
    return record


def round_once(state: dict, dry_run: bool = False) -> dict:
    round_id = len(state.get("rounds", [])) + 1
    record = {"round": round_id, "started": int(time.time())}
    if dry_run:
        record["task"] = pick_task(ROOT, state)
        record["implementers"] = available(IMPLEMENTERS, state)
        record["reviewers"] = available(REVIEWERS, state)
        record["status"] = "dry_run"
        return record
    try:
        tree = ensure_worktree(state)
        task = pick_task(tree, state)
        if not task:
            return finish_round(state, record, "complete", "all domain targets reached")
        record["task"] = task
        implementers = available(IMPLEMENTERS, state)
        reviewers = available(REVIEWERS, state)
        if not implementers or not reviewers:
            return finish_round(state, record, "rate_limited", "no model pair outside cooldown")
        if not prepare_tooling(tree):
            return finish_round(state, record, "setup_failed", "analyzer binaries unavailable")
        before = run(["git", "rev-parse", "HEAD"], cwd=tree)["stdout"].strip()
        record["base"] = before
        for implementer in implementers:
            result = dispatch(tree, implementer,
                              IMPLEMENTER_TEMPLATE.format(tree=tree, branch=BRANCH, **task),
                              f"grow-{task['domain']}", state)
            if result["code"] == 0:
                record["implementer"] = implementer
                break
            if (unfinished_files(tree)
                    or run(["git", "rev-parse", "HEAD"], cwd=tree)["stdout"].strip() != before):
                raise RuntimeError("failed implementer left changes; preserving them instead of reusing them")
        else:
            return finish_round(state, record, "implementation_failed", "all implementers failed")

        cases = candidate_cases(tree, before, task)
        head = run(["git", "rev-parse", "HEAD"], cwd=tree)["stdout"].strip()
        record.update(head=head, cases=cases)
        for index, reviewer in enumerate(reviewers):
            if reviewer.split("/")[-1].split("-")[0] == implementer.split("/")[-1].split("-")[0]:
                continue
            receipt = os.path.join(EVIDENCE_DIR, f"review-{round_id}-{time.time_ns()}-{index}.json")
            result = dispatch(tree, reviewer, REVIEWER_TEMPLATE.format(
                tree=tree, base=before, head=head, cases=json.dumps(cases), receipt=receipt),
                f"review-{task['domain']}", state)
            if result["code"] or not os.path.isfile(receipt):
                continue
            try:
                with open(receipt, encoding="utf-8") as handle:
                    review = json.load(handle)
            except (OSError, ValueError):
                continue
            if (not isinstance(review, dict)
                    or review.get("base") != before or review.get("head") != head
                    or review.get("cases") != cases
                    or not isinstance(review.get("reason"), str) or not review["reason"].strip()):
                continue
            record.update(reviewer=reviewer, receipt=receipt)
            if review.get("verdict") == "reject":
                return finish_round(state, record, "rejected", review["reason"])
            if review.get("verdict") != "accept":
                continue
            if (candidate_cases(tree, before, task) != cases
                    or run(["git", "rev-parse", "HEAD"], cwd=tree)["stdout"].strip() != head):
                raise RuntimeError("reviewer changed the candidate it was asked to review")
            status = "promoted" if promote(tree, record, review) else "gated"
            return finish_round(state, record, status, review["reason"])
        return finish_round(state, record, "review_failed", "no valid independent acceptance receipt")
    except (RuntimeError, OSError, ValueError) as exc:
        return finish_round(state, record, "blocked", str(exc))


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
    if args.command == "status":
        return cmd_status(load_state())
    if args.command == "dry-run":
        print(json.dumps(round_once(load_state(), dry_run=True), indent=2))
        return 0
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    with open(os.path.join(EVIDENCE_DIR, "factory.lock"), "w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("another factory round is already running", file=sys.stderr)
            return 1
        state = load_state()
        if args.command == "prepare":
            tree = ensure_worktree(state)
            ready = prepare_tooling(tree)
            print(f"worktree: {tree}")
            print(f"tooling: {'ready' if ready else 'missing'}")
            return 0 if ready else 1
        result = round_once(state)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in ("promoted", "complete") else 1


if __name__ == "__main__":
    raise SystemExit(main())
