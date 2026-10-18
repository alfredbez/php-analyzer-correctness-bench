# Gaps for psalm

From run `stable` (Psalm 6.20.0@804f03c0c183d149fcd4b8c7c0c9b3fbf836d34c, PHP 8.4.26).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `arrays/catalog-phpstan-3df530270084e3d904a0` - false_positive

- rule class: `return.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): InvalidReturnStatement@8, InvalidReturnType@6
- reported but not justified: `InvalidReturnStatement@8`, `InvalidReturnType@6`
- run it: `python3 harness/bench.py run --case arrays/catalog-phpstan-3df530270084e3d904a0 --tool psalm` (case directory: `cases/arrays/catalog-phpstan-3df530270084e3d904a0`)

## `arrays/catalog-psalm-540e6672f974be8ec019` - false_negative

- rule class: `argument.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): PossiblyInvalidArgument
- missing: `PossiblyInvalidArgument`
- run it: `python3 harness/bench.py run --case arrays/catalog-psalm-540e6672f974be8ec019 --tool psalm` (case directory: `cases/arrays/catalog-psalm-540e6672f974be8ec019`)

## `arrays/catalog-psalm-59b1c78bfa12967fb1ac` - false_negative

- rule class: `argument.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): InvalidArgument
- missing: `InvalidArgument`
- run it: `python3 harness/bench.py run --case arrays/catalog-psalm-59b1c78bfa12967fb1ac --tool psalm` (case directory: `cases/arrays/catalog-psalm-59b1c78bfa12967fb1ac`)

## `assignability/catalog-phpstan-bef8ffa161779c8ea9bd` - false_positive

- rule class: `return.type`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): InvalidReturnStatement@8, InvalidReturnType@6
- reported but not justified: `InvalidReturnStatement@8`, `InvalidReturnType@6`
- run it: `python3 harness/bench.py run --case assignability/catalog-phpstan-bef8ffa161779c8ea9bd --tool psalm` (case directory: `cases/assignability/catalog-phpstan-bef8ffa161779c8ea9bd`)

## `callables/catalog-phpstan-554b2c43131257c0d354` - false_positive

- rule class: `return.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): InvalidScope@6, MixedReturnStatement@6
- reported but not justified: `InvalidScope@6`, `MixedReturnStatement@6`
- run it: `python3 harness/bench.py run --case callables/catalog-phpstan-554b2c43131257c0d354 --tool psalm` (case directory: `cases/callables/catalog-phpstan-554b2c43131257c0d354`)

## `callables/catalog-phpstan-6931357e80bcf4ac18ca` - false_positive

- rule class: `return.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): MissingClosureParamType@4, MixedReturnStatement@4
- reported but not justified: `MissingClosureParamType@4`, `MixedReturnStatement@4`
- run it: `python3 harness/bench.py run --case callables/catalog-phpstan-6931357e80bcf4ac18ca --tool psalm` (case directory: `cases/callables/catalog-phpstan-6931357e80bcf4ac18ca`)

## `callables/catalog-phpstan-71ff2ec3ba7e1627cfa7` - false_positive

- rule class: `return.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): MissingClosureParamType@10, MixedArgument@10
- reported but not justified: `MissingClosureParamType@10`, `MixedArgument@10`
- run it: `python3 harness/bench.py run --case callables/catalog-phpstan-71ff2ec3ba7e1627cfa7 --tool psalm` (case directory: `cases/callables/catalog-phpstan-71ff2ec3ba7e1627cfa7`)

## `dead-code/catalog-mago-c0e93f2edb2c2610c6e8` - false_negative

- rule class: `unreachable-code`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): ParadoxicalCondition
- missing: `ParadoxicalCondition`
- run it: `python3 harness/bench.py run --case dead-code/catalog-mago-c0e93f2edb2c2610c6e8 --tool psalm` (case directory: `cases/dead-code/catalog-mago-c0e93f2edb2c2610c6e8`)

