# The autonomous factory

`bench_factory.py` grows the corpus without a human in the loop. One round:

1. **Pick** the domain with the largest deficit against its target and pair it
   with the source material for that domain (`factory/SOURCES.md`).
2. **Implement** - a session on one free model authors cases, proves their ground
   truth, runs them and commits. Implementers never review their own work.
3. **Review** - a session on a *different* model audits the new cases: is the
   stated basis real, did anything get widened, do the recorded verdicts
   reproduce? It fixes contract violations and files disagreements in
   `factory/REVIEW.md`.
4. **Gate** - `validate` must pass, the whole corpus must run, and no case may
   end in `tool_error` or `case_error`. Only then is the branch pushed to `main`.

```
python3 factory/bench_factory.py status      # corpus size, rounds, parked models
python3 factory/bench_factory.py dry-run     # what the next round would do
python3 factory/bench_factory.py round       # do one round
python3 factory/bench_factory.py prepare     # create the worktree and install the analyzers
```

State lives in `factory/STATE.json`, logs in `factory/evidence/`, prompts in
`factory/prompts/`. All three are local; the log is the audit trail.

The factory works in its own git worktree (`/home/abez/projects/php-analyzer-bench-worktrees/factory`)
on branch `factory/auto` and pushes to `main` only after the gate. An interactive
session can therefore work in the main checkout at the same time without either
side stepping on the other's files.

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

`factory/bench-factory.service` + `.timer` run one round every 30 minutes,
persisted across reboots. Install:

```
cp factory/bench-factory.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now bench-factory.timer
```

The timer is intentionally slow. A round costs a model session and a full corpus
run; a faster cadence produces unread churn, which is exactly the failure mode
that made the upstream pull requests unwelcome in the first place.
