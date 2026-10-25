# Gaps for phpstan

From run `2026-10-24-stable-final` (PHPStan - PHP Static Analysis Tool 2.3.1, PHP 8.4.27).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `arrays/catalog-psalm-59b1c78bfa12967fb1ac` - false_negative

- rule class: `argument.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): argument.type
- missing: `argument.type`
- run it: `python3 harness/bench.py run --case arrays/catalog-psalm-59b1c78bfa12967fb1ac --tool phpstan` (case directory: `cases/arrays/catalog-psalm-59b1c78bfa12967fb1ac`)

## `assignability/catalog-psalm-7597f481858da256f914` - false_negative

- rule class: `OverriddenPropertyAccess`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): property.visibility
- missing: `property.visibility`
- run it: `python3 harness/bench.py run --case assignability/catalog-psalm-7597f481858da256f914 --tool phpstan` (case directory: `cases/assignability/catalog-psalm-7597f481858da256f914`)

## `dead-code/catalog-mago-c0e93f2edb2c2610c6e8` - false_negative

- rule class: `unreachable-code`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): deadCode.unreachable
- missing: `deadCode.unreachable`
- run it: `python3 harness/bench.py run --case dead-code/catalog-mago-c0e93f2edb2c2610c6e8 --tool phpstan` (case directory: `cases/dead-code/catalog-mago-c0e93f2edb2c2610c6e8`)

## `dead-code/catalog-psalm-2e01e321c4dcfa1729a2` - false_negative

- rule class: `RedundantCast`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): cast.useless
- missing: `cast.useless`
- run it: `python3 harness/bench.py run --case dead-code/catalog-psalm-2e01e321c4dcfa1729a2 --tool phpstan` (case directory: `cases/dead-code/catalog-psalm-2e01e321c4dcfa1729a2`)

## `dead-code/finally-assignment-always-runs` - false_positive

- rule class: `constant-condition`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): ternary.alwaysFalse@25
- reported but not justified: `ternary.alwaysFalse@25`
- run it: `python3 harness/bench.py run --case dead-code/finally-assignment-always-runs --tool phpstan` (case directory: `cases/dead-code/finally-assignment-always-runs`)

## `legacy-patterns/catalog-psalm-6c129980869ba963c7aa` - false_positive

- rule class: `property.notFound`, domain: `legacy-patterns`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): property.notFound@7
- reported but not justified: `property.notFound@7`
- run it: `python3 harness/bench.py run --case legacy-patterns/catalog-psalm-6c129980869ba963c7aa --tool phpstan` (case directory: `cases/legacy-patterns/catalog-psalm-6c129980869ba963c7aa`)

## `narrowing/catalog-mago-3c721332594e39bdab90` - false_negative

- rule class: `redundant-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): if.alwaysTrue
- missing: `if.alwaysTrue`
- run it: `python3 harness/bench.py run --case narrowing/catalog-mago-3c721332594e39bdab90 --tool phpstan` (case directory: `cases/narrowing/catalog-mago-3c721332594e39bdab90`)

## `narrowing/catalog-phpstan-2a3506b6815e78d94aa5` - false_positive

- rule class: `return.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): return.type@10
- reported but not justified: `return.type@10`
- run it: `python3 harness/bench.py run --case narrowing/catalog-phpstan-2a3506b6815e78d94aa5 --tool phpstan` (case directory: `cases/narrowing/catalog-phpstan-2a3506b6815e78d94aa5`)

## `narrowing/catalog-psalm-cd294fcb8e014ab18e3e` - false_negative

- rule class: `impossible-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): function.impossibleType
- missing: `function.impossibleType`
- run it: `python3 harness/bench.py run --case narrowing/catalog-psalm-cd294fcb8e014ab18e3e --tool phpstan` (case directory: `cases/narrowing/catalog-psalm-cd294fcb8e014ab18e3e`)

## `nullability/catalog-phpstan-3df7186a1b833d024d52` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): return.type@5
- reported but not justified: `return.type@5`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-3df7186a1b833d024d52 --tool phpstan` (case directory: `cases/nullability/catalog-phpstan-3df7186a1b833d024d52`)

## `nullability/catalog-psalm-c517a982a06f57ea084b` - false_negative

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): return.type
- missing: `return.type`
- run it: `python3 harness/bench.py run --case nullability/catalog-psalm-c517a982a06f57ea084b --tool phpstan` (case directory: `cases/nullability/catalog-psalm-c517a982a06f57ea084b`)

## `phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da` - false_negative

- rule class: `InvalidDocblock`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): typeAlias.invalidType
- missing: `typeAlias.invalidType`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da --tool phpstan` (case directory: `cases/phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da`)

## `phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3` - false_negative

- rule class: `InvalidDocblock`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): /(?i)(duplicat.*@return|@return.*(duplicat|more than once|multiple))/
- missing: `/(?i)(duplicat.*@return|@return.*(duplicat|more than once|multiple))/`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3 --tool phpstan` (case directory: `cases/phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3`)

## `phpdoc-extensions/catalog-psalm-a02980c52843949bdecb` - false_negative

- rule class: `InvalidDocblock`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): phpDoc.duplicateTag
- missing: `phpDoc.duplicateTag`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-psalm-a02980c52843949bdecb --tool phpstan` (case directory: `cases/phpdoc-extensions/catalog-psalm-a02980c52843949bdecb`)
