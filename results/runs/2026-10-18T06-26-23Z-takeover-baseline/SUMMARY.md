# Correctness summary

- Run: `2026-10-18T06-26-23Z-takeover-baseline`
- Started: 2026-10-18T06:26:23Z (UTC)
- phpstan: PHPStan - PHP Static Analysis Tool 2.3.1
- psalm: Psalm 6.20.0@804f03c0c183d149fcd4b8c7c0c9b3fbf836d34c
- mago: mago 1.57.0
- PHP: 8.3.35
- Cases: 14 (valid: 14)
- Runtime checks passed: 14/14

`agreement` = ok / judged, where judged = ok + false positives + false negatives + mixed. By-design divergences, tool errors, case errors and skips are excluded and listed separately.

| Tool | Cases | Judged | ok | FP | FN | mixed | by-design | tool error | case error | skipped | agreement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mago | 14 | 14 | 8 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 57.1% |
| phpstan | 14 | 14 | 13 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 92.9% |
| psalm | 14 | 14 | 13 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 92.9% |

## Per domain

| Domain | Tool | Cases | ok | FP | FN | by-design |
| --- | --- | --- | --- | --- | --- | --- |
| callables | mago | 2 | 0 | 2 | 0 | 0 |
| dead-code | mago | 1 | 1 | 0 | 0 | 0 |
| narrowing | mago | 7 | 5 | 0 | 2 | 0 |
| nullability | mago | 4 | 2 | 2 | 0 | 0 |
| callables | phpstan | 2 | 2 | 0 | 0 | 0 |
| dead-code | phpstan | 1 | 0 | 1 | 0 | 0 |
| narrowing | phpstan | 7 | 7 | 0 | 0 | 0 |
| nullability | phpstan | 4 | 4 | 0 | 0 | 0 |
| callables | psalm | 2 | 2 | 0 | 0 | 0 |
| dead-code | psalm | 1 | 1 | 0 | 0 | 0 |
| narrowing | psalm | 7 | 6 | 0 | 1 | 0 |
| nullability | psalm | 4 | 4 | 0 | 0 | 0 |
