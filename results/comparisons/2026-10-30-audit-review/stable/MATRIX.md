# Correctness matrix

| Case | Domain | Rule class | Ground truth | mago | phpstan | psalm |
| --- | --- | --- | --- | --- | --- | --- |
| `arrays/array-key-for-string-key` | arrays | argument.type | runtime_proof (runtime) | ok | n/a | ok |
| `arrays/catalog-mago-2495784ddff2f9b32ae7` | arrays | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-mago-3cb66fa76d0fbac8d0a6` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-mago-516197fbc28d66be6138` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-mago-aa06b37e787d640d9565` | arrays | return.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-mago-b04020e1b1f459b0e255` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-mago-bc1302afb96cabb21965` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-mago-bc8c6a80a3112f0b9fcf` | arrays | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-phpstan-2bc9c9c0af361dbd0dea` | arrays | return.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-phpstan-3df530270084e3d904a0` | arrays | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): invalid-return-statement@8, possibly-invali…</sub> | ok | **FP** <sub>unexpected diagnostic(s): InvalidReturnStatement@8, InvalidReturnType…</sub> |
| `arrays/catalog-phpstan-a5a1bead8612b57ce91c` | arrays | return.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-phpstan-d438454d94600dcbba53` | arrays | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): invalid-return-statement@10</sub> | ok | ok |
| `arrays/catalog-phpstan-e03afd4ffd085e429c5e` | arrays | return.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-psalm-13be39b2d9591fa1a9e5` | arrays | MixedArrayOffset | runtime_proof (runtime) | **FN** <sub>missing required diagnostic(s): mixed-array-index</sub> | ok | ok |
| `arrays/catalog-psalm-1fb88d68d2ffa0e1ab18` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-psalm-540e6672f974be8ec019` | arrays | argument.type | runtime_proof (runtime) | **FN** <sub>missing required diagnostic(s): invalid-argument</sub> | ok | **FN** <sub>missing required diagnostic(s): PossiblyInvalidArgument</sub> |
| `arrays/catalog-psalm-59b1c78bfa12967fb1ac` | arrays | argument.type | runtime_proof (runtime) | **FN** <sub>missing required diagnostic(s): invalid-argument</sub> | **FN** <sub>missing required diagnostic(s): argument.type</sub> | **FN** <sub>missing required diagnostic(s): InvalidArgument</sub> |
| `arrays/catalog-psalm-6e0079989da3fbda2530` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/catalog-psalm-946e241294d114c29a8b` | arrays | return.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/numeric-string-array-key` | arrays | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `arrays/scalar-array-for-string-array` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/strict-in-array-narrowing` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/callable-not-closure` | assignability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-mago-70af4f68103648de14b8` | assignability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-mago-af4d2483259287749e40` | assignability | method.notFound | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-mago-ddd6d489f1173eabbd99` | assignability | invalid-method-access | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-phpstan-23edd0555732c08f1948` | assignability | return.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-phpstan-34d04d27febb3bff2282` | assignability | return.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-phpstan-70f67b02133286eb99f5` | assignability | return.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-phpstan-935b22d9e63374f594a3` | assignability | return.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-phpstan-abc5fa1b77dc14531ca8` | assignability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-invalid-argument@6</sub> | ok | ok |
| `assignability/catalog-phpstan-bef8ffa161779c8ea9bd` | assignability | return.type | runtime_proof (runtime) | ok | ok | **FP** <sub>unexpected diagnostic(s): InvalidReturnStatement@8, InvalidReturnType…</sub> |
| `assignability/catalog-phpstan-da61ed3a1be4f5592a03` | assignability | invalid-property-write | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-psalm-0e66d52886bd21db7846` | assignability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): invalid-return-statement@17, invalid-return…</sub> | ok | ok |
| `assignability/catalog-psalm-28307cba67aa2a6c65af` | assignability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-psalm-2ed1be42908ccc536dd5` | assignability | invalid-operand | runtime_proof (runtime) | **FN** <sub>missing required diagnostic(s): invalid-operand</sub> | ok | ok |
| `assignability/catalog-psalm-5489e87365002fea3494` | assignability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): invalid-return-statement@9</sub> | ok | ok |
| `assignability/catalog-psalm-7597f481858da256f914` | assignability | OverriddenPropertyAccess | runtime_proof | skip | skip | skip |
| `assignability/catalog-psalm-7c8a6899c045380fcf5f` | assignability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-psalm-969cef3e55d9ffe925f9` | assignability | argument.count | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-psalm-a6aa7787b414a8456355` | assignability | throws.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-psalm-e8412c2dfa81d2a9bbd5` | assignability | argument.count | runtime_proof (runtime) | ok | ok | ok |
| `assignability/catalog-psalm-fbe59540f6b89bde9139` | assignability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/docblock-return-covariance` | assignability | method.childReturnType | runtime_proof (runtime) | ok | n/a | ok |
| `callables/catalog-mago-1e0010ad90cf2846677d` | callables | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `callables/catalog-mago-8c7967e992bbf717d0fd` | callables | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `callables/catalog-mago-ea195975bc7c109ce598` | callables | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `callables/catalog-phpstan-554b2c43131257c0d354` | callables | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): redundant-condition@6</sub> | ok | **FP** <sub>unexpected diagnostic(s): InvalidScope@6, MixedReturnStatement@6</sub> |
| `callables/catalog-phpstan-6931357e80bcf4ac18ca` | callables | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): mixed-return-statement@4</sub> | ok | **FP** <sub>unexpected diagnostic(s): MissingClosureParamType@4, MixedReturnState…</sub> |
| `callables/catalog-phpstan-71ff2ec3ba7e1627cfa7` | callables | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): mixed-argument@10</sub> | ok | **FP** <sub>unexpected diagnostic(s): MissingClosureParamType@10, MixedArgument@10</sub> |
| `callables/catalog-psalm-100d258360108b7340f8` | callables | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `callables/catalog-psalm-7d2ccd7549c78392118c` | callables | phpDoc.parseError | runtime_proof (runtime) | ok | ok | ok |
| `callables/catalog-psalm-9e4f5a27653ddc7273ca` | callables | phpDoc.parseError | runtime_proof (runtime) | ok | ok | ok |
| `callables/catalog-psalm-f280033f57db8a07358a` | callables | InvalidDocblock | upstream_docs (runtime) | ok | ok | ok |
| `callables/is-object-on-callable-parameter` | callables | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `callables/negated-is-callable-removes-function-name` | callables | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `dead-code/catalog-mago-c0e93f2edb2c2610c6e8` | dead-code | unreachable-code | runtime_proof (runtime) | ok | **FN** <sub>missing required diagnostic(s): deadCode.unreachable</sub> | **FN** <sub>missing required diagnostic(s): ParadoxicalCondition</sub> |
| `dead-code/catalog-phpstan-11fdcf0b00c64eb0fb04` | dead-code | unused-parameter | runtime_proof (runtime) | ok | ok | ok |
| `dead-code/catalog-phpstan-6e5e8ab0ce9a991556b3` | dead-code | unused-parameter | runtime_proof (runtime) | ok | ok | ok |
| `dead-code/catalog-phpstan-958a009704557ee9b44f` | dead-code | unused-parameter | runtime_proof (runtime) | ok | ok | ok |
| `dead-code/catalog-psalm-2e01e321c4dcfa1729a2` | dead-code | RedundantCast | runtime_proof (runtime) | ok | **FN** <sub>missing required diagnostic(s): cast.useless</sub> | ok |
| `dead-code/finally-assignment-always-runs` | dead-code | constant-condition | runtime_proof (runtime) | ok | **FP** <sub>unexpected diagnostic(s): ternary.alwaysFalse@25</sub> | ok |
| `enums/catalog-mago-c0921366ed9477f63e10` | enums | method.notFound | runtime_proof (runtime) | ok | ok | ok |
| `enums/catalog-phpstan-50e5714f7332b2d3a4ff` | enums | return.type | runtime_proof (runtime) | ok | ok | ok |
| `enums/catalog-phpstan-5cca931b9e656814c244` | enums | return.type | runtime_proof (runtime) | ok | ok | ok |
| `enums/catalog-psalm-c013f91ca882f9f18a36` | enums | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-invalid-argument@8</sub> | ok | ok |
| `enums/match-not-exhaustive` | enums | match.unhandled | runtime_proof (runtime) | ok | ok | ok |
| `enums/try-from-result-nullability` | enums | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-null-argument@20</sub> | ok | **FP** <sub>unexpected diagnostic(s): PossiblyNullArgument@20</sub> |
| `generics/catalog-mago-5fcd56c1b41c11a4f222` | generics | missing-template-parameter | upstream_docs (runtime) | ok | ok | ok |
| `generics/catalog-phpstan-23069a8fe555fc224d34` | generics | return.type | runtime_proof (runtime) | ok | ok | ok |
| `generics/catalog-phpstan-28d71ec402e5aaedb00e` | generics | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): invalid-return-statement@10, invalid-return…</sub> | ok | **FP** <sub>unexpected diagnostic(s): InvalidArrayOffset@10, LessSpecificReturnSt…</sub> |
| `generics/catalog-phpstan-d2ee700fdda5c0e356e9` | generics | return.type | runtime_proof (runtime) | ok | ok | **FP** <sub>unexpected diagnostic(s): MixedReturnStatement@11</sub> |
| `generics/catalog-phpstan-d88a0707d9479f04b2ed` | generics | return.type | runtime_proof (runtime) | ok | ok | ok |
| `generics/catalog-psalm-a8cb5b46f221852f2145` | generics | InvalidDocblock | upstream_docs (runtime) | ok | ok | **FN** <sub>missing required diagnostic(s): InvalidDocblock</sub> |
| `generics/catalog-psalm-af4807bea53ac80a15c3` | generics | return.type | runtime_proof (runtime) | ok | ok | ok |
| `generics/class-template-substitution-member-type` | generics | undefined-method | runtime_proof (runtime) | ok | ok | ok |
| `generics/covariant-template-in-write-position` | generics | template-variance-violation | runtime_proof (runtime) | ok | ok | ok |
| `generics/template-bound-violation` | generics | template-constraint-violation | runtime_proof (runtime) | ok | ok | ok |
| `generics/template-inference-from-argument` | generics | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `legacy-patterns/array-filter-string-callable-loses-list` | legacy-patterns | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `legacy-patterns/catalog-mago-af46b0f735b875e1a546` | legacy-patterns | undefined-variable | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): invalid-iterator@10, mixed-argument@10, mix…</sub> | ok | ok |
| `legacy-patterns/catalog-mago-ea6e3e02fc81b5208281` | legacy-patterns | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `legacy-patterns/catalog-psalm-6c129980869ba963c7aa` | legacy-patterns | property.notFound | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): non-existent-property@7</sub> | **FP** <sub>unexpected diagnostic(s): property.notFound@7</sub> | **FP** <sub>unexpected diagnostic(s): UndefinedPropertyAssignment@7</sub> |
| `legacy-patterns/count-on-iterable` | legacy-patterns | argument.type | runtime_proof (runtime) | ok | ok | **FN** <sub>missing required diagnostic(s): PossiblyInvalidArgument</sub> |
| `legacy-patterns/loose-comparison-with-zero` | legacy-patterns | impossible-condition | runtime_proof (runtime) | ok | ok | **FN** <sub>missing required diagnostic(s): TypeDoesNotContainType</sub> |
| `narrowing/catalog-mago-011e4b9469d7500de1f2` | narrowing | possibly-undefined-variable | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-1b312aa116cfe2b77850` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-213d169182afe4bafef8` | narrowing | method.notFound | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-28273499247a04f959b8` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-3c721332594e39bdab90` | narrowing | redundant-condition | runtime_proof (runtime) | ok | **FN** <sub>missing required diagnostic(s): if.alwaysTrue</sub> | ok |
| `narrowing/catalog-mago-43b57ad31a5d31bb2f4d` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-48e2336d00fe4ea5a90e` | narrowing | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-7d48310c1ee3d27f86fb` | narrowing | possibly-undefined-variable | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-a46fe274608e52136bea` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-ac60f1cdd2c628cc61fc` | narrowing | method.notFound | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-e5b2d1e6e25c64063071` | narrowing | possibly-undefined-variable | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-e65aa880dfdaf921f063` | narrowing | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-mago-ea8b8b0683bd66f27f4f` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0` | narrowing | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): less-specific-return-statement@6</sub> | ok | **FP** <sub>unexpected diagnostic(s): LessSpecificReturnStatement@6, MoreSpecific…</sub> |
| `narrowing/catalog-phpstan-2a3506b6815e78d94aa5` | narrowing | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): mixed-return-statement@10</sub> | **FP** <sub>unexpected diagnostic(s): return.type@10</sub> | **FP** <sub>unexpected diagnostic(s): MixedReturnStatement@10</sub> |
| `narrowing/catalog-phpstan-51152d85f829e8534475` | narrowing | return.type | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-phpstan-912f700441dc19e2b58b` | narrowing | return.type | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/catalog-psalm-924aac46207f32ed8ed5` | narrowing | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): invalid-return-statement@7</sub> | ok | ok |
| `narrowing/catalog-psalm-cd294fcb8e014ab18e3e` | narrowing | impossible-condition | runtime_proof (runtime) | **FP+FN** <sub>missing impossible-condition; unexpected redundant-docblock-type@7</sub> | **FN** <sub>missing required diagnostic(s): function.impossibleType</sub> | **FP+FN** <sub>missing TypeDoesNotContainType; unexpected UnsafeInstantiation@8</sub> |
| `narrowing/catalog-psalm-de14e6754f8edfa65da8` | narrowing | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): unknown-class-instantiation@5</sub> | ok | **FP** <sub>unexpected diagnostic(s): MixedMethodCall@5</sub> |
| `narrowing/is-bool-guard-excludes-true` | narrowing | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/is-int-on-string` | narrowing | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/is-numeric-after-is-int` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/is-numeric-guard-excludes-int` | narrowing | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/negated-instanceof-unrelated-class` | narrowing | impossible-condition | runtime_proof (runtime) | n/a | ok | ok |
| `narrowing/object-is-always-truthy` | narrowing | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/redundant-instanceof-in-condition` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/redundant-instanceof-on-declared-class` | narrowing | redundant-condition | runtime_proof (runtime) | n/a | ok | n/a |
| `nullability/catalog-mago-099feb9408203b5d7167` | nullability | possibly-null-method-call | runtime_proof (runtime) | ok | ok | ok |
| `nullability/catalog-mago-12192c3c16be73f35ba7` | nullability | possibly-null-property-fetch | runtime_proof (runtime) | ok | ok | ok |
| `nullability/catalog-phpstan-0f19731e70a569c020bd` | nullability | return.type | runtime_proof | skip | skip | skip |
| `nullability/catalog-phpstan-306c280bb8a6ca46a961` | nullability | return.type | runtime_proof (runtime) | ok | ok | **FP** <sub>unexpected diagnostic(s): InvalidReturnStatement@13, InvalidReturnTyp…</sub> |
| `nullability/catalog-phpstan-3df7186a1b833d024d52` | nullability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): falsable-return-statement@5, invalid-return…</sub> | **FP** <sub>unexpected diagnostic(s): return.type@5</sub> | **FP** <sub>unexpected diagnostic(s): FalsableReturnStatement@5, InvalidFalsableR…</sub> |
| `nullability/catalog-phpstan-3ecb74a1fba6668eac61` | nullability | return.type | runtime_proof (runtime) | ok | ok | **FP** <sub>unexpected diagnostic(s): LessSpecificReturnStatement@7, MoreSpecific…</sub> |
| `nullability/catalog-phpstan-5588ff8af852e7139b7d` | nullability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-null-property-access@6</sub> | ok | ok |
| `nullability/catalog-phpstan-5d813bb8b104d0c619ca` | nullability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possible-method-access-on-null@5</sub> | ok | **FP** <sub>unexpected diagnostic(s): MixedReturnStatement@7, PossiblyNullReferen…</sub> |
| `nullability/catalog-phpstan-68486e793e9b077839dc` | nullability | return.type | runtime_proof (runtime) | ok | ok | ok |
| `nullability/catalog-phpstan-ccdd6746fb9cf55bd2d7` | nullability | return.type | runtime_proof (runtime) | ok | ok | ok |
| `nullability/catalog-phpstan-d1f39552939e65fa35c3` | nullability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): falsable-return-statement@4, invalid-return…</sub> | ok | **FP** <sub>unexpected diagnostic(s): FalsableReturnStatement@4, InvalidFalsableR…</sub> |
| `nullability/catalog-phpstan-f1455a36807cc2badc75` | nullability | return.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-null-property-access@10</sub> | ok | ok |
| `nullability/catalog-psalm-b832ee21bb9a15b5e6bc` | nullability | method.nonObject | runtime_proof (runtime) | ok | ok | ok |
| `nullability/catalog-psalm-c517a982a06f57ea084b` | nullability | return.type | runtime_proof (runtime) | **FN** <sub>missing required diagnostic(s): invalid-return-statement</sub> | **FN** <sub>missing required diagnostic(s): return.type</sub> | **FN** <sub>missing required diagnostic(s): NullableReturnStatement</sub> |
| `nullability/catalog-psalm-fe044cea9130c52f9d28` | nullability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `nullability/elseif-else-return-keeps-possible-null` | nullability | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `nullability/is-null-guard-narrows-away-null` | nullability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `nullability/loose-null-guard-keeps-empty-string` | nullability | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `nullability/relational-comparison-excludes-null` | nullability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `phpdoc-extensions/catalog-mago-d86bc7b7eabe71006e0c` | phpdoc-extensions | invalid-docblock | upstream_docs (runtime) | **FN** <sub>missing required diagnostic(s): invalid-docblock</sub> | ok | ok |
| `phpdoc-extensions/catalog-phpstan-7009f55abd4d6861610f` | phpdoc-extensions | return.type | runtime_proof (runtime) | ok | ok | ok |
| `phpdoc-extensions/catalog-phpstan-e134f5937b2ca742f51c` | phpdoc-extensions | return.type | runtime_proof (runtime) | ok | ok | ok |
| `phpdoc-extensions/catalog-psalm-046e3c888eee140464f5` | phpdoc-extensions | InvalidDocblock | upstream_docs (runtime) | ok | ok | ok |
| `phpdoc-extensions/catalog-psalm-06716895300af389cfc9` | phpdoc-extensions | InvalidDocblock | upstream_test (runtime) | ok | ok | ok |
| `phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da` | phpdoc-extensions | InvalidDocblock | upstream_docs (runtime) | **FN** <sub>missing required diagnostic(s): invalid-docblock</sub> | **FN** <sub>missing required diagnostic(s): typeAlias.invalidType</sub> | ok |
| `phpdoc-extensions/catalog-psalm-3cb038acaec155a5e87e` | phpdoc-extensions | InvalidDocblock | upstream_docs (runtime) | ok | ok | ok |
| `phpdoc-extensions/catalog-psalm-53ae3931e59580d6f84c` | phpdoc-extensions | NamedArgumentNotAllowed | upstream_docs (runtime) | ok | ok | **FP** <sub>unexpected diagnostic(s): InvalidArgument@8</sub> |
| `phpdoc-extensions/catalog-psalm-604771ba27ab94845cc5` | phpdoc-extensions | property.defaultValue | runtime_proof (runtime) | ok | ok | ok |
| `phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3` | phpdoc-extensions | InvalidDocblock | upstream_docs (runtime) | **FN** <sub>missing required diagnostic(s): invalid-docblock</sub> | **FN** <sub>missing required diagnostic(s): /(?i)(duplicat.*@return|@return.*(dup…</sub> | ok |
| `phpdoc-extensions/catalog-psalm-a02980c52843949bdecb` | phpdoc-extensions | InvalidDocblock | upstream_docs (runtime) | **FN** <sub>missing required diagnostic(s): invalid-docblock</sub> | **FN** <sub>missing required diagnostic(s): phpDoc.duplicateTag</sub> | ok |
| `phpdoc-extensions/catalog-psalm-a589cd9fbab7175a992d` | phpdoc-extensions | NamedArgumentNotAllowed | upstream_docs (runtime) | ok | ok | ok |

Legend: `ok` matches the case, **FP** false positive, **FN** false negative, `n/a` by-design divergence, `ERR` tool error, `BAD` invalid case, `skip` not applicable.
