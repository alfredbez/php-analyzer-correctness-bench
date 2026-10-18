# Gaps for mago

From run `main` (mago 1.57.0, PHP 8.4.26).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `arrays/catalog-phpstan-3df530270084e3d904a0` - false_positive

- rule class: `return.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-return-statement@8, possibly-invalid-argument@8
- reported but not justified: `invalid-return-statement@8`, `possibly-invalid-argument@8`
- run it: `python3 harness/bench.py run --case arrays/catalog-phpstan-3df530270084e3d904a0 --tool mago` (case directory: `cases/arrays/catalog-phpstan-3df530270084e3d904a0`)

## `arrays/catalog-phpstan-d438454d94600dcbba53` - false_positive

- rule class: `return.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-return-statement@10
- reported but not justified: `invalid-return-statement@10`
- run it: `python3 harness/bench.py run --case arrays/catalog-phpstan-d438454d94600dcbba53 --tool mago` (case directory: `cases/arrays/catalog-phpstan-d438454d94600dcbba53`)

## `arrays/catalog-psalm-13be39b2d9591fa1a9e5` - false_negative

- rule class: `MixedArrayOffset`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): mixed-array-index
- missing: `mixed-array-index`
- run it: `python3 harness/bench.py run --case arrays/catalog-psalm-13be39b2d9591fa1a9e5 --tool mago` (case directory: `cases/arrays/catalog-psalm-13be39b2d9591fa1a9e5`)

## `arrays/catalog-psalm-540e6672f974be8ec019` - false_negative

- rule class: `argument.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): invalid-argument
- missing: `invalid-argument`
- run it: `python3 harness/bench.py run --case arrays/catalog-psalm-540e6672f974be8ec019 --tool mago` (case directory: `cases/arrays/catalog-psalm-540e6672f974be8ec019`)

## `arrays/catalog-psalm-59b1c78bfa12967fb1ac` - false_negative

- rule class: `argument.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): invalid-argument
- missing: `invalid-argument`
- run it: `python3 harness/bench.py run --case arrays/catalog-psalm-59b1c78bfa12967fb1ac --tool mago` (case directory: `cases/arrays/catalog-psalm-59b1c78bfa12967fb1ac`)

## `assignability/catalog-phpstan-abc5fa1b77dc14531ca8` - false_positive

- rule class: `return.type`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-invalid-argument@6
- reported but not justified: `possibly-invalid-argument@6`
- run it: `python3 harness/bench.py run --case assignability/catalog-phpstan-abc5fa1b77dc14531ca8 --tool mago` (case directory: `cases/assignability/catalog-phpstan-abc5fa1b77dc14531ca8`)

## `assignability/catalog-psalm-0e66d52886bd21db7846` - false_positive

- rule class: `return.type`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-return-statement@17, invalid-return-statement@9
- reported but not justified: `invalid-return-statement@17`, `invalid-return-statement@9`
- run it: `python3 harness/bench.py run --case assignability/catalog-psalm-0e66d52886bd21db7846 --tool mago` (case directory: `cases/assignability/catalog-psalm-0e66d52886bd21db7846`)

## `assignability/catalog-psalm-5489e87365002fea3494` - false_positive

- rule class: `return.type`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-return-statement@9
- reported but not justified: `invalid-return-statement@9`
- run it: `python3 harness/bench.py run --case assignability/catalog-psalm-5489e87365002fea3494 --tool mago` (case directory: `cases/assignability/catalog-psalm-5489e87365002fea3494`)

## `callables/catalog-phpstan-554b2c43131257c0d354` - false_positive

- rule class: `return.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): redundant-condition@6
- reported but not justified: `redundant-condition@6`
- run it: `python3 harness/bench.py run --case callables/catalog-phpstan-554b2c43131257c0d354 --tool mago` (case directory: `cases/callables/catalog-phpstan-554b2c43131257c0d354`)

## `callables/catalog-phpstan-6931357e80bcf4ac18ca` - false_positive

- rule class: `return.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): mixed-return-statement@4
- reported but not justified: `mixed-return-statement@4`
- run it: `python3 harness/bench.py run --case callables/catalog-phpstan-6931357e80bcf4ac18ca --tool mago` (case directory: `cases/callables/catalog-phpstan-6931357e80bcf4ac18ca`)

## `callables/catalog-phpstan-71ff2ec3ba7e1627cfa7` - false_positive

- rule class: `return.type`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): mixed-argument@10
- reported but not justified: `mixed-argument@10`
- run it: `python3 harness/bench.py run --case callables/catalog-phpstan-71ff2ec3ba7e1627cfa7 --tool mago` (case directory: `cases/callables/catalog-phpstan-71ff2ec3ba7e1627cfa7`)

