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

`python3 factory/catalog.py build` inventories pinned Psalm datasets, PHPStan
fixtures and historical Mago probes. Its initial 120 candidates are unreviewed
leads, not 120 finished criteria or confirmed defects. Rounds select unused
candidates for their domain and record `source_candidate_id` in new manifests.
Rejected leads are not silently retried; domains can also use the broader source
checkouts when the initial inventory is exhausted. Extraction is not semantic
review, and no claim is made that the entire upstream suites were reviewed.

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
