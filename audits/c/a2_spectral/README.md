# C/FLINT unitarity and crossing

This verifier checks generic unitarity in the five dilute A(2) representations
and crossing in all sixteen diagram coordinates, using exact rational functions.
It requires a C11 compiler, FLINT development headers, GMP and MPFR.
The saved run used GCC 11.4.0 and FLINT runtime 2.8.0.

From the repository root:

```sh
make -C audits/c/a2_spectral
python3 audits/run_a2_spectral.py --backend c --results checks
```

The launcher saves a fresh `checks/` directory alongside this guide, with exact
residuals, status, wall time, peak memory and diagnostics. Choose a fresh name
for each run. Limits are 60 seconds per task and 300 seconds per batch.
To run both implementations within one combined batch:

```sh
python3 audits/run_a2_spectral.py --backend all --results combined_checks
```

The Python backend requires the dependencies in its
[guide](../../python/a2_spectral/README.md).
Standalone diagnostic commands also run from the repository root:

```sh
timeout -s KILL 60s audits/c/a2_spectral/verify I
timeout -s KILL 60s audits/c/a2_spectral/verify crossing
```

Task names are I, L, X2, Y2, Y2_star and crossing.
`verify.c` constructs the spectral matrices from repository JSON and
[the shared identity specification](../../a2_spectral_spec.json).
`exact.h` supplies rational arithmetic and parsing; FLINT performs polynomial
arithmetic, denominator clearing and gcd reduction.

The [report](REPORT.md) describes the calculation and links the saved residuals.
The [comparison report](../../A2_SPECTRAL_COMPARISON.md) relates the C and Python
implementations. The launcher records PASS, FAIL, ERROR and TIMEOUT separately.
