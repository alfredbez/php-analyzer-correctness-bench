# Gaps for mago

From run `2026-10-24-new-batch-final` (mago 1.58.2, PHP 8.4.27).

Each entry is a case file a maintainer (or their agent) can run directly; the raw tool output of the run is in the run directory next to this report.

## `assignability/catalog-psalm-2ed1be42908ccc536dd5` - false_negative

- rule class: `invalid-operand`, domain: `assignability`
- ground truth basis: `runtime_proof`
- what the tool did: missing required diagnostic(s): invalid-operand
- missing: `invalid-operand`
- run it: `python3 harness/bench.py run --case assignability/catalog-psalm-2ed1be42908ccc536dd5 --tool mago` (case directory: `cases/assignability/catalog-psalm-2ed1be42908ccc536dd5`)
