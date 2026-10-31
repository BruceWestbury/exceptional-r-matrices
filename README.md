# Exceptional-series R-matrices — local release candidate

Exact JSON matrices and computational audits accompanying Bruce W. Westbury and
Paul Zinn-Justin, *A uniform trigonometric R-matrix for the exceptional series*
(arXiv:2406.01348, accepted manuscript). This directory is an **unlicensed draft**,
not an approved release. No Git repository, remote or Zenodo deposit is created.

Start with `data/publication.json` and FORMAT.md. The 542 sparse matrices comprise
110 ordinary A(3), 330 dilute A(3), 80 dilute A(2), and 22 polynomial spectral
matrices. Coefficients are exact; indices are zero-based; row vectors act on the
right. Raw dilute normalization differs from the manuscript-normalized spectral
files. Scalar aliases, embeddings, basis maps and normalizations are portable JSON.
No Macaulay2 or manuscript file is needed at runtime.

## Reproduce the checks

Linux/POSIX, Python >=3.10, jsonschema >=3.2, python-flint 0.9.0, a C11 compiler,
FLINT development headers, GMP and MPFR are required. Sage is optional. The
original tests used C FLINT 2.8.0 and Python FLINT 3.6.0. Optional legacy helper
functions in exact_a2.py require SymPy; core structural validation does not.

```sh
python3 tools/validate_publication.py --self-test
make -C audits/c/a3_relations
make -C audits/c/a2_spectral
make -C benchmarks/flint_ybe
mkdir -p rerun
audits/c/a3_relations/runner rerun/ordinary_a3
python3 audits/run_a2_spectral.py --results fresh_results
benchmarks/flint_ybe/runner benchmarks/flint_ybe/fresh_results
# The Python report consumes the completed C summary, not C mathematical matrices:
cp benchmarks/flint_ybe/fresh_results/results.json benchmarks/flint_ybe/results.json
python3 audits/python/run.py --output rerun/python_ybe
# Optional:
timeout -s KILL 60s sage -python examples/import_spectral.py
```

Choose fresh output
directories; runners refuse to overwrite evidence. Each mathematical worker is
limited to 60 seconds and each batch to 300 seconds. Do not run standalone workers
without a deadline. `python3 verify_release.py --run-name rerun_all` automates these steps with fresh evidence
and checks result statuses, rather than relying solely on runner exit codes.

See CLEAN_CHECKOUT_REPORT.md for this candidate's actual test results,
AUDIT_COVERAGE.md for scope/limitations, DEPENDENCY_AUDIT.md for dependency chains,
and PUBLICATION_INVENTORY.md for the complete proposed inventory.
PUBLICATION_MANIFEST.json is the explicit copy whitelist, with source/candidate
hashes; EXCLUDED_FILES.json lists every excluded tracked research file and reason.
DATASET_PROVENANCE.md explains metadata-only curation. PUBLICATION_DECISIONS.md
lists approvals still needed, including licences and citation/release metadata.

The recorded verification was stronger than a normal rerun: bubblewrap mounted
only this candidate at `/tmp/release`, hid the research Dropbox tree, disabled
networking, and supplied `/dev`; PWD/OLDPWD pointed inside the candidate. Python
and FLINT/Sage installations remained available read-only. A normal invocation
of verify_release.py does not claim this namespace isolation; its report states
whether PUBLIC_ISOLATED was provided by the external namespace supervisor.
