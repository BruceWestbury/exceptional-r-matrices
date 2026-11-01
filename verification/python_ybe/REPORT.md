# Independent Python/FLINT spectral YBE audit

Exact arithmetic over QQ(p,q,u,v), with algebraically independent variables.

| Representation | Dim. | Python | C | Construct s | YBE s | Compare s | Wall s | Peak MiB |
|---|---:|---|---|---:|---:|---:|---:|---:|
| X3 | 1 | PASS | PASS | 0.0251 | 0.0059 | 0.0027 | 0.0706 | 23.93 |
| Y3 | 1 | PASS | PASS | 0.0277 | 0.0035 | 0.0024 | 0.0636 | 23.27 |
| Y3_star | 1 | PASS | PASS | 0.0197 | 0.0030 | 0.0025 | 0.0539 | 23.30 |
| C | 2 | PASS | PASS | 0.0254 | 0.0204 | 0.0042 | 0.1222 | 24.06 |
| C_star | 2 | PASS | PASS | 0.0263 | 0.0182 | 0.0042 | 0.1255 | 24.27 |
| A | 3 | PASS | PASS | 0.0331 | 0.0437 | 0.0099 | 0.2258 | 26.09 |
| I | 5 | PASS | PASS | 0.0430 | 0.1833 | 0.0945 | 0.8659 | 33.33 |
| Y2 | 6 | PASS | PASS | 0.0577 | 0.2360 | 0.1034 | 0.9915 | 34.86 |
| Y2_star | 6 | PASS | PASS | 0.0591 | 0.2705 | 0.1097 | 1.0320 | 34.65 |
| X2 | 7 | PASS | PASS | 0.0790 | 0.3649 | 0.1014 | 1.3269 | 38.13 |
| L | 11 | PASS | PASS | 0.1456 | 1.5502 | 0.3004 | 4.4622 | 69.14 |

All eleven generic symbolic YBE checks and all polynomial/rational comparisons PASS with exact zero residuals.

Sum of worker wall times: 9.3402 seconds.
Limits: 60 seconds per worker and 300 seconds per batch.

Construction uses literal rational equation (8.3), followed by the paper’s polynomial normalization. Clearing time is separate in results.json. YBE time includes FLINT composition, both triple products, and every entrywise difference. Comparison occurs after YBE. Wall time includes interpreter/library import and reporting overhead; peak RSS is wait4 ru_maxrss on Linux.

The Python workers construct and evaluate their own matrices. The report loads C results after the Python batch finishes. The implementations share the JSON mathematical specifications and the FLINT library family.

The conclusion concerns the supplied representations with the specified embeddings and normalization. The paper provides the categorical interpretation and abstract presentation arguments.