## `dead-code/catalog-phpstan-11fdcf0b00c64eb0fb04` - false_positive

- rule class: `unused-parameter`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): MixedAssignment@8
- reported but not justified: `MixedAssignment@8`
- run it: `python3 harness/bench.py run --case dead-code/catalog-phpstan-11fdcf0b00c64eb0fb04 --tool psalm` (case directory: `cases/dead-code/catalog-phpstan-11fdcf0b00c64eb0fb04`)

## `enums/try-from-result-nullability` - false_positive

- rule class: `argument.type`, domain: `enums`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): PossiblyNullArgument@20
- reported but not justified: `PossiblyNullArgument@20`
- run it: `python3 harness/bench.py run --case enums/try-from-result-nullability --tool psalm` (case directory: `cases/enums/try-from-result-nullability`)

## `generics/catalog-phpstan-28d71ec402e5aaedb00e` - false_positive

- rule class: `return.type`, domain: `generics`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): InvalidArrayOffset@10, LessSpecificReturnStatement@9, MixedReturnStatement@10, MoreSpecificReturnType@7
- reported but not justified: `InvalidArrayOffset@10`, `LessSpecificReturnStatement@9`, `MixedReturnStatement@10`, `MoreSpecificReturnType@7`
- run it: `python3 harness/bench.py run --case generics/catalog-phpstan-28d71ec402e5aaedb00e --tool psalm` (case directory: `cases/generics/catalog-phpstan-28d71ec402e5aaedb00e`)

## `generics/catalog-phpstan-d2ee700fdda5c0e356e9` - false_positive

- rule class: `return.type`, domain: `generics`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): MixedReturnStatement@11
- reported but not justified: `MixedReturnStatement@11`
- run it: `python3 harness/bench.py run --case generics/catalog-phpstan-d2ee700fdda5c0e356e9 --tool psalm` (case directory: `cases/generics/catalog-phpstan-d2ee700fdda5c0e356e9`)

## `generics/catalog-psalm-a8cb5b46f221852f2145` - false_negative

- rule class: `InvalidDocblock`, domain: `generics`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): InvalidDocblock
- missing: `InvalidDocblock`
- run it: `python3 harness/bench.py run --case generics/catalog-psalm-a8cb5b46f221852f2145 --tool psalm` (case directory: `cases/generics/catalog-psalm-a8cb5b46f221852f2145`)

## `legacy-patterns/catalog-psalm-6c129980869ba963c7aa` - false_positive

- rule class: `property.notFound`, domain: `legacy-patterns`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): UndefinedPropertyAssignment@7
- reported but not justified: `UndefinedPropertyAssignment@7`
- run it: `python3 harness/bench.py run --case legacy-patterns/catalog-psalm-6c129980869ba963c7aa --tool psalm` (case directory: `cases/legacy-patterns/catalog-psalm-6c129980869ba963c7aa`)

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

## `narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0` - false_positive

- rule class: `return.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): LessSpecificReturnStatement@6, MoreSpecificReturnType@4
- reported but not justified: `LessSpecificReturnStatement@6`, `MoreSpecificReturnType@4`
- run it: `python3 harness/bench.py run --case narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0 --tool psalm` (case directory: `cases/narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0`)

## `narrowing/catalog-phpstan-2a3506b6815e78d94aa5` - false_positive

- rule class: `return.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): MixedReturnStatement@10
- reported but not justified: `MixedReturnStatement@10`
- run it: `python3 harness/bench.py run --case narrowing/catalog-phpstan-2a3506b6815e78d94aa5 --tool psalm` (case directory: `cases/narrowing/catalog-phpstan-2a3506b6815e78d94aa5`)

## `narrowing/catalog-psalm-924aac46207f32ed8ed5` - false_positive

