# Gaps for psalm

From run `2026-10-18T06-26-23Z-takeover-baseline` (Psalm 6.20.0@804f03c0c183d149fcd4b8c7c0c9b3fbf836d34c, PHP 8.3.35).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `narrowing/redundant-instanceof-on-declared-class` - false_negative

- rule class: `redundant-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): RedundantCondition
- missing: `RedundantCondition`
- run it: `python3 harness/bench.py run --case narrowing/redundant-instanceof-on-declared-class --tool psalm` (case directory: `cases/narrowing/redundant-instanceof-on-declared-class`)
