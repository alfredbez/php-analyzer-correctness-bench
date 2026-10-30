# Correctness summary

- Run: `stable`
- Started: 2026-10-30T16:18:21Z (UTC)
- phpstan: PHPStan - PHP Static Analysis Tool 2.3.1
- psalm: Psalm 6.20.1@376425b8e67b79773add388e16b4f6be5693dc87
- mago: mago 1.59.0
- PHP: 8.3.36
- Cases: 144 (valid: 144)
- Runtime checks passed: 142/144

`agreement` = ok / judged, where judged = ok + false positives + false negatives + mixed. By-design divergences, tool errors, case errors and skips are excluded and listed separately.

| Tool | Cases | Judged | ok | FP | FN | mixed | by-design | tool error | case error | skipped | agreement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mago | 144 | 140 | 108 | 22 | 9 | 1 | 2 | 0 | 0 | 2 | 77.1% |
| phpstan | 144 | 140 | 127 | 4 | 9 | 0 | 2 | 0 | 0 | 2 | 90.7% |
| psalm | 144 | 141 | 115 | 18 | 7 | 1 | 1 | 0 | 0 | 2 | 81.6% |

## Per domain

| Domain | Tool | Cases | ok | FP | FN | by-design |
| --- | --- | --- | --- | --- | --- | --- |
| arrays | mago | 22 | 17 | 2 | 3 | 0 |
| assignability | mago | 22 | 17 | 3 | 1 | 0 |
| callables | mago | 12 | 9 | 3 | 0 | 0 |
| dead-code | mago | 6 | 6 | 0 | 0 | 0 |
| enums | mago | 6 | 4 | 2 | 0 | 0 |
| generics | mago | 11 | 10 | 1 | 0 | 0 |
| legacy-patterns | mago | 6 | 4 | 2 | 0 | 0 |
| narrowing | mago | 28 | 21 | 4 | 0 | 2 |
| nullability | mago | 19 | 12 | 5 | 1 | 0 |
| phpdoc-extensions | mago | 12 | 8 | 0 | 4 | 0 |
| arrays | phpstan | 22 | 20 | 0 | 1 | 1 |
| assignability | phpstan | 22 | 20 | 0 | 0 | 1 |
| callables | phpstan | 12 | 12 | 0 | 0 | 0 |
| dead-code | phpstan | 6 | 3 | 1 | 2 | 0 |
| enums | phpstan | 6 | 6 | 0 | 0 | 0 |
| generics | phpstan | 11 | 11 | 0 | 0 | 0 |
| legacy-patterns | phpstan | 6 | 5 | 1 | 0 | 0 |
| narrowing | phpstan | 28 | 25 | 1 | 2 | 0 |
| nullability | phpstan | 19 | 16 | 1 | 1 | 0 |
| phpdoc-extensions | phpstan | 12 | 9 | 0 | 3 | 0 |
| arrays | psalm | 22 | 19 | 1 | 2 | 0 |
| assignability | psalm | 22 | 20 | 1 | 0 | 0 |
| callables | psalm | 12 | 9 | 3 | 0 | 0 |
| dead-code | psalm | 6 | 5 | 0 | 1 | 0 |
| enums | psalm | 6 | 5 | 1 | 0 | 0 |
| generics | psalm | 11 | 8 | 2 | 1 | 0 |
| legacy-patterns | psalm | 6 | 3 | 1 | 2 | 0 |
| narrowing | psalm | 28 | 23 | 3 | 0 | 1 |
| nullability | psalm | 19 | 12 | 5 | 1 | 0 |
| phpdoc-extensions | psalm | 12 | 11 | 1 | 0 | 0 |

## Recorded by-design divergences

| Case | Tool | Reason | Citation |
| --- | --- | --- | --- |
| `narrowing/negated-instanceof-unrelated-class` | mago | Mago 1.57.0 analyzes a bare return as an expression. Unary Not negates the inferred instanceof result but does not invoke conditional diagnostics or assertion reconciliation. Its silence here is outside this warning's reporting scope; impossible instanceof conditions remain supported and must be tested separately. | https://github.com/carthage-software/mago/blob/1.57.0/crates/analyzer/src/expression/unary.rs#L86-L106 |
| `narrowing/redundant-instanceof-on-declared-class` | mago | Mago 1.57.0 infers literal true for this subtype test but does not emit redundant-condition on a bare returned instanceof. Its own parent-class fixture permits this expression without a diagnostic. Missing a warning here is a reporting-scope divergence, not failed subtype reasoning. | https://github.com/carthage-software/mago/blob/1.57.0/crates/analyzer/tests/cases/inheritance_instanceof_parent_class.php#L5-L17 |
| `arrays/array-key-for-string-key` | phpstan | PHPStan explicitly defines array-key as a permissive benevolent union rather than a strictly checked int|string alias. ArrayType normalizes that key to implicit mixed, and this baseline level-9 configuration leaves checkImplicitMixed disabled. Silence is therefore an excluded documented configuration-scope difference. An independent check with checkImplicitMixed: true emits argument.type on the unchanged fixture; the rule is implemented. | https://phpstan.org/config-reference#checkbenevolentuniontypes |
| `assignability/docblock-return-covariance` | phpstan | In this baseline configuration PHPStan deliberately suppresses maybe-compatible PHPDoc override checks: reportMaybesInMethodSignatures defaults to false. MethodSignatureRule emits method.childReturnType for this widening only with that optional flag enabled. This is an excluded configuration-scope difference, not evidence that PHPStan lacks the rule. | https://github.com/phpstan/phpstan-src/blob/2c12dac5e4f8626c8a7cfc0b4bb9c5ce48d37c96/src/Rules/Methods/MethodSignatureRule.php#L115-L131 |
| `narrowing/redundant-instanceof-on-declared-class` | psalm | Psalm 6.20.0 does not require RedundantCondition on a bare returned instanceof expression. Its standalone InstanceofAnalyzer assigns bool; conditional reconciliation is a separate reporting context. This exclusion concerns warning scope, not whether the expression is semantically always true. | https://github.com/vimeo/psalm/blob/6.20.0/src/Psalm/Internal/Analyzer/Statements/Expression/InstanceofAnalyzer.php#L25-L100 |
