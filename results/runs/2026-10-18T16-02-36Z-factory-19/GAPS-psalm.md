# Gaps for psalm

From run `2026-10-18T16-02-36Z-factory-19` (Psalm 6.20.0@804f03c0c183d149fcd4b8c7c0c9b3fbf836d34c, PHP 8.3.35).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `enums/try-from-result-nullability` - false_positive

- rule class: `argument.type`, domain: `enums`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): PossiblyNullArgument@20
- reported but not justified: `PossiblyNullArgument@20`
- run it: `python3 harness/bench.py run --case enums/try-from-result-nullability --tool psalm` (case directory: `cases/enums/try-from-result-nullability`)

## `legacy-patterns/count-on-iterable` - false_negative

- rule class: `argument.type`, domain: `legacy-patterns`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): PossiblyInvalidArgument
- missing: `PossiblyInvalidArgument`
- run it: `python3 harness/bench.py run --case legacy-patterns/count-on-iterable --tool psalm` (case directory: `cases/legacy-patterns/count-on-iterable`)

## `legacy-patterns/loose-comparison-with-zero` - false_negative

- rule class: `impossible-condition`, domain: `legacy-patterns`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): TypeDoesNotContainType
- missing: `TypeDoesNotContainType`
- run it: `python3 harness/bench.py run --case legacy-patterns/loose-comparison-with-zero --tool psalm` (case directory: `cases/legacy-patterns/loose-comparison-with-zero`)
