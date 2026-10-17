# Correctness summary

- Run: `2026-10-17T07-22-27Z-bootstrap`
- Started: 2026-10-17T07:22:27Z (UTC)
- phpstan: PHPStan - PHP Static Analysis Tool 2.3.1
- psalm: Psalm 6.20.0@804f03c0c183d149fcd4b8c7c0c9b3fbf836d34c
- mago: mago 1.57.0
- PHP: 8.3.35
- Cases: 1 (valid: 1)

`agreement` = ok / (ok + false positives + false negatives). Cases whose ground truth is a by-design divergence, a tool error or a skip are excluded and listed separately.

| Tool | Cases | ok | false positive | false negative | mixed | by-design | tool error | agreement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mago | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 100.0% |
| phpstan | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 100.0% |
| psalm | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 100.0% |

## Per domain

| Domain | Tool | Cases | ok | FP | FN | by-design |
| --- | --- | --- | --- | --- | --- | --- |
| narrowing | mago | 1 | 1 | 0 | 0 | 0 |
| narrowing | phpstan | 1 | 1 | 0 | 0 | 0 |
| narrowing | psalm | 1 | 1 | 0 | 0 | 0 |
