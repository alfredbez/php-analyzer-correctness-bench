# The autonomous factory

`bench_factory.py` grows the corpus without a human in the loop. One round:

1. **Pick** the domain with the largest deficit against its target and pair it
   with the source material for that domain (`factory/SOURCES.md`).
2. **Implement** - a session on one free model authors cases, proves their ground
   truth, runs them and commits. Implementers never review their own work.
3. **Review** - a session on a *different* model audits the new cases: is the
   stated basis real, did anything get widened, do the recorded verdicts
   reproduce? The reviewer is read-only and writes an explicit acceptance or
   rejection receipt tied to the exact base, candidate commit, and case list.
   Rejection or a failed review blocks publication.
4. **Gate** - `validate` must pass, the whole corpus must run, and no case may
   end in `tool_error` or `case_error`. The report audit must pass and cover every
   case with all three tools. The coordinator commits the measurement and review
   receipt before pushing to `main`. Analyzer FP and FN findings do not block it.

```
python3 factory/bench_factory.py status      # corpus size, rounds, parked models
python3 factory/bench_factory.py dry-run     # what the next round would do
python3 factory/bench_factory.py round       # do one round
python3 factory/bench_factory.py prepare     # create the worktree and install the analyzers
```

State lives in `factory/evidence/STATE.json`, logs in `factory/evidence/`, and
prompts in `factory/prompts/`. These directories are local and ignored by Git.
Each published snapshot includes `review.json` with the accepted candidate and
both model names. `dry-run` neither writes state nor changes the worktree.

The factory works in its own git worktree (`/home/abez/projects/php-analyzer-bench-worktrees/factory`)
on branch `factory/auto` and pushes to `main` only after the gate. An interactive
session can therefore work in the main checkout at the same time without either
side stepping on the other's files.

Workers may only add complete case directories in the assigned domain. Edits to
existing cases, pins, or shared code block publication. Failed workers and
rejected candidates are moved intact to timestamped quarantine worktrees and
branches. Their paths are recorded in state. The next round starts from a fresh
`origin/main`; it cannot publish or combine a rejected author's changes.
Only one round can run at a time. Worker timeouts kill the process group.

Targets are fixed in `TARGETS` and total 120 semantic criteria across 14 domains.
Variants sharing `criterion_id` do not increase coverage. An independent reviewer
must check novelty as well as correctness. The factory stops growing when all
domain targets are met; it never silently raises its own target.

The October 24 pilot does not enable the timer or raise those targets. Alfred
subsequently approved integrating and pushing the reviewed work to this
benchmark's `main`, not unattended operation. The existing `round` command can
push to `main`; do not invoke it as a local-only validation command.

`python3 factory/catalog.py build` inventories pinned Psalm datasets, PHPStan
fixtures and historical Mago probes. Its initial 120 candidates are unreviewed
leads, not 120 finished criteria or confirmed defects. Rounds select unused
candidates for their domain and record `source_candidate_id` in new manifests.
Rejected leads are not silently retried; domains can also use the broader source
checkouts when the initial inventory is exhausted. Extraction is not semantic
review, and no claim is made that the entire upstream suites were reviewed.

## Expand the source inventory locally

Use separate output paths until every new outcome has been reviewed:

```
python3 factory/catalog.py expand --limit-per-family 40 \
  --out results/harvest/my-batch/catalog.json \
  --assessment-out results/harvest/my-batch/assessment.json
python3 factory/catalog.py check \
  --inventory results/harvest/my-batch/catalog.json \
  --assessment results/harvest/my-batch/assessment.json
```

`expand` preserves existing records and appends fresh public Psalm and PHPStan
leads. It excludes prior IDs and probe hashes, records source revisions, and
creates `pending` assessments. The second command deliberately fails until all
pending leads have a supported outcome. Existing `assess --receipts` accepts
complete receipts for the resulting inventory, not just the additions.
Without output overrides, expansion updates the input pair in place. These two
writes are not transactional; do not run concurrent writers against that pair.

The October 24 harvest snapshot contains 80 additional unreviewed leads, 40 from
each public source. These are not 80 new criteria or confirmed defects. Only two
independently reduced new criteria enter the main catalog, bringing it to 122
assessed leads and 144 executable cases covering 129 declared criteria.
Terminal assessments, including covered, deferred and disabled leads, are no
longer eligible for automatic reselection. `pending` remains eligible within the
unchanged domain targets.

## Experimental Pzoom lane

Pzoom is opt-in. It is not part of the three-tool publication gate or the public
comparison. Build its pinned source with Rust and Cargo on PATH:

```
python3 tools/install-pzoom.py --jobs 2
python3 harness/bench.py run --php 8.4 --tool pzoom \
  --case assignability/catalog-psalm-2ed1be42908ccc536dd5 \
  --output results/runs/my-pzoom-experiment
```

The build uses the checked-in Cargo lock and records the source commit, compiler,
lock hash and binary hash. Pzoom has no working `--version` probe at this pin;
the harness verifies the receipt against the selected binary instead.
`BENCH_TOOL_PZOOM` overrides also require a matching adjacent provenance receipt.
Cases without an explicit Pzoom expectation keep observations outside the score
as `skipped`, never as an invented by-design divergence. Scan failures still
produce `tool_error`, even on unreviewed cases.

The pinned revision is currently blocked by an invalid `-096` literal in its
mandatory embedded `stubs/extensions/sockets.phpstub`. Disabling optional
extensions cannot disable that stub. The adapter rejects these partial runs,
including the two pilot cases. The exposed `--format json` flag is unused in
this revision, so the adapter validates the console report's counts and footer.
Explicit `analyze` targets prevent diagnostics from runtime control files.
No upstream sources were patched, and no support request or issue was sent.
See `docs/local-pilot-2026-10-24.md` for evidence and remaining decisions.

## What the factory must never do

* Open a pull request - on this repository or any other. Mago is frozen for new
  pull requests (`~/.config/software-factory/pr-freeze.json`) and this repository
  exists to measure, not to send.
* Widen an expectation so that a round ends green.
* Promote a round that did not run the corpus.
* Touch `tools/versions.json`. Moving a pin is a human decision.

## Model routing

Free models only, alternating families between the two lanes so that an
implementer and its reviewer do not share blind spots:

| lane | models, in order |
| --- | --- |
| implementer | `opencode/deepseek-v4.1-flash-free`, `opencode/space-bunny-free`, `opencode/glm-5.3-flash-free` |
| reviewer | `opencode/glm-5.3-flash-free`, `opencode/mimo-v2.6-flash-free`, `opencode/longcat-2.5-preview-free` |

A rate limit parks the model for an hour and the next candidate takes over. The
parking is visible in `status`, because a factory that silently stops producing
looks the same as a factory that has nothing to do.

## Timer

`factory/bench-factory.service` and `.timer` start a round 30 minutes after the
previous round finishes, and 10 minutes after boot. Install:

```
cp factory/bench-factory.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now bench-factory.timer
```

Each batch adds at most two cases. Each worker gets 30 minutes; the service
allows five hours for all model fallbacks, setup, and a full corpus run.
Unavailable model routes produce a failed round, not an accepted review. The
timer retries later, subject to model cooldowns. Inspect `status` and the journal
to distinguish quota blocks from quarantined candidates that require inspection.
