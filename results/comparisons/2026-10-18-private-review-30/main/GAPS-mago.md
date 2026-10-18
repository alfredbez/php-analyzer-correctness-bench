# Gaps for mago

From run `main` (mago 1.57.0, PHP 8.3.35).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

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
