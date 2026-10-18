# Mago version comparison

Same-case correctness measurements, not a speed benchmark or general quality ranking.

Not every expectation is desirable for every tool. FP/FN mean disagreement with the declared baseline, including warning-policy differences. External reproducers and corrections are welcome.

| Profile | Observed version | Source | ok / judged | FP | FN | mixed | excluded |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mago 1.54.0 | mago 1.54.0 | `1.54.0` | 89 / 139 | 39 | 10 | 1 | 3 |
| Mago 1.57.0 · stable | mago 1.57.0 | `1.57.0` | 95 / 139 | 34 | 9 | 1 | 3 |
| Mago main · bbabf3395981 | mago 1.57.0 | `bbabf3395981ace80b8043f9020c4f28d8a9a4b3` | 104 / 139 | 25 | 8 | 2 | 3 |

## historical → stable

| Case | Before | After | Transition |
| --- | --- | --- | --- |
| `arrays/catalog-mago-aa06b37e787d640d9565` | false_positive | false_positive | still_open |
| `arrays/catalog-phpstan-3df530270084e3d904a0` | false_positive | false_positive | still_open |
| `arrays/catalog-phpstan-d438454d94600dcbba53` | false_positive | false_positive | still_open |
| `arrays/catalog-psalm-13be39b2d9591fa1a9e5` | false_negative | false_negative | still_open |
| `arrays/catalog-psalm-540e6672f974be8ec019` | false_negative | false_negative | still_open |
| `arrays/catalog-psalm-59b1c78bfa12967fb1ac` | false_negative | false_negative | still_open |
| `arrays/numeric-string-array-key` | false_positive | false_positive | still_open |
| `arrays/strict-in-array-narrowing` | false_positive | false_positive | still_open |
| `assignability/catalog-mago-70af4f68103648de14b8` | false_positive | false_positive | still_open |
| `assignability/catalog-mago-ddd6d489f1173eabbd99` | false_positive | false_positive | still_open |
| `assignability/catalog-phpstan-abc5fa1b77dc14531ca8` | false_positive | false_positive | still_open |
| `assignability/catalog-psalm-0e66d52886bd21db7846` | false_positive | false_positive | still_open |
| `assignability/catalog-psalm-5489e87365002fea3494` | false_positive | false_positive | still_open |
| `callables/catalog-mago-1e0010ad90cf2846677d` | false_positive | false_positive | still_open |
| `callables/catalog-phpstan-554b2c43131257c0d354` | false_positive | false_positive | still_open |
| `callables/catalog-phpstan-6931357e80bcf4ac18ca` | false_positive | false_positive | still_open |
| `callables/catalog-phpstan-71ff2ec3ba7e1627cfa7` | false_positive | false_positive | still_open |
| `callables/is-object-on-callable-parameter` | false_positive | false_positive | still_open |
| `callables/negated-is-callable-removes-function-name` | false_positive | false_positive | still_open |
| `dead-code/catalog-mago-c0e93f2edb2c2610c6e8` | false_negative | false_negative | still_open |
| `enums/catalog-mago-c0921366ed9477f63e10` | false_positive | ok | fixed |
| `enums/catalog-psalm-c013f91ca882f9f18a36` | false_positive | false_positive | still_open |
| `enums/try-from-result-nullability` | false_positive | false_positive | still_open |
| `generics/catalog-mago-5fcd56c1b41c11a4f222` | false_positive | ok | fixed |
| `generics/catalog-phpstan-28d71ec402e5aaedb00e` | false_positive | false_positive | still_open |
| `legacy-patterns/catalog-mago-af46b0f735b875e1a546` | false_positive | false_positive | still_open |
| `legacy-patterns/catalog-psalm-6c129980869ba963c7aa` | false_positive | false_positive | still_open |
| `narrowing/catalog-mago-213d169182afe4bafef8` | false_positive | false_positive | still_open |
| `narrowing/catalog-mago-3c721332594e39bdab90` | false_negative | ok | fixed |
| `narrowing/catalog-mago-48e2336d00fe4ea5a90e` | false_positive | false_positive | still_open |
| `narrowing/catalog-mago-7d48310c1ee3d27f86fb` | false_negative | ok | fixed |
| `narrowing/catalog-mago-ac60f1cdd2c628cc61fc` | false_positive | ok | fixed |
| `narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0` | false_positive | false_positive | still_open |
| `narrowing/catalog-phpstan-2a3506b6815e78d94aa5` | false_positive | false_positive | still_open |
| `narrowing/catalog-psalm-924aac46207f32ed8ed5` | false_positive | false_positive | still_open |
| `narrowing/catalog-psalm-cd294fcb8e014ab18e3e` | mixed | mixed | still_open |
| `narrowing/catalog-psalm-de14e6754f8edfa65da8` | false_positive | false_positive | still_open |
| `narrowing/negated-instanceof-unrelated-class` | divergence | divergence | not_comparable |
| `narrowing/redundant-instanceof-on-declared-class` | divergence | divergence | not_comparable |
| `nullability/catalog-phpstan-0f19731e70a569c020bd` | skipped | skipped | not_comparable |
| `nullability/catalog-phpstan-3df7186a1b833d024d52` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-5588ff8af852e7139b7d` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-5d813bb8b104d0c619ca` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-d1f39552939e65fa35c3` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-f1455a36807cc2badc75` | false_positive | false_positive | still_open |
| `nullability/catalog-psalm-b832ee21bb9a15b5e6bc` | false_positive | ok | fixed |
| `nullability/catalog-psalm-c517a982a06f57ea084b` | false_positive | false_negative | still_open |
| `nullability/elseif-else-return-keeps-possible-null` | false_positive | false_positive | still_open |
| `nullability/loose-null-guard-keeps-empty-string` | false_positive | false_positive | still_open |
| `phpdoc-extensions/catalog-mago-d86bc7b7eabe71006e0c` | false_negative | false_negative | still_open |
| `phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da` | false_negative | false_negative | still_open |
| `phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3` | false_negative | false_negative | still_open |
| `phpdoc-extensions/catalog-psalm-a02980c52843949bdecb` | false_negative | false_negative | still_open |

