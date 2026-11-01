# Dilute A(2) spectral verification

**Both implementations pass unitarity and crossing with exact zero residuals.**
C/FLINT and Python/FLINT evaluate the shared mathematical specification using
separate parsers and arithmetic implementations.

| Check | Python/FLINT | C/FLINT | Scope |
|---|---|---|---|
| Unitarity, I | PASS | PASS | 2×2 matrix |
| Unitarity, L | PASS | PASS | 3×3 matrix |
| Unitarity, X2 | PASS | PASS | 1×1 matrix |
| Unitarity, Y2 | PASS | PASS | 1×1 matrix |
| Unitarity, Y2_star | PASS | PASS | 1×1 matrix |
| Crossing | PASS | PASS | Sixteen diagram coefficients |

The calculations use QQ(p,q,u). Unitarity tests all sixteen entries across the
five blocks. Crossing tests all sixteen coefficients after diagram rotation and
skein reduction, in both rational and polynomial normalizations.

Both implementations also check the nine spectral normalization coefficients at
both arguments, the crossing substitution and its involution, and the identity
`N(u)c(u)=N(p^-3*u^-1)`. The resulting polynomial crossing factor is 1.

## Methods and scope

Python uses direct rational matrix multiplication and FLINT rational polynomials.
C uses denominator-cleared integer-polynomial products. Each implementation
constructs its own intermediate matrices and residuals; they share the JSON
specification and the FLINT library family. The saved C run used FLINT 2.8.0;
the Python run used python-flint 0.9.0 with FLINT 3.6.0.

These are exact algebraic checks with the specified diagram basis and rotation.
The paper supplies their categorical interpretation. Specializations require
the relevant rational expressions to be defined.

## Results and reproduction

The [Python report](python/a2_spectral/REPORT.md) and
[C report](c/a2_spectral/REPORT.md) link their saved worker results.
The [machine-readable comparison](a2_spectral_comparison.json) records agreement
of the reported residuals.

To run both implementations from the repository root:

```sh
make -C audits/c/a2_spectral
python3 audits/run_a2_spectral.py --backend all --results checks
```

Use a fresh result name and the dependencies described in the component guides.
The launcher applies a 60-second limit per task and a 300-second combined budget.
