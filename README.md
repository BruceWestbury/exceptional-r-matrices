# Exceptional-series R-matrices

Exact JSON matrices, the ExceptionalDiagrams Macaulay2 package, and computational
audits accompanying Bruce W. Westbury and
Paul Zinn-Justin, *A uniform trigonometric R-matrix for the exceptional series*
(arXiv:2406.01348, accepted manuscript). The data, documentation and code are
licensed under [Creative Commons Attribution 4.0 International
(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); see [LICENSE](LICENSE).

Start with `data/publication.json` and FORMAT.md. The 542 sparse matrices comprise
110 ordinary A(3), 330 dilute A(3), 80 dilute A(2), and 22 polynomial spectral
matrices. Coefficients are exact; indices are zero-based; row vectors act on the
right. Raw dilute normalization differs from the manuscript-normalized spectral
files. Scalar aliases, embeddings, basis maps and normalizations are portable JSON.
The JSON data and C/Python audits do not require Macaulay2 or the manuscript.

## Macaulay2 package

The maintained package is in [macaulay2/](macaulay2/README.md), including all
auxiliary files and the original tests. From the repository root, in Macaulay2:

```m2
needsPackage("ExceptionalDiagrams",
    FileName=>"macaulay2/ExceptionalDiagrams.m2");
s1 = rep(3,(braid())_1,Dilute=>false);
s2 = rep(3,(braid())_2,Dilute=>false);
assert(s1*s2*s1 == s2*s1*s2);
```

The package needs `VectorGraphics`; `Factor` is optional. See its README for
installation, spectral matrices, normalization choices, and tests. The package
runs independently of the JSON data and the Python/C software.

To verify exact agreement with the data, and test the package and installation:

```sh
python3 tools/check_macaulay2_data.py --package-tests --output /tmp/m2-check.json
```

This separate check requires Macaulay2 and Python with jsonschema. It performs
952 matrix comparisons covering all 542 stored matrices, testing both package
normalizations for raw dilute data. It neither updates nor regenerates data.
The GitHub Actions Macaulay2 job runs this check independently of the C/Python
mathematical audits below.

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
DATASET_PROVENANCE.md explains the initial curation and subsequent changes.
PUBLICATION_DECISIONS.md records the licence choice and remaining release
decisions, including citation metadata.

The recorded verification was stronger than a normal rerun: bubblewrap mounted
only this candidate at `/tmp/release`, hid the research Dropbox tree, disabled
networking, and supplied `/dev`; PWD/OLDPWD pointed inside the candidate. Python
and FLINT/Sage installations remained available read-only. A normal invocation
of verify_release.py does not claim this namespace isolation; its report states
whether PUBLIC_ISOLATED was provided by the external namespace supervisor.

## Licence and attribution

CC BY 4.0 applies to the repository's mathematical data, documentation and
software, including ExceptionalDiagrams and the C/Python audit code. When sharing
or adapting this material, give appropriate credit, link to the licence and
indicate any changes, as specified in [LICENSE](LICENSE). Credit Bruce W. Westbury
and Paul Zinn-Justin for the companion repository, and retain Paul Zinn-Justin's
authorship credit for ExceptionalDiagrams. See [CITATION.cff](CITATION.cff) for the
accompanying paper's citation. External dependencies retain their own licences.
