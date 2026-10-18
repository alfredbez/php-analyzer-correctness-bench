# Gaps for mago

From run `2026-10-18T06-26-23Z-takeover-baseline` (mago 1.57.0, PHP 8.3.35).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `callables/is-object-on-callable-parameter` - false_positive

- rule class: `argument.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): impossible-condition@24, impossible-type-comparison@24, no-value@25
- reported but not justified: `impossible-condition@24`, `impossible-type-comparison@24`, `no-value@25`
- run it: `python3 harness/bench.py run --case callables/is-object-on-callable-parameter --tool mago` (case directory: `cases/callables/is-object-on-callable-parameter`)

## `callables/negated-is-callable-removes-function-name` - false_positive

- rule class: `argument.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-invalid-argument@24
- reported but not justified: `possibly-invalid-argument@24`
- run it: `python3 harness/bench.py run --case callables/negated-is-callable-removes-function-name --tool mago` (case directory: `cases/callables/negated-is-callable-removes-function-name`)

## `narrowing/negated-instanceof-unrelated-class` - false_negative

- rule class: `impossible-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): impossible-type-comparison
- missing: `impossible-type-comparison`
- run it: `python3 harness/bench.py run --case narrowing/negated-instanceof-unrelated-class --tool mago` (case directory: `cases/narrowing/negated-instanceof-unrelated-class`)

## `narrowing/redundant-instanceof-on-declared-class` - false_negative

- rule class: `redundant-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): redundant-condition
- missing: `redundant-condition`
- run it: `python3 harness/bench.py run --case narrowing/redundant-instanceof-on-declared-class --tool mago` (case directory: `cases/narrowing/redundant-instanceof-on-declared-class`)

## `nullability/elseif-else-return-keeps-possible-null` - false_positive

- rule class: `redundant-condition`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): redundant-comparison@23
- reported but not justified: `redundant-comparison@23`
- run it: `python3 harness/bench.py run --case nullability/elseif-else-return-keeps-possible-null --tool mago` (case directory: `cases/nullability/elseif-else-return-keeps-possible-null`)

## `nullability/loose-null-guard-keeps-empty-string` - false_positive

- rule class: `redundant-condition`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): redundant-comparison@15, redundant-condition@15
- reported but not justified: `redundant-comparison@15`, `redundant-condition@15`
- run it: `python3 harness/bench.py run --case nullability/loose-null-guard-keeps-empty-string --tool mago` (case directory: `cases/nullability/loose-null-guard-keeps-empty-string`)