## stable → main

| Case | Before | After | Transition |
| --- | --- | --- | --- |
| `arrays/catalog-mago-aa06b37e787d640d9565` | false_positive | ok | fixed |
| `arrays/catalog-phpstan-3df530270084e3d904a0` | false_positive | false_positive | still_open |
| `arrays/catalog-phpstan-d438454d94600dcbba53` | false_positive | false_positive | still_open |
| `arrays/catalog-psalm-13be39b2d9591fa1a9e5` | false_negative | false_negative | still_open |
| `arrays/catalog-psalm-540e6672f974be8ec019` | false_negative | false_negative | still_open |
| `arrays/catalog-psalm-59b1c78bfa12967fb1ac` | false_negative | false_negative | still_open |
| `arrays/numeric-string-array-key` | false_positive | ok | fixed |
| `arrays/strict-in-array-narrowing` | false_positive | ok | fixed |
| `assignability/catalog-mago-70af4f68103648de14b8` | false_positive | ok | fixed |
| `assignability/catalog-mago-ddd6d489f1173eabbd99` | false_positive | ok | fixed |
| `assignability/catalog-phpstan-abc5fa1b77dc14531ca8` | false_positive | false_positive | still_open |
| `assignability/catalog-psalm-0e66d52886bd21db7846` | false_positive | false_positive | still_open |
| `assignability/catalog-psalm-5489e87365002fea3494` | false_positive | false_positive | still_open |
| `callables/catalog-mago-1e0010ad90cf2846677d` | false_positive | ok | fixed |
| `callables/catalog-phpstan-554b2c43131257c0d354` | false_positive | false_positive | still_open |
| `callables/catalog-phpstan-6931357e80bcf4ac18ca` | false_positive | false_positive | still_open |
| `callables/catalog-phpstan-71ff2ec3ba7e1627cfa7` | false_positive | false_positive | still_open |
| `callables/is-object-on-callable-parameter` | false_positive | ok | fixed |
| `callables/negated-is-callable-removes-function-name` | false_positive | ok | fixed |
| `dead-code/catalog-mago-c0e93f2edb2c2610c6e8` | false_negative | mixed | still_open |
| `enums/catalog-psalm-c013f91ca882f9f18a36` | false_positive | false_positive | still_open |
| `enums/try-from-result-nullability` | false_positive | false_positive | still_open |
| `generics/catalog-phpstan-28d71ec402e5aaedb00e` | false_positive | false_positive | still_open |
| `legacy-patterns/catalog-mago-af46b0f735b875e1a546` | false_positive | false_positive | still_open |
| `legacy-patterns/catalog-psalm-6c129980869ba963c7aa` | false_positive | false_positive | still_open |
| `narrowing/catalog-mago-213d169182afe4bafef8` | false_positive | ok | fixed |
| `narrowing/catalog-mago-48e2336d00fe4ea5a90e` | false_positive | false_positive | still_open |
| `narrowing/catalog-mago-ac60f1cdd2c628cc61fc` | ok | false_positive | regressed |
| `narrowing/catalog-phpstan-13d11cb24c0ac0aec4c0` | false_positive | false_positive | still_open |
| `narrowing/catalog-phpstan-2a3506b6815e78d94aa5` | false_positive | false_positive | still_open |
| `narrowing/catalog-psalm-924aac46207f32ed8ed5` | false_positive | false_positive | still_open |
| `narrowing/catalog-psalm-cd294fcb8e014ab18e3e` | mixed | mixed | still_open |
| `narrowing/catalog-psalm-de14e6754f8edfa65da8` | false_positive | false_positive | still_open |
| `narrowing/negated-instanceof-unrelated-class` | divergence | divergence | not_comparable |
| `narrowing/redundant-instanceof-on-declared-class` | divergence | divergence | not_comparable |
| `nullability/catalog-phpstan-0f19731e70a569c020bd` | skipped | skipped | not_comparable |
| `nullability/catalog-phpstan-3df7186a1b833d024d52` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-5588ff8af852e7139b7d` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-5d813bb8b104d0c619ca` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-d1f39552939e65fa35c3` | false_positive | false_positive | still_open |
| `nullability/catalog-phpstan-f1455a36807cc2badc75` | false_positive | false_positive | still_open |
| `nullability/catalog-psalm-c517a982a06f57ea084b` | false_negative | false_negative | still_open |
| `nullability/elseif-else-return-keeps-possible-null` | false_positive | false_positive | still_open |
| `nullability/loose-null-guard-keeps-empty-string` | false_positive | ok | fixed |
| `phpdoc-extensions/catalog-mago-d86bc7b7eabe71006e0c` | false_negative | false_negative | still_open |
| `phpdoc-extensions/catalog-psalm-2d4ae8911311e23b45da` | false_negative | false_negative | still_open |
| `phpdoc-extensions/catalog-psalm-7a3fdc7ca8bd3d5091c3` | false_negative | false_negative | still_open |
| `phpdoc-extensions/catalog-psalm-a02980c52843949bdecb` | false_negative | false_negative | still_open |

Benchmark expectations have not been submitted for maintainer agreement.
