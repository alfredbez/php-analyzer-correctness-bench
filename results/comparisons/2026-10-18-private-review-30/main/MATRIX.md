# Correctness matrix

| Case | Domain | Rule class | Ground truth | mago |
| --- | --- | --- | --- | --- |
| `arrays/array-key-for-string-key` | arrays | argument.type | runtime_proof (runtime) | ok |
| `arrays/numeric-string-array-key` | arrays | impossible-condition | runtime_proof (runtime) | ok |
| `arrays/scalar-array-for-string-array` | arrays | argument.type | runtime_proof (runtime) | ok |
| `arrays/strict-in-array-narrowing` | arrays | argument.type | runtime_proof (runtime) | ok |
| `assignability/callable-not-closure` | assignability | argument.type | runtime_proof (runtime) | ok |
| `assignability/docblock-return-covariance` | assignability | method.childReturnType | runtime_proof (runtime) | ok |
| `callables/is-object-on-callable-parameter` | callables | argument.type | runtime_proof (runtime) | ok |
| `callables/negated-is-callable-removes-function-name` | callables | argument.type | runtime_proof (runtime) | ok |
| `dead-code/finally-assignment-always-runs` | dead-code | constant-condition | runtime_proof (runtime) | ok |
| `enums/match-not-exhaustive` | enums | match.unhandled | runtime_proof (runtime) | ok |
| `enums/try-from-result-nullability` | enums | argument.type | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): possibly-null-argument@20</sub> |
| `generics/class-template-substitution-member-type` | generics | undefined-method | runtime_proof (runtime) | ok |
| `generics/covariant-template-in-write-position` | generics | template-variance-violation | runtime_proof (runtime) | ok |
| `generics/template-bound-violation` | generics | template-constraint-violation | runtime_proof (runtime) | ok |
| `generics/template-inference-from-argument` | generics | argument.type | runtime_proof (runtime) | ok |
| `legacy-patterns/array-filter-string-callable-loses-list` | legacy-patterns | argument.type | runtime_proof (runtime) | ok |
| `legacy-patterns/count-on-iterable` | legacy-patterns | argument.type | runtime_proof (runtime) | ok |
| `legacy-patterns/loose-comparison-with-zero` | legacy-patterns | impossible-condition | runtime_proof (runtime) | ok |
| `narrowing/is-bool-guard-excludes-true` | narrowing | argument.type | runtime_proof (runtime) | ok |
| `narrowing/is-int-on-string` | narrowing | impossible-condition | runtime_proof (runtime) | ok |
| `narrowing/is-numeric-after-is-int` | narrowing | redundant-condition | runtime_proof (runtime) | ok |
| `narrowing/is-numeric-guard-excludes-int` | narrowing | argument.type | runtime_proof (runtime) | ok |
| `narrowing/negated-instanceof-unrelated-class` | narrowing | impossible-condition | runtime_proof (runtime) | n/a |
| `narrowing/object-is-always-truthy` | narrowing | impossible-condition | runtime_proof (runtime) | ok |
| `narrowing/redundant-instanceof-in-condition` | narrowing | redundant-condition | runtime_proof (runtime) | ok |
| `narrowing/redundant-instanceof-on-declared-class` | narrowing | redundant-condition | runtime_proof (runtime) | n/a |
| `nullability/elseif-else-return-keeps-possible-null` | nullability | redundant-condition | runtime_proof (runtime) | **FP** <sub>unexpected diagnostic(s): redundant-comparison@23</sub> |
| `nullability/is-null-guard-narrows-away-null` | nullability | argument.type | runtime_proof (runtime) | ok |
| `nullability/loose-null-guard-keeps-empty-string` | nullability | redundant-condition | runtime_proof (runtime) | ok |
| `nullability/relational-comparison-excludes-null` | nullability | argument.type | runtime_proof (runtime) | ok |

Legend: `ok` matches the case, **FP** false positive, **FN** false negative, `n/a` by-design divergence, `ERR` tool error, `BAD` invalid case, `skip` not applicable.
