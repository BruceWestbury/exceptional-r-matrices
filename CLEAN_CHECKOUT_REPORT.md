# Clean-checkout verification report

**PASS**: all requested candidate checks completed. This historical report records the initial clean curated directory, before the Git repository and Macaulay2 integration were added.

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

Structural validation: 47 data JSON files, 542 matrices, six schemas and ten negative fixtures. Ordinary A(3): **1,605 exact PASS, 45 NOT APPLICABLE**; the unprinted degree-seven relation is not claimed. Dilute A(2): both implementations pass unitarity in five representations and crossing coefficientwise. Generic dilute A(3) YBE: both implementations pass all eleven representations, with exact zero residuals. Sage: exact scaled unitarity at u=2,1/2 in both positions of dilute I over QQ(p,q).

Dependencies: {'python': '3.10.12', 'compiler': 'cc (Ubuntu 11.4.0-1ubuntu1~22.04.3) 11.4.0', 'python-flint': '0.9.0', 'jsonschema': '3.2.0', 'sympy': '1.9'}. C FLINT runtime 2.8.0; python-flint 0.9.0 / FLINT 3.6.0; Sage 10.6.beta2. Worker JSON records exact timings and peak memory. Build time is separate.

## Isolation and startup incident

The candidate was mounted at `/tmp/release` in a bubblewrap namespace; the entire research Dropbox tree was hidden and networking disabled. The original repository and manuscript were inaccessible. All successful checks were traced with strace and recorded **zero forbidden research-path attempts**. External software dependencies remained available read-only. Raw access traces were ephemeral; per-stage counts are retained in verification/summary.json.

The first namespace mount failed before calculation because the read-only root could not create /release. The later initial Sage startup failed because /dev/null was read-only; an inherited PWD produced one inaccessible research-path probe. No Sage mathematics ran. Supplying /dev and clean PWD/OLDPWD fixed startup. Only the unchanged Sage example was retried, under a reduced 59-second ceiling, and passed in 4.052 seconds. Successful mathematical batches were not repeated. The incident, initial evidence hashes and corrective details are in verification/isolation_incident.json.

Each mathematical worker retained a 60-second hard limit and each batch a 300-second ceiling. No limit was extended, no numerical fallback was used, and no mathematical failure was hidden. The final summary combines the successful main batch and this Sage-only retry.

## Integrity and reproducibility

All original research JSON hashes still match; the research working tree remains clean at 83aed000254bf7aca4836f0d3e3fb47c818ee4fa. All selected mathematical sources are byte-for-byte copies. Only explicitly documented candidate metadata and documentation changed. No compiled executable, M2 file, cache, symlink or .git directory remains in the candidate.

The historical Python ordinary-audit wrapper is deliberately excluded because it reads exploratory/Git-history inputs; the portable C manifest audit supplies current ordinary-relation coverage. Original construction-source comparisons are cited historical evidence, not rerun assertions.

Run `python3 verify_release.py --run-name a_fresh_name` for another bounded suite after installing the documented dependencies. It reports whether namespace isolation was supplied; ordinary reruns do not pretend the research tree was masked. Generated executable removal is part of the runner. New evidence must use fresh names.

The verification run itself created no GitHub remote, commit, release or Zenodo
deposit. The repository has since adopted [CC BY 4.0](LICENSE); citation and
release metadata remain to be finalized.
