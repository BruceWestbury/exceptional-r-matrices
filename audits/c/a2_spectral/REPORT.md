# C/FLINT dilute A(2) spectral verification

**PASS:** generic unitarity in all five representations and coefficientwise
crossing in all sixteen diagram coordinates. All sixteen matrix entries across
the unitarity blocks, and all sixteen coefficients in each crossing formulation,
have exact zero residuals.

The table summarizes the included [run results](verification_results/results.json).

| Task | Status | Calculation s | Wall s | Peak MiB |
|---|---|---:|---:|---:|
| X2 | PASS | 0.0470 | 0.0590 | 9.89 |
| Y2 | PASS | 0.0471 | 0.0588 | 9.89 |
| Y2_star | PASS | 0.0467 | 0.0601 | 10.16 |
| I | PASS | 0.0528 | 0.0641 | 9.89 |
| L | PASS | 0.0504 | 0.0598 | 9.89 |
| crossing | PASS | 0.0622 | 0.0761 | 9.89 |

## Calculation

C constructs polynomial spectral matrices and clears their common denominators
at u and u^-1. If A=D_a Rpoly(u) and B=D_b Rpoly(u^-1), it evaluates
`AB-D_a D_b N(u)N(u^-1)Id` using FLINT integer multivariate polynomials.
Recorded rational residuals divide out the clearing factors and N(u)N(u^-1).
Each worker records the exact factors used.

The scalar parser and reduced numerator/denominator arithmetic are implemented
in `exact.h`. The saved calculation used GCC 11.4.0 and FLINT runtime 2.8.0.

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
