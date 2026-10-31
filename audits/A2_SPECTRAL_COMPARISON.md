# Dilute A(2) spectral audit comparison

**Both independent implementations PASS. All reported residuals agree exactly.**
Comparison was performed only after each completed its own calculations.

| Identity/task | Python/FLINT | C/FLINT | Exact residual |
|---|---|---|---|
| I | PASS | PASS | all zero |
| L | PASS | PASS | all zero |
| X2 | PASS | PASS | all zero |
| Y2 | PASS | PASS | all zero |
| Y2_star | PASS | PASS | all zero |
| crossing | PASS | PASS | all zero |

Unitarity: all 16 matrix entries across I,L,X2,Y2,Y2_star vanish exactly over
QQ(p,q,u). Crossing: all 16 diagram coefficients vanish in both rational and
polynomial formulations after prescribed rotation and skein reduction. Both
implementations also verify the nine normalization coefficients at both
arguments, the crossing substitution/involution, N(u)c(u)=N(p^-3*u^-1), and the
polynomial crossing factor 1.

Python uses direct rational matrix multiplication with a new AST/parser and
Python/FLINT fraction implementation. C uses denominator-cleared integer
polynomial matrix multiplication and a separate recursive-descent parser;
its generic infrastructure is adapted from the prior C YBE audit. They share
the public mathematical JSON inputs and FLINT library family, but no computed
intermediate matrices, residuals or arithmetic evaluator. C uses FLINT 2.8.0;
Python uses python-flint 0.9.0 / FLINT 3.6.0. The different algorithms do not make
the common mathematical specification or FLINT library an independent source.

No discrepancies or unresolved algebraic conventions arose. The stated geometric
rotation is an assumption, not a geometric theorem established by these audits.
No existing data, evidence, manuscript or M2 files were changed. Nothing was
committed or published. Both runs used only repository JSON as mathematical
input; accepted-manuscript hashes are provenance, not runtime dependencies.

See [Python report](python/a2_spectral/REPORT.md), [C report](c/a2_spectral/REPORT.md)
and [machine-readable comparison](a2_spectral_comparison.json). All artifacts
are in the research repository. The base commit remains db523ef; the portable
JSON additions from the preceding task were already uncommitted when this task
began, and have been preserved unchanged.
