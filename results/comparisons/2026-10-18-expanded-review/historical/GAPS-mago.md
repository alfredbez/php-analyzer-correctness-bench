# Gaps for mago

From run `historical` (mago 1.54.0, PHP 8.4.26).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `arrays/catalog-mago-aa06b37e787d640d9565` - false_positive

- rule class: `return.type`, domain: `arrays`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-return-statement@7
- reported but not justified: `invalid-return-statement@7`
- run it: `python3 harness/bench.py run --case arrays/catalog-mago-aa06b37e787d640d9565 --tool mago` (case directory: `cases/arrays/catalog-mago-aa06b37e787d640d9565`)

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

## `assignability/catalog-mago-70af4f68103648de14b8` - false_positive

- rule class: `argument.type`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-argument@11, possibly-null-argument@11
- reported but not justified: `invalid-argument@11`, `possibly-null-argument@11`
- run it: `python3 harness/bench.py run --case assignability/catalog-mago-70af4f68103648de14b8 --tool mago` (case directory: `cases/assignability/catalog-mago-70af4f68103648de14b8`)

## `assignability/catalog-mago-ddd6d489f1173eabbd99` - false_positive

- rule class: `invalid-method-access`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-method-access@11
- reported but not justified: `invalid-method-access@11`
- run it: `python3 harness/bench.py run --case assignability/catalog-mago-ddd6d489f1173eabbd99 --tool mago` (case directory: `cases/assignability/catalog-mago-ddd6d489f1173eabbd99`)

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

## `callables/catalog-mago-1e0010ad90cf2846677d` - false_positive

- rule class: `impossible-condition`, domain: `callables`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): impossible-condition@5, impossible-type-comparison@5, no-value@4, no-value@5
- reported but not justified: `impossible-condition@5`, `impossible-type-comparison@5`, `no-value@4`, `no-value@5`
- run it: `python3 harness/bench.py run --case callables/catalog-mago-1e0010ad90cf2846677d --tool mago` (case directory: `cases/callables/catalog-mago-1e0010ad90cf2846677d`)

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

## `dead-code/catalog-mago-c0e93f2edb2c2610c6e8` - false_negative

- rule class: `unreachable-code`, domain: `dead-code`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): unreachable-switch-default
- missing: `unreachable-switch-default`
- run it: `python3 harness/bench.py run --case dead-code/catalog-mago-c0e93f2edb2c2610c6e8 --tool mago` (case directory: `cases/dead-code/catalog-mago-c0e93f2edb2c2610c6e8`)

## `enums/catalog-mago-c0921366ed9477f63e10` - false_positive

- rule class: `method.notFound`, domain: `enums`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): invalid-method-access@11, mixed-return-statement@11
- reported but not justified: `invalid-method-access@11`, `mixed-return-statement@11`
- run it: `python3 harness/bench.py run --case enums/catalog-mago-c0921366ed9477f63e10 --tool mago` (case directory: `cases/enums/catalog-mago-c0921366ed9477f63e10`)

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

## `generics/catalog-mago-5fcd56c1b41c11a4f222` - false_positive

- rule class: `missing-template-parameter`, domain: `generics`
- ground truth basis: `upstream_docs`
- what the tool did: unexpected diagnostic(s): possibly-invalid-argument@17
- reported but not justified: `possibly-invalid-argument@17`
- run it: `python3 harness/bench.py run --case generics/catalog-mago-5fcd56c1b41c11a4f222 --tool mago` (case directory: `cases/generics/catalog-mago-5fcd56c1b41c11a4f222`)

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

## `narrowing/catalog-mago-213d169182afe4bafef8` - false_positive

- rule class: `method.notFound`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): mixed-return-statement@7, mixed-return-statement@8, non-existent-method@7, non-existent-method@8
- reported but not justified: `mixed-return-statement@7`, `mixed-return-statement@8`, `non-existent-method@7`, `non-existent-method@8`
- run it: `python3 harness/bench.py run --case narrowing/catalog-mago-213d169182afe4bafef8 --tool mago` (case directory: `cases/narrowing/catalog-mago-213d169182afe4bafef8`)

## `narrowing/catalog-mago-3c721332594e39bdab90` - false_negative

- rule class: `redundant-condition`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): redundant-condition
- missing: `redundant-condition`
- run it: `python3 harness/bench.py run --case narrowing/catalog-mago-3c721332594e39bdab90 --tool mago` (case directory: `cases/narrowing/catalog-mago-3c721332594e39bdab90`)

## `narrowing/catalog-mago-48e2336d00fe4ea5a90e` - false_positive

- rule class: `argument.type`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): possibly-invalid-argument@5
- reported but not justified: `possibly-invalid-argument@5`
- run it: `python3 harness/bench.py run --case narrowing/catalog-mago-48e2336d00fe4ea5a90e --tool mago` (case directory: `cases/narrowing/catalog-mago-48e2336d00fe4ea5a90e`)

## `narrowing/catalog-mago-7d48310c1ee3d27f86fb` - false_negative

- rule class: `possibly-undefined-variable`, domain: `narrowing`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): possibly-undefined-variable
- missing: `possibly-undefined-variable`
- run it: `python3 harness/bench.py run --case narrowing/catalog-mago-7d48310c1ee3d27f86fb --tool mago` (case directory: `cases/narrowing/catalog-mago-7d48310c1ee3d27f86fb`)

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
- what the tool did: unexpected diagnostic(s): mixed-assignment@5, mixed-property-access@7, mixed-return-statement@7, possible-method-access-on-null@5
- reported but not justified: `mixed-assignment@5`, `mixed-property-access@7`, `mixed-return-statement@7`, `possible-method-access-on-null@5`
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

## `nullability/catalog-psalm-b832ee21bb9a15b5e6bc` - false_positive

- rule class: `method.nonObject`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): mixed-return-statement@5
- reported but not justified: `mixed-return-statement@5`
- run it: `python3 harness/bench.py run --case nullability/catalog-psalm-b832ee21bb9a15b5e6bc --tool mago` (case directory: `cases/nullability/catalog-psalm-b832ee21bb9a15b5e6bc`)

## `nullability/catalog-psalm-c517a982a06f57ea084b` - false_positive

- rule class: `return.type`, domain: `nullability`
- ground truth basis: `runtime_proof`
- what the tool did: unexpected diagnostic(s): nullable-return-statement@4, redundant-comparison@7
- reported but not justified: `nullable-return-statement@4`, `redundant-comparison@7`
- run it: `python3 harness/bench.py run --case nullability/catalog-psalm-c517a982a06f57ea084b --tool mago` (case directory: `cases/nullability/catalog-psalm-c517a982a06f57ea084b`)

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
