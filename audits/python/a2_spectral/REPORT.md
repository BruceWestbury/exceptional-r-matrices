# Python/FLINT dilute A(2) spectral verification

**PASS:** generic unitarity in all five representations and coefficientwise
crossing in all sixteen diagram coordinates. All sixteen matrix entries across
the unitarity blocks, and all sixteen coefficients in each crossing formulation,
have exact zero residuals.

The table summarizes the included [run results](verification_results/results.json).

| Task | Status | Calculation s | Wall s | Peak MiB |
|---|---|---:|---:|---:|
| X2 | PASS | 0.0508 | 0.1642 | 26.34 |
| Y2 | PASS | 0.0526 | 0.1628 | 26.32 |
| Y2_star | PASS | 0.0516 | 0.1573 | 26.78 |
| I | PASS | 0.0820 | 0.1833 | 27.07 |
| L | PASS | 0.1271 | 0.2305 | 27.20 |
| crossing | PASS | 0.0753 | 0.1782 | 26.92 |

## Calculation

Python constructs normalized diagram matrices and multiplies the rational
R-matrices directly. The polynomial residual follows from the verified scalar
normalization. Arithmetic uses reduced fractions of FLINT rational multivariate
polynomials in lexicographic order and a restricted AST scalar parser.
The saved calculation used Python 3.10.12 and python-flint 0.9.0 with FLINT 3.6.0.

All identities are evaluated over QQ(p,q,u), with independent variables.
Raw A(2) diagram matrices are multiplied by their `paper2_multiplier`.
Let N(u) be the prefactor in [data/spectral_r.json](../../../data/spectral_r.json)
and let w=p^-3*u^-1. The scalar checks establish

```text
Rpoly(u) = N(u) Rcheck(u)
N(u)c(u) = N(w)
Rot(Rpoly(u)) = Rpoly(w).
```

Here c(u) is the rational crossing prefactor. The rational and polynomial
unitarity residuals differ by N(u)N(u^-1). These identities hold in the generic
fraction field and specialize wherever the relevant expressions are defined.

## Coefficientwise crossing

The [identity specification](../../a2_spectral_spec.json) encodes the rational
spectral coefficients and the skein relation

```text
S-Sinv = t*(H-K+(q-q^-1)^2*(U-I))
t = (q-q^-1)[n+1][2n][3n]/[6n].
```

Nine coefficient comparisons at both spectral arguments verify the polynomial
normalization. Crossing rotates the split ordinary diagrams, eliminates S using
the skein relation, and expands into D0,...,D15. D4 denotes the square of H.
Both rational and polynomial crossing residuals record every diagram coefficient.
The diagram basis and rotation are the mathematical conventions supplied by the
paper and encoded in the specification.

## Reproducing the check

Follow [README.md](README.md). Each task has a 60-second process-group limit,
and the combined C/Python batch has a 300-second limit. JSON results contain
exact numerator/denominator residuals, zero-based coordinates, timings and peak
resident memory. The [comparison report](../../A2_SPECTRAL_COMPARISON.md)
summarizes agreement between the implementations.
