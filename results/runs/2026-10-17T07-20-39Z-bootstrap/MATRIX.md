# Correctness matrix

| Case | Domain | Rule class | Ground truth | mago | phpstan | psalm |
| --- | --- | --- | --- | --- | --- | --- |
| `narrowing/is-int-on-string` | narrowing | impossible-condition | runtime_proof | ok | ok | ERR |

Legend: `ok` matches the case, **FP** false positive, **FN** false negative, `n/a` by-design divergence, `ERR` tool error, `BAD` invalid case, `skip` not applicable.
