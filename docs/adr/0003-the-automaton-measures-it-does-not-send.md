# 0003 - The automaton measures, it does not send

Date: 2026-10-17
Status: accepted

## Context

The corpus was seeded by an agent that read Psalm's test suite, ran the patterns
through Mago and opened pull requests for the differences. That produced useful
findings and an unmanageable review load for the maintainer, who then asked for a
hold-off on new pull requests (recorded in
`~/.config/software-factory/pr-freeze.json`, enforced by a host-level `gh`
wrapper and audited every 30 minutes).

An autonomous loop that keeps finding things needs somewhere to put them that is
not somebody else's review queue.

## Decision

This repository is the destination. The factory writes cases, verdicts and
citations into a private repository, and never opens, replaces or splits a pull
request anywhere. Review load moves from the maintainer to the repository's own
reviewer lane: a second model, on a different family, audits every batch before
it is promoted.

Divergences and defects are published as a matrix and a per-tool work list that a
maintainer can read when they choose to.

## Consequences

* Findings accumulate without consuming maintainer attention.
* The repository must be self-explanatory without a human in the loop: contract,
  methodology and citations in tree, raw evidence next to each run.
* If a maintainer ever wants the cases, they can be handed over as data. That is
  a decision for a human, not for the loop.
