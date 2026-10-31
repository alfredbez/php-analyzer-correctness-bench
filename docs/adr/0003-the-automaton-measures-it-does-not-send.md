# 0003 - The automaton measures, it does not send

Date: 2026-10-17
Status: accepted

## Context

The corpus originated from analyzing divergence patterns across PHP analyzer test suites
and real-world fixtures. Automated comparison and analysis can produce a large number
of findings. Filing each divergence as an upstream issue or pull request creates an
unmanageable review load for analyzer maintainers.

Tool comparisons and test suites need a neutral repository to record and track findings
without burdening upstream issue trackers or review queues.

## Decision

This repository is the destination. The benchmark records cases, verdicts, and
citations locally, and never opens, replaces, or files pull requests or issues upstream.
Review and validation occur within this repository before findings are committed.

Divergences and defects are published as a matrix and per-tool work lists that
maintainers can inspect at their own discretion.

## Consequences

* Findings accumulate without consuming maintainer attention or cluttering upstream trackers.
* The repository must be self-explanatory: contract, methodology, and citations in-tree, raw evidence next to each run.
* If maintainers want the cases or reproduction steps, they can be accessed as data or reviewed on the published report.
