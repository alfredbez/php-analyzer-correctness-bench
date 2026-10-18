# Correctness matrix

| Case | Domain | Rule class | Ground truth | mago | phpstan | psalm |
| --- | --- | --- | --- | --- | --- | --- |
| `arrays/array-key-for-string-key` | arrays | argument.type | runtime_proof (runtime) | ok | **FN** <sub>missing required diagnostic(s): argument.type</sub> | ok |
| `arrays/numeric-string-array-key` | arrays | impossible-condition | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): impossible-condition@12, no-value@17</sub> | ok | ok |
| `arrays/scalar-array-for-string-array` | arrays | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `arrays/strict-in-array-narrowing` | arrays | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-invalid-argument@17</sub> | ok | ok |
| `assignability/callable-not-closure` | assignability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `assignability/docblock-return-covariance` | assignability | method.childReturnType | runtime_proof (runtime) | ok | n/a | ok |
| `callables/is-object-on-callable-parameter` | callables | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): impossible-condition@24, impossible-type-co…</sub> | ok | ok |
| `callables/negated-is-callable-removes-function-name` | callables | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-invalid-argument@24</sub> | ok | ok |
| `dead-code/finally-assignment-always-runs` | dead-code | constant-condition | runtime_proof (runtime) | ok | **FP** <sub>unexpected diagnostic(s): ternary.alwaysFalse@25</sub> | ok |
| `enums/match-not-exhaustive` | enums | match.unhandled | runtime_proof (runtime) | ok | ok | ok |
| `enums/try-from-result-nullability` | enums | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-null-argument@20</sub> | ok | **FP** <sub>unexpected diagnostic(s): PossiblyNullArgument@20</sub> |
| `generics/template-bound-violation` | generics | template-constraint-violation | runtime_proof (runtime) | ok | ok | ok |
| `generics/template-inference-from-argument` | generics | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `legacy-patterns/array-filter-string-callable-loses-list` | legacy-patterns | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `legacy-patterns/count-on-iterable` | legacy-patterns | argument.type | runtime_proof (runtime) | ok | ok | **FN** <sub>missing required diagnostic(s): PossiblyInvalidArgument</sub> |
| `legacy-patterns/loose-comparison-with-zero` | legacy-patterns | impossible-condition | runtime_proof (runtime) | ok | ok | **FN** <sub>missing required diagnostic(s): TypeDoesNotContainType</sub> |
| `narrowing/is-bool-guard-excludes-true` | narrowing | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/is-int-on-string` | narrowing | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/is-numeric-after-is-int` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/is-numeric-guard-excludes-int` | narrowing | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/negated-instanceof-unrelated-class` | narrowing | impossible-condition | runtime_proof (runtime) | n/a | ok | ok |
| `narrowing/object-is-always-truthy` | narrowing | impossible-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/redundant-instanceof-in-condition` | narrowing | redundant-condition | runtime_proof (runtime) | ok | ok | ok |
| `narrowing/redundant-instanceof-on-declared-class` | narrowing | redundant-condition | runtime_proof (runtime) | n/a | ok | n/a |
| `nullability/elseif-else-return-keeps-possible-null` | nullability | redundant-condition | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): redundant-comparison@23</sub> | ok | ok |
| `nullability/is-null-guard-narrows-away-null` | nullability | argument.type | runtime_proof (runtime) | ok | ok | ok |
| `nullability/loose-null-guard-keeps-empty-string` | nullability | redundant-condition | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): redundant-comparison@15, redundant-conditio…</sub> | ok | ok |
| `nullability/relational-comparison-excludes-null` | nullability | argument.type | runtime_proof (runtime) | ok | ok | ok |

Legend: `ok` matches the case, **FP** false positive, **FN** false negative, `n/a` by-design divergence, `ERR` tool error, `BAD` invalid case, `skip` not applicable.
