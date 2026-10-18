# Gaps for phpstan

From run `2026-10-18T12-06-50Z-factory-12` (PHPStan - PHP Static Analysis Tool 2.3.1, PHP 8.3.35).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `arrays/array-key-for-string-key` - false_negative

- rule class: `argument.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): argument.type
- missing: `argument.type`
- run it: `python3 harness/bench.py run --case arrays/array-key-for-string-key --tool phpstan` (case directory: `cases/arrays/array-key-for-string-key`)

## `dead-code/finally-assignment-always-runs` - false_positive

- rule class: `constant-condition`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): ternary.alwaysFalse@25
- reported but not justified: `ternary.alwaysFalse@25`
- run it: `python3 harness/bench.py run --case dead-code/finally-assignment-always-runs --tool phpstan` (case directory: `cases/dead-code/finally-assignment-always-runs`)
