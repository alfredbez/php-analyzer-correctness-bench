# Correctness summary

- Run: `2026-10-18T06-56-24Z-factory-2`
- Started: 2026-10-18T06:56:24Z (UTC)
- phpstan: PHPStan - PHP Static Analysis Tool 2.3.1
- psalm: Psalm 6.20.0@804f03c0c183d149fcd4b8c7c0c9b3fbf836d34c
- mago: mago 1.57.0
- PHP: 8.3.35
- Cases: 18 (valid: 18)
- Runtime checks passed: 18/18

`agreement` = ok / judged, where judged = ok + false positives + false negatives + mixed. By-design divergences, tool errors, case errors and skips are excluded and listed separately.

| Tool | Cases | Judged | ok | FP | FN | mixed | by-design | tool error | case error | skipped | agreement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mago | 18 | 16 | 12 | 4 | 0 | 0 | 2 | 0 | 0 | 0 | 75.0% |
| phpstan | 18 | 18 | 17 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 94.4% |
| psalm | 18 | 17 | 15 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 88.2% |

## Per domain

| Domain | Tool | Cases | ok | FP | FN | by-design |
| --- | --- | --- | --- | --- | --- | --- |
| callables | mago | 2 | 0 | 2 | 0 | 0 |
| dead-code | mago | 1 | 1 | 0 | 0 | 0 |
| legacy-patterns | mago | 3 | 3 | 0 | 0 | 0 |
| narrowing | mago | 8 | 6 | 0 | 0 | 2 |
| nullability | mago | 4 | 2 | 2 | 0 | 0 |
| callables | phpstan | 2 | 2 | 0 | 0 | 0 |
| dead-code | phpstan | 1 | 0 | 1 | 0 | 0 |
| legacy-patterns | phpstan | 3 | 3 | 0 | 0 | 0 |
| narrowing | phpstan | 8 | 8 | 0 | 0 | 0 |
| nullability | phpstan | 4 | 4 | 0 | 0 | 0 |
| callables | psalm | 2 | 2 | 0 | 0 | 0 |
| dead-code | psalm | 1 | 1 | 0 | 0 | 0 |
| legacy-patterns | psalm | 3 | 1 | 0 | 2 | 0 |
| narrowing | psalm | 8 | 7 | 0 | 0 | 1 |
| nullability | psalm | 4 | 4 | 0 | 0 | 0 |

## Recorded by-design divergences

| Case | Tool | Reason | Citation |
| --- | --- | --- | --- |
| `narrowing/negated-instanceof-unrelated-class` | mago | Mago 1.57.0 analyzes a bare return as an expression. Unary Not negates the inferred instanceof result but does not invoke conditional diagnostics or assertion reconciliation. Its silence here is outside this warning's reporting scope; impossible instanceof conditions remain supported and must be tested separately. | https://github.com/carthage-software/mago/blob/1.57.0/crates/analyzer/src/expression/unary.rs#L86-L106 |
| `narrowing/redundant-instanceof-on-declared-class` | mago | Mago 1.57.0 infers literal true for this subtype test but does not emit redundant-condition on a bare returned instanceof. Its own parent-class fixture permits this expression without a diagnostic. Missing a warning here is a reporting-scope divergence, not failed subtype reasoning. | https://github.com/carthage-software/mago/blob/1.57.0/crates/analyzer/tests/cases/inheritance_instanceof_parent_class.php#L5-L17 |
| `narrowing/redundant-instanceof-on-declared-class` | psalm | Psalm 6.20.0 does not require RedundantCondition on a bare returned instanceof expression. Its standalone InstanceofAnalyzer assigns bool; conditional reconciliation is a separate reporting context. This exclusion concerns warning scope, not whether the expression is semantically always true. | https://github.com/vimeo/psalm/blob/6.20.0/src/Psalm/Internal/Analyzer/Statements/Expression/InstanceofAnalyzer.php#L25-L100 |
