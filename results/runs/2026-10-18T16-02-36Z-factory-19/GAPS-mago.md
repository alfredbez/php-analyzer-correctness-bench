# Gaps for mago

From run `2026-10-18T16-02-36Z-factory-19` (mago 1.57.0, PHP 8.3.35).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `arrays/numeric-string-array-key` - false_positive

- rule class: `impossible-condition`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): impossible-condition@12, no-value@17
- reported but not justified: `impossible-condition@12`, `no-value@17`
- run it: `python3 harness/bench.py run --case arrays/numeric-string-array-key --tool mago` (case directory: `cases/arrays/numeric-string-array-key`)

## `arrays/strict-in-array-narrowing` - false_positive

- rule class: `argument.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-invalid-argument@17
- reported but not justified: `possibly-invalid-argument@17`
- run it: `python3 harness/bench.py run --case arrays/strict-in-array-narrowing --tool mago` (case directory: `cases/arrays/strict-in-array-narrowing`)

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

## `enums/try-from-result-nullability` - false_positive

- rule class: `argument.type`, domain: `enums`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-null-argument@20
- reported but not justified: `possibly-null-argument@20`
- run it: `python3 harness/bench.py run --case enums/try-from-result-nullability --tool mago` (case directory: `cases/enums/try-from-result-nullability`)

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
