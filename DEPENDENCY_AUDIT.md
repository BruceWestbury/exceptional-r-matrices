# Dependencies and execution

Choose the components needed for your calculation. The JSON data can be imported
into any system supporting exact rational functions. ExceptionalDiagrams runs
in Macaulay2; the algebraic verification programs run in C or Python.

| Entry point | Repository inputs | Required software |
|---|---|---|
| `macaulay2/ExceptionalDiagrams.m2` | Adjacent `ExceptionalDiagrams/` auxiliary files | Macaulay2 and VectorGraphics; Factor optional |
| `tools/check_macaulay2_data.py` | Bundled package, JSON data and validation helpers | Python >=3.10, jsonschema, Macaulay2 |
| `tools/validate_publication.py` | `data/`, `schema/` and validation helpers | Python >=3.10, jsonschema >=3.2 |
| `audits/c/a3_relations/runner` | Ordinary matrices and relation manifest | C11 compiler, FLINT, GMP, MPFR |
| `audits/run_a2_spectral.py` | A(2) diagrams, spectral specification and selected workers | Python; python-flint for the Python backend; compiled C backend for C |
| `benchmarks/flint_ybe/runner` | Dilute A(3) generators, embeddings and rational comparison matrices | C11 compiler, FLINT, GMP, MPFR |
| `audits/python/run.py` | Same mathematical JSON, plus completed C results for the report | Python >=3.10, python-flint 0.9.0 |
| `examples/import_spectral.py` | Dilute generators and polynomial spectral matrices | SageMath |
| `verify_release.py` | C/Python runners and validation tools | Linux/POSIX, Python and the C/Python dependencies above; SageMath and strace optional |

## Tested versions

The saved C/Python suite used Python 3.10.12, GCC 11.4.0, C FLINT runtime 2.8.0,
python-flint 0.9.0 with FLINT 3.6.0, and jsonschema 3.2.0. The SageMath example
was tested with SageMath 10.6.beta2. Package-check results record the Macaulay2
version in [verification/macaulay2.json](verification/macaulay2.json).

Python requirements for the spectral checks are listed in
[audits/python/requirements.txt](audits/python/requirements.txt) and
[audits/python/a2_spectral/requirements.txt](audits/python/a2_spectral/requirements.txt).
The optional scalar helper `tools/exact_a2.py` uses SymPy.

## Running components separately

Run these commands from the repository root, using fresh output directories:

```sh
make -C audits/c/a3_relations
make -C audits/c/a2_spectral
make -C benchmarks/flint_ybe
mkdir -p checks
audits/c/a3_relations/runner checks/ordinary_a3
python3 audits/run_a2_spectral.py --results checks
benchmarks/flint_ybe/runner benchmarks/flint_ybe/checks
cp benchmarks/flint_ybe/checks/results.json benchmarks/flint_ybe/results.json
python3 audits/python/run.py --output checks/python_ybe
```

The copy command selects the C summary used by the Python comparison report.
Python loads that summary after completing its own mathematical workers.
`verify_release.py` automates this sequence and restores the saved C summary
when the Python stage finishes.

Runners record exact residuals, status, wall time and peak resident memory. Use
the supplied runners for their 60-second worker and 300-second batch limits.
Standalone diagnostic commands in the component guides use `timeout`.