- rule class: `return.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): RedundantCastGivenDocblockType@7
- reported but not justified: `RedundantCastGivenDocblockType@7`
- run it: `python3 harness/bench.py run --case narrowing/catalog-psalm-924aac46207f32ed8ed5 --tool psalm` (case directory: `cases/narrowing/catalog-psalm-924aac46207f32ed8ed5`)

## `narrowing/catalog-psalm-cd294fcb8e014ab18e3e` - mixed

- rule class: `impossible-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing TypeDoesNotContainType; unexpected UnsafeInstantiation@8
- missing: `TypeDoesNotContainType`
- reported but not justified: `UnsafeInstantiation@8`
- run it: `python3 harness/bench.py run --case narrowing/catalog-psalm-cd294fcb8e014ab18e3e --tool psalm` (case directory: `cases/narrowing/catalog-psalm-cd294fcb8e014ab18e3e`)

## `narrowing/catalog-psalm-de14e6754f8edfa65da8` - false_positive

- rule class: `argument.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): MixedMethodCall@5
- reported but not justified: `MixedMethodCall@5`
- run it: `python3 harness/bench.py run --case narrowing/catalog-psalm-de14e6754f8edfa65da8 --tool psalm` (case directory: `cases/narrowing/catalog-psalm-de14e6754f8edfa65da8`)

## `nullability/catalog-phpstan-306c280bb8a6ca46a961` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): InvalidReturnStatement@13, InvalidReturnType@6
- reported but not justified: `InvalidReturnStatement@13`, `InvalidReturnType@6`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-306c280bb8a6ca46a961 --tool psalm` (case directory: `cases/nullability/catalog-phpstan-306c280bb8a6ca46a961`)

## `nullability/catalog-phpstan-3df7186a1b833d024d52` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): FalsableReturnStatement@5, InvalidFalsableReturnType@4
- reported but not justified: `FalsableReturnStatement@5`, `InvalidFalsableReturnType@4`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-3df7186a1b833d024d52 --tool psalm` (case directory: `cases/nullability/catalog-phpstan-3df7186a1b833d024d52`)

## `nullability/catalog-phpstan-3ecb74a1fba6668eac61` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): LessSpecificReturnStatement@7, MoreSpecificReturnType@5
- reported but not justified: `LessSpecificReturnStatement@7`, `MoreSpecificReturnType@5`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-3ecb74a1fba6668eac61 --tool psalm` (case directory: `cases/nullability/catalog-phpstan-3ecb74a1fba6668eac61`)

## `nullability/catalog-phpstan-5d813bb8b104d0c619ca` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): MixedReturnStatement@7, PossiblyNullReference@5, UndefinedPropertyFetch@7
- reported but not justified: `MixedReturnStatement@7`, `PossiblyNullReference@5`, `UndefinedPropertyFetch@7`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-5d813bb8b104d0c619ca --tool psalm` (case directory: `cases/nullability/catalog-phpstan-5d813bb8b104d0c619ca`)

## `nullability/catalog-phpstan-d1f39552939e65fa35c3` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): FalsableReturnStatement@4, InvalidFalsableReturnType@4
- reported but not justified: `FalsableReturnStatement@4`, `InvalidFalsableReturnType@4`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-d1f39552939e65fa35c3 --tool psalm` (case directory: `cases/nullability/catalog-phpstan-d1f39552939e65fa35c3`)

## `nullability/catalog-psalm-c517a982a06f57ea084b` - false_negative

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): NullableReturnStatement
- missing: `NullableReturnStatement`
- run it: `python3 harness/bench.py run --case nullability/catalog-psalm-c517a982a06f57ea084b --tool psalm` (case directory: `cases/nullability/catalog-psalm-c517a982a06f57ea084b`)

## `phpdoc-extensions/catalog-psalm-53ae3931e59580d6f84c` - false_positive

- rule class: `NamedArgumentNotAllowed`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: unexpected diagnostic(s): InvalidArgument@8
- reported but not justified: `InvalidArgument@8`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-psalm-53ae3931e59580d6f84c --tool psalm` (case directory: `cases/phpdoc-extensions/catalog-psalm-53ae3931e59580d6f84c`)