## `enums/catalog-psalm-c013f91ca882f9f18a36` - false_positive

- rule class: `argument.type`, domain: `enums`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-invalid-argument@8
- reported but not justified: `possibly-invalid-argument@8`
- run it: `python3 harness/bench.py run --case enums/catalog-psalm-c013f91ca882f9f18a36 --tool mago` (case directory: `cases/enums/catalog-psalm-c013f91ca882f9f18a36`)

## `enums/try-from-result-nullability` - false_positive

- rule class: `argument.type`, domain: `enums`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-null-argument@20
- reported but not justified: `possibly-null-argument@20`
- run it: `python3 harness/bench.py run --case enums/try-from-result-nullability --tool mago` (case directory: `cases/enums/try-from-result-nullability`)

## `generics/catalog-phpstan-28d71ec402e5aaedb00e` - false_positive

- rule class: `return.type`, domain: `generics`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-return-statement@10, invalid-return-statement@9, undefined-string-array-index@10
- reported but not justified: `invalid-return-statement@10`, `invalid-return-statement@9`, `undefined-string-array-index@10`
- run it: `python3 harness/bench.py run --case generics/catalog-phpstan-28d71ec402e5aaedb00e --tool mago` (case directory: `cases/generics/catalog-phpstan-28d71ec402e5aaedb00e`)

## `legacy-patterns/catalog-mago-af46b0f735b875e1a546` - false_positive

- rule class: `undefined-variable`, domain: `legacy-patterns`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-iterator@10, mixed-argument@10, mixed-assignment@10, undefined-variable@10, undefined-variable@7
- reported but not justified: `invalid-iterator@10`, `mixed-argument@10`, `mixed-assignment@10`, `undefined-variable@10`, `undefined-variable@7`
- run it: `python3 harness/bench.py run --case legacy-patterns/catalog-mago-af46b0f735b875e1a546 --tool mago` (case directory: `cases/legacy-patterns/catalog-mago-af46b0f735b875e1a546`)

## `legacy-patterns/catalog-psalm-6c129980869ba963c7aa` - false_positive

- rule class: `property.notFound`, domain: `legacy-patterns`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): non-existent-property@7
- reported but not justified: `non-existent-property@7`
- run it: `python3 harness/bench.py run --case legacy-patterns/catalog-psalm-6c129980869ba963c7aa --tool mago` (case directory: `cases/legacy-patterns/catalog-psalm-6c129980869ba963c7aa`)

## `narrowing/catalog-mago-48e2336d00fe4ea5a90e` - false_positive

- rule class: `argument.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-invalid-argument@5
- reported but not justified: `possibly-invalid-argument@5`
- run it: `python3 harness/bench.py run --case narrowing/catalog-mago-48e2336d00fe4ea5a90e --tool mago` (case directory: `cases/narrowing/catalog-mago-48e2336d00fe4ea5a90e`)

## `narrowing/catalog-mago-ac60f1cdd2c628cc61fc` - false_positive

- rule class: `method.notFound`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): mixed-return-statement@7
- reported but not justified: `mixed-return-statement@7`
- run it: `python3 harness/bench.py run --case narrowing/catalog-mago-ac60f1cdd2c628cc61fc --tool mago` (case directory: `cases/narrowing/catalog-mago-ac60f1cdd2c628cc61fc`)

## `narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0` - false_positive

- rule class: `return.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): less-specific-return-statement@6
- reported but not justified: `less-specific-return-statement@6`
- run it: `python3 harness/bench.py run --case narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0 --tool mago` (case directory: `cases/narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0`)

## `narrowing/catalog-phpstan-2a3506b6815e78d94aa5` - false_positive

- rule class: `return.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): mixed-return-statement@10
- reported but not justified: `mixed-return-statement@10`
- run it: `python3 harness/bench.py run --case narrowing/catalog-phpstan-2a3506b6815e78d94aa5 --tool mago` (case directory: `cases/narrowing/catalog-phpstan-2a3506b6815e78d94aa5`)

## `narrowing/catalog-psalm-924aac46207f32ed8ed5` - false_positive

- rule class: `return.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-return-statement@7
- reported but not justified: `invalid-return-statement@7`
- run it: `python3 harness/bench.py run --case narrowing/catalog-psalm-924aac46207f32ed8ed5 --tool mago` (case directory: `cases/narrowing/catalog-psalm-924aac46207f32ed8ed5`)

## `narrowing/catalog-psalm-cd294fcb8e014ab18e3e` - mixed

