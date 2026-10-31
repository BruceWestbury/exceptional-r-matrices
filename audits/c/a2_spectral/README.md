# C/FLINT dilute A(2) spectral audit

Requires a C11 compiler, FLINT development headers/library, GMP and MPFR.
Tested with cc 11.4.0 and FLINT runtime 2.8.0 (Ubuntu package 2.8.4).
Build from the repository root:

```sh
make -C audits/c/a2_spectral
```

Compilation uses `-O2 -std=c11 -Wall -Wextra` and links
`-lflint -lgmp -lmpfr`. `build_final.txt` records the clean final build;
`build.txt` preserves the initial indentation warnings. No calculation ran with
those warnings; the final calculation source hashes are in `results/results.json`.

Run a standalone exact check, with the repository root as cwd:

```sh
timeout -s KILL 60s audits/c/a2_spectral/verify I
timeout -s KILL 60s audits/c/a2_spectral/verify crossing
```

The standalone binary does not invoke Python, Sage or Macaulay2. Task names are
I,L,X2,Y2,Y2_star,crossing. The only mathematical inputs are public repository
JSON and `audits/a2_spectral_spec.json`. Manuscript/source paths in provenance
are citations, not runtime dependencies.

For resource measurements and a complete machine-readable batch, the optional
standard-library Python launcher executes the binary, without doing mathematics:

```sh
python3 audits/run_a2_spectral.py --backend c --results new_run
# Or run both implementations under one combined 300-second budget:
python3 audits/run_a2_spectral.py --backend all --results new_run
```

Choose a new output directory name. Existing evidence is never overwritten by
the runner. It imposes a hard 60-second process-group limit per task and a
300-second total batch deadline, then records PASS/FAIL/ERROR/TIMEOUT, stderr,
wall time and Linux peak RSS. Standalone failures to parse/build return nonzero;
the launcher turns those into ERROR records. Nonzero mathematical residuals are
printed exactly and return FAIL. No numerical fallback or limit extension exists.

`verify.c` is the new A(2) calculation. `exact.h` adapts **generic** C arithmetic,
JSON parsing and scalar parsing from the existing C YBE verifier; no spectral
matrix construction was copied. Integer-polynomial numerator/denominator pairs
are reduced exactly using FLINT gcd. Dense matrix products use polynomial
arithmetic after denominator clearing. The shared factors are printed; the
reported residual divides them out and also divides out N(u)N(u^-1) for rational
unitarity. D4 is the declared H-squared diagram; no representation basis map is
fitted. Coefficientwise crossing uses formal rotation and skein elimination,
not matrix transposition or tests only in irreducible representations.

See `REPORT.md`, `results/`, `../../A2_SPECTRAL_COMPARISON.md`, and the shared
provenance JSON. Python/C results are compared only by the separate summarizer
after both independent batches have completed.
