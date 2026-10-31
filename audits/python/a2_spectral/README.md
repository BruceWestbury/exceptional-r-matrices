# Python/FLINT dilute A(2) spectral audit

Requires Python >=3.10 and `python-flint==0.9.0` (tested with FLINT 3.6.0).
No SymPy, Sage, C verifier, previous Python audit, manuscript file or Macaulay2
is imported or executed. Mathematical inputs are the public JSON dataset plus
`audits/a2_spectral_spec.json`, the source-derived identity specification.

From the repository root:

```sh
python3 -m pip install -r audits/python/a2_spectral/requirements.txt
python3 audits/run_a2_spectral.py --backend python --results new_run
```

Choose a new results directory name: the launcher refuses to overwrite evidence.
It kills each process group at 60 seconds and enforces 300 seconds for the batch.
For both backends within **one** 300-second budget, build C first, then use:

```sh
python3 audits/run_a2_spectral.py --backend all --results new_run
```

Direct diagnostic invocation (still use a hard limit):

```sh
timeout -s KILL 60s python3 audits/python/a2_spectral/verify.py crossing
timeout -s KILL 60s python3 audits/python/a2_spectral/verify.py I
```

Task names: I, L, X2, Y2, Y2_star, crossing. The default launcher order is
X2,Y2,Y2_star,I,L,crossing, increasing representation dimension.
The launcher does process supervision and JSON recording only, with no CAS
operations. Source `verify.py` has its own rational arithmetic, AST parser,
matrix evaluator and diagram coefficient reduction.

`results/` is the original successful evidence. `REPORT.md` states the exact
mathematics and conditional scope. Each unitarity result includes full rational
and polynomial residual matrices in zero-based row/column array order; every
scalar is an exact numerator/denominator string. Crossing includes every D0–D15
coefficient. The polynomial unitarity residual is obtained from the direct
rational residual by the separately verified normalization equivalence, rather
than a duplicate polynomial matrix multiplication.

`audits/summarize_a2_spectral.py` compares the saved completed `results/` files
and renders the reports; it does not perform mathematical calculations. It is
not part of either verifier and must be run only after both backends finish.
No output of the C implementation enters the Python computation.
