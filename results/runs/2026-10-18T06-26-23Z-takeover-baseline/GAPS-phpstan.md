# Gaps for phpstan

From run `2026-10-18T06-26-23Z-takeover-baseline` (PHPStan - PHP Static Analysis Tool 2.3.1, PHP 8.3.35).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `dead-code/finally-assignment-always-runs` - false_positive

- rule class: `constant-condition`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): ternary.alwaysFalse@25
- reported but not justified: `ternary.alwaysFalse@25`
- run it: `python3 harness/bench.py run --case dead-code/finally-assignment-always-runs --tool phpstan` (case directory: `cases/dead-code/finally-assignment-always-runs`)
