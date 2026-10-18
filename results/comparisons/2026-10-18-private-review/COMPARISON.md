# Mago version comparison

Same-case correctness measurements, not a speed benchmark or general quality ranking.

| Profile | Observed version | Source | ok / judged | FP | FN | mixed | excluded |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mago 1.54.0 | mago 1.54.0 | `1.54.0` | 17 / 24 | 7 | 0 | 0 | 2 |
| Mago 1.57.0 · stable | mago 1.57.0 | `1.57.0` | 17 / 24 | 7 | 0 | 0 | 2 |
| Mago main · bbabf3395981 | mago 1.57.0 | `bbabf3395981ace80b8043f9020c4f28d8a9a4b3` | 22 / 24 | 2 | 0 | 0 | 2 |

## historical → stable

| Case | Before | After | Transition |
| --- | --- | --- | --- |
| `arrays/numeric-string-array-key` | false_positive | false_positive | still_open |
| `arrays/strict-in-array-narrowing` | false_positive | false_positive | still_open |
| `callables/is-object-on-callable-parameter` | false_positive | false_positive | still_open |
| `callables/negated-is-callable-removes-function-name` | false_positive | false_positive | still_open |
| `enums/try-from-result-nullability` | false_positive | false_positive | still_open |
| `narrowing/negated-instanceof-unrelated-class` | divergence | divergence | not_comparable |
| `narrowing/redundant-instanceof-on-declared-class` | divergence | divergence | not_comparable |
| `nullability/elseif-else-return-keeps-possible-null` | false_positive | false_positive | still_open |
| `nullability/loose-null-guard-keeps-empty-string` | false_positive | false_positive | still_open |

## stable → main

| Case | Before | After | Transition |
| --- | --- | --- | --- |
| `arrays/numeric-string-array-key` | false_positive | ok | fixed |
| `arrays/strict-in-array-narrowing` | false_positive | ok | fixed |
| `callables/is-object-on-callable-parameter` | false_positive | ok | fixed |
| `callables/negated-is-callable-removes-function-name` | false_positive | ok | fixed |
| `enums/try-from-result-nullability` | false_positive | false_positive | still_open |
| `narrowing/negated-instanceof-unrelated-class` | divergence | divergence | not_comparable |
| `narrowing/redundant-instanceof-on-declared-class` | divergence | divergence | not_comparable |
| `nullability/elseif-else-return-keeps-possible-null` | false_positive | false_positive | still_open |
| `nullability/loose-null-guard-keeps-empty-string` | false_positive | ok | fixed |

Benchmark expectations have not been submitted for maintainer agreement.