- rule class: `impossible-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing impossible-condition; unexpected redundant-docblock-type@7
- missing: `impossible-condition`
- reported but not justified: `redundant-docblock-type@7`
- run it: `python3 harness/bench.py run --case narrowing/catalog-psalm-cd294fcb8e014ab18e3e --tool mago` (case directory: `cases/narrowing/catalog-psalm-cd294fcb8e014ab18e3e`)

## `narrowing/catalog-psalm-de14e6754f8edfa65da8` - false_positive

- rule class: `argument.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): unknown-class-instantiation@5
- reported but not justified: `unknown-class-instantiation@5`
- run it: `python3 harness/bench.py run --case narrowing/catalog-psalm-de14e6754f8edfa65da8 --tool mago` (case directory: `cases/narrowing/catalog-psalm-de14e6754f8edfa65da8`)

## `nullability/catalog-phpstan-3df7186a1b833d024d52` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): falsable-return-statement@5, invalid-return-statement@5
- reported but not justified: `falsable-return-statement@5`, `invalid-return-statement@5`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-3df7186a1b833d024d52 --tool mago` (case directory: `cases/nullability/catalog-phpstan-3df7186a1b833d024d52`)

## `nullability/catalog-phpstan-5588ff8af852e7139b7d` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-null-property-access@6
- reported but not justified: `possibly-null-property-access@6`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-5588ff8af852e7139b7d --tool mago` (case directory: `cases/nullability/catalog-phpstan-5588ff8af852e7139b7d`)

## `nullability/catalog-phpstan-5d813bb8b104d0c619ca` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possible-method-access-on-null@5
- reported but not justified: `possible-method-access-on-null@5`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-5d813bb8b104d0c619ca --tool mago` (case directory: `cases/nullability/catalog-phpstan-5d813bb8b104d0c619ca`)

## `nullability/catalog-phpstan-d1f39552939e65fa35c3` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): falsable-return-statement@4, invalid-return-statement@4
- reported but not justified: `falsable-return-statement@4`, `invalid-return-statement@4`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-d1f39552939e65fa35c3 --tool mago` (case directory: `cases/nullability/catalog-phpstan-d1f39552939e65fa35c3`)

## `nullability/catalog-phpstan-f1455a36807cc2badc75` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-null-property-access@10
- reported but not justified: `possibly-null-property-access@10`
- run it: `python3 harness/bench.py run --case nullability/catalog-phpstan-f1455a36807cc2badc75 --tool mago` (case directory: `cases/nullability/catalog-phpstan-f1455a36807cc2badc75`)

## `nullability/catalog-psalm-c517a982a06f57ea084b` - false_negative

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): invalid-return-statement
- missing: `invalid-return-statement`
- run it: `python3 harness/bench.py run --case nullability/catalog-psalm-c517a982a06f57ea084b --tool mago` (case directory: `cases/nullability/catalog-psalm-c517a982a06f57ea084b`)

## `nullability/elseif-else-return-keeps-possible-null` - false_positive

- rule class: `redundant-condition`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): redundant-comparison@23
- reported but not justified: `redundant-comparison@23`
- run it: `python3 harness/bench.py run --case nullability/elseif-else-return-keeps-possible-null --tool mago` (case directory: `cases/nullability/elseif-else-return-keeps-possible-null`)

## `phpdoc-extensions/catalog-mago-d86bc7b7eabe71006e0c` - false_negative

- rule class: `invalid-docblock`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): invalid-docblock
- missing: `invalid-docblock`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-mago-d86bc7b7eabe71006e0c --tool mago` (case directory: `cases/phpdoc-extensions/catalog-mago-d86bc7b7eabe71006e0c`)

## `phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da` - false_negative

- rule class: `InvalidDocblock`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): invalid-docblock
- missing: `invalid-docblock`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da --tool mago` (case directory: `cases/phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da`)

## `phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3` - false_negative

- rule class: `InvalidDocblock`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): invalid-docblock
- missing: `invalid-docblock`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3 --tool mago` (case directory: `cases/phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3`)

## `phpdoc-extensions/catalog-psalm-a02980c52843949bdecb` - false_negative

- rule class: `InvalidDocblock`, domain: `phpdoc-extensions`
- ground truth basis: `upstream_docs`
- what the tool did: missing required diagnostic(s): invalid-docblock
- missing: `invalid-docblock`
- run it: `python3 harness/bench.py run --case phpdoc-extensions/catalog-psalm-a02980c52843949bdecb --tool mago` (case directory: `cases/phpdoc-extensions/catalog-psalm-a02980c52843949bdecb`)
