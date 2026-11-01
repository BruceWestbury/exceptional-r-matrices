# Python/FLINT unitarity and crossing

This verifier checks generic unitarity in the five dilute A(2) representations
and crossing in all sixteen diagram coordinates. It requires Python >=3.10 and
python-flint 0.9.0; the saved run used FLINT 3.6.0.

From the repository root:

```sh
python3 -m pip install -r audits/python/a2_spectral/requirements.txt
python3 audits/run_a2_spectral.py --backend python --results checks
```

The launcher creates a fresh `checks/` directory alongside this guide and records
exact residuals, status, diagnostics, wall time and peak memory. Choose a fresh
name for each run. Limits are 60 seconds per task and 300 seconds per batch.

For both implementations within one combined batch, build the C verifier first:

```sh
make -C audits/c/a2_spectral
python3 audits/run_a2_spectral.py --backend all --results combined_checks
```

Standalone diagnostics run from the repository root:

```sh
timeout -s KILL 60s python3 audits/python/a2_spectral/verify.py crossing
timeout -s KILL 60s python3 audits/python/a2_spectral/verify.py I
```

Task names are I, L, X2, Y2, Y2_star and crossing. The launcher processes the
one-dimensional representations first, followed by I, L and crossing.

`verify.py` implements a restricted scalar parser, rational arithmetic, ordered
matrix products and diagram coefficient reduction. Its mathematical inputs are
repository JSON and [the shared identity specification](../../a2_spectral_spec.json).
Unitarity uses direct rational matrix multiplication; the polynomial residual
follows from the separately checked normalization equivalence.

The [report](REPORT.md) describes the mathematics and saved results.
The [comparison report](../../A2_SPECTRAL_COMPARISON.md) summarizes agreement with
the separately evaluated C implementation.
