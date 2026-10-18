# Correctness summary

- Run: `historical`
- Started: 2026-10-18T11:36:32Z (UTC)
- mago: mago 1.54.0
- PHP: 8.3.35
- Cases: 26 (valid: 26)
- Runtime checks passed: 26/26

`agreement` = ok / judged, where judged = ok + false positives + false negatives + mixed. By-design divergences, tool errors, case errors and skips are excluded and listed separately.

| Tool | Cases | Judged | ok | FP | FN | mixed | by-design | tool error | case error | skipped | agreement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mago | 26 | 24 | 17 | 7 | 0 | 0 | 2 | 0 | 0 | 0 | 70.8% |

## Per domain

| Domain | Tool | Cases | ok | FP | FN | by-design |
| --- | --- | --- | --- | --- | --- | --- |
| arrays | mago | 2 | 0 | 2 | 0 | 0 |
| assignability | mago | 2 | 2 | 0 | 0 | 0 |
| callables | mago | 2 | 0 | 2 | 0 | 0 |
| dead-code | mago | 1 | 1 | 0 | 0 | 0 |
| enums | mago | 2 | 1 | 1 | 0 | 0 |
| generics | mago | 2 | 2 | 0 | 0 | 0 |
| legacy-patterns | mago | 3 | 3 | 0 | 0 | 0 |
| narrowing | mago | 8 | 6 | 0 | 0 | 2 |
| nullability | mago | 4 | 2 | 2 | 0 | 0 |

## Recorded by-design divergences

| Case | Tool | Reason | Citation |
| --- | --- | --- | --- |
| `narrowing/negated-instanceof-unrelated-class` | mago | Mago 1.57.0 analyzes a bare return as an expression. Unary Not negates the inferred instanceof result but does not invoke conditional diagnostics or assertion reconciliation. Its silence here is outside this warning's reporting scope; impossible instanceof conditions remain supported and must be tested separately. | https://github.com/carthage-software/mago/blob/1.57.0/crates/analyzer/src/expression/unary.rs#L86-L106 |
| `narrowing/redundant-instanceof-on-declared-class` | mago | Mago 1.57.0 infers literal true for this subtype test but does not emit redundant-condition on a bare returned instanceof. Its own parent-class fixture permits this expression without a diagnostic. Missing a warning here is a reporting-scope divergence, not failed subtype reasoning. | https://github.com/carthage-software/mago/blob/1.57.0/crates/analyzer/tests/cases/inheritance_instanceof_parent_class.php#L5-L17 |
