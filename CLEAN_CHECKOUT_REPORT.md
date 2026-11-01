# Recorded verification results

**PASS:** the saved C/Python suite covers structural validation, ordinary A(3)
relations, dilute A(2) unitarity and crossing, generic Yang–Baxter identities,
and the SageMath import example. The table summarizes
[verification/summary.json](verification/summary.json).

| Stage | Status | Wall seconds | Limit seconds |
|---|---|---:|---:|
| structural | PASS | 1.622 | 60 |
| build_ordinary | PASS | 0.824 | 60 |
| build_a2 | PASS | 0.622 | 60 |
| build_ybe | PASS | 0.821 | 60 |
| ordinary_a3 | PASS | 2.321 | 300 |
| a2_spectral | PASS | 1.574 | 300 |
| c_ybe | PASS | 2.220 | 300 |
| python_ybe | PASS | 9.536 | 300 |
| sage | PASS | 4.052 | 59 |

## Mathematical results

- Structural validation: 47 JSON files, six schemas and 542 matrices pass;
  ten malformed-data fixtures are rejected.
- Ordinary A(3): 1,605 applicable encoded relations pass in eleven representations.
- Dilute A(2): C and Python both pass unitarity in five representations and
  crossing in all sixteen diagram coefficients.
- Dilute A(3): C and Python both pass the generic Yang–Baxter equation in eleven
  representations, with exact zero residuals.
- SageMath: scaled unitarity passes at u=2 and u=1/2 over QQ(p,q), in both
  spectral positions for dilute I.

The separately recorded [Macaulay2 check](verification/macaulay2.json) passes
952 exact matrix comparisons and its package and installation tests. That run
contains 46 stages and took about 439 seconds.

[AUDIT_COVERAGE.md](AUDIT_COVERAGE.md) describes the scope of each check and the
additional construction work needed for full ordinary-to-dilute reconstruction.

## Environment and measurements

The C/Python run used Python 3.10.12, GCC 11.4.0, C FLINT runtime 2.8.0,
python-flint 0.9.0 with FLINT 3.6.0, jsonschema 3.2.0 and SageMath 10.6.beta2.
Compilation time is recorded separately. Worker logs retain exact residuals,
wall times and peak resident memory.

The saved suite ran in an isolated filesystem environment with local software
dependencies available. Its summary records the environment settings and
file-access measurements. Each mathematical worker has a 60-second ceiling and
each batch a 300-second ceiling; the table records the effective stage limits.

## Reproduction

Follow the dependencies in [README.md](README.md), then run:

```sh
python3 verify_release.py --run-name checks
python3 tools/check_macaulay2_data.py --package-tests --output /tmp/m2-check.json
```

Choose a fresh run name and output filename. The suite saves logs and JSON
results under the run name and updates this Markdown summary. The Macaulay2
command writes its separate report to the chosen output file.
