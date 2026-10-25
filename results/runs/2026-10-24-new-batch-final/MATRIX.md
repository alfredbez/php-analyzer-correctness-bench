# Correctness matrix

| Case | Domain | Rule class | Ground truth | mago | phpstan | psalm | pzoom |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `assignability/catalog-phpstan-da61ed3a1be4f5592a03` | assignability | invalid-property-write | runtime_proof (runtime) | ok | ok | ok | ERR |
| `assignability/catalog-psalm-2ed1be42908ccc536dd5` | assignability | invalid-operand | runtime_proof (runtime) | **FN** <sub>missing required diagnostic(s): invalid-operand</sub> | ok | ok | ERR |

Legend: `ok` matches the case, **FP** false positive, **FN** false negative, `n/a` by-design divergence, `ERR` tool error, `BAD` invalid case, `skip` not applicable.
