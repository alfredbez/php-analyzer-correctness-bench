# Correctness summary

- Run: `2026-10-24-new-batch-final`
- Started: 2026-10-24T17:31:05Z (UTC)
- phpstan: PHPStan - PHP Static Analysis Tool 2.3.1
- psalm: Psalm 6.20.1@376425b8e67b79773add388e16b4f6be5693dc87
- mago: mago 1.58.2
- pzoom: pzoom c8162978033745e585f8e60d15a66a48862333cc
- PHP: 8.4.27
- Cases: 2 (valid: 2)
- Runtime checks passed: 2/2

`agreement` = ok / judged, where judged = ok + false positives + false negatives + mixed. By-design divergences, tool errors, case errors and skips are excluded and listed separately.

| Tool | Cases | Judged | ok | FP | FN | mixed | by-design | tool error | case error | skipped | agreement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mago | 2 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 50.0% |
| phpstan | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0% |
| psalm | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0% |
| pzoom | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | n/a |

## Per domain

| Domain | Tool | Cases | ok | FP | FN | by-design |
| --- | --- | --- | --- | --- | --- | --- |
| assignability | mago | 2 | 1 | 0 | 1 | 0 |
| assignability | phpstan | 2 | 2 | 0 | 0 | 0 |
| assignability | psalm | 2 | 2 | 0 | 0 | 0 |
| assignability | pzoom | 2 | 0 | 0 | 0 | 0 |
