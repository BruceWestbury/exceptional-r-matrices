# C/FLINT dilute A(2) spectral audit

**PASS:** generic unitarity in all five representations and coefficientwise
crossing in all sixteen diagram coordinates. No nonzero residual, ERROR or
TIMEOUT occurred. The rational unitarity residual has 16 entries across the
five blocks, all zero; each crossing formulation has 16 zero coefficients.

| Task | Status | Calculation s | Wall s | Peak MiB |
|---|---|---:|---:|---:|
| X2 | PASS | 0.0537 | 0.0671 | 10.02 |
| Y2 | PASS | 0.0493 | 0.0570 | 10.02 |
| Y2_star | PASS | 0.0565 | 0.0636 | 10.03 |
| I | PASS | 0.0544 | 0.0623 | 10.03 |
| L | PASS | 0.0551 | 0.0622 | 10.04 |
| crossing | PASS | 0.0665 | 0.0732 | 10.04 |

Total worker wall time: 0.3854 s. Interpreter/compiler: `cc (Ubuntu 11.4.0-1ubuntu1~22.04.3) 11.4.0`.

C constructs diagram coefficient vectors, assembles polynomial spectral
matrices and clears their exact common denominators separately at u and u^-1.
The triple-loop matrix product uses FLINT integer multivariate polynomials.
If A=D_a Rpoly(u), B=D_b Rpoly(u^-1), it tests
AB-D_a D_b N(u)N(u^-1)Id=0 after exact scalar denominator clearing.
The recorded residuals divide out these nonzero factors; the rational residual
also divides by N(u)N(u^-1). Every clearing factor is saved in the worker result.

`exact.h` adapts the prior C YBE verifier's generic rational arithmetic, JSON and
scalar-parser infrastructure; no prior spectral construction is copied. The A(2)
construction and coefficient-reduction code in `verify.c` is new. No Python,
Sage, Macaulay2 or previously computed matrices/residuals enter the C calculation.
FLINT runtime 2.8.0; cc 11.4.0; `-O2 -std=c11 -Wall -Wextra`, linked with
`-lflint -lgmp -lmpfr`. The final build has no warnings. Initial indentation
warnings and the clean final build log are both retained.

The rational identity is checked over QQ(p,q,u), with algebraically independent
variables. No numerical or finite-field evaluation is used. Raw A(2) generator
matrices are multiplied by their `paper2_multiplier`; no basis fitting or
conjugation is needed for these identities.

Let N(u) be the paper's scalar in `data/spectral_r.json` and let
w=p^-3*u^-1. The independently evaluated scalar checks establish
N(u)c(u)=N(w), where c is the printed (8.13) prefactor. Thus
Rot(Rpoly(u))=Rpoly(w), with polynomial transformation factor **1**.
The rational and polynomial unitarity residuals differ by exactly
N(u)N(u^-1). These nonzero rational scalars are invertible in the generic
field; this is not a claim at every singular specialization.

The rational coefficients are transcribed from accepted `yangbaxter.tex:134–148`
(8.3) in the shared declarative `audits/a2_spectral_spec.json`. Nine coefficient
comparisons at u and the substituted argument verify Rpoly=N Rcheck against the
unchanged portable JSON formula. The outer [x] in the E coefficient is retained.
The skein input (8.2), lines 115–125, is
S-Sinv=t*(H-K+(q-q^-1)^2*(U-I)), t=(q-q^-1)[n+1][2n][3n]/[6n].
Crossing rotates the split ordinary generators before eliminating S with this
relation, then expands all coefficients into D0,...,D15. D4 denotes H squared
in the declared basis. Both rational and polynomial crossing residuals are
reported for **every** diagram coordinate, including all zeros. This is a
coefficientwise calculation, not a check only in representations.

The manuscript's rotation table and diagram basis are assumed mathematical
specifications. Their geometric validity and basis independence are not proved
by this computation. There is no unresolved scalar, substitution or normalization
ambiguity in these checks. The separate 92-entry dilute A(3) assembly gap is
unaffected and is not relevant to this A(2) identity calculation.

Hard limits: 60 seconds per process group, 300 seconds for the entire combined
Python+C batch. The completed combined batch took about 1.319 seconds; no limit
was extended. Peak memory is Linux wait4 ru_maxrss. Results contain every residual
as numerator/denominator and every matrix row/column in zero-based array order.
FAIL would retain nonzero entries; the launcher records ERROR and TIMEOUT as
separate statuses with stderr and resource measurements.

No authoritative data, manuscript, earlier audit evidence or M2 source was
modified. All new evidence is in the research repository, not workspace-only.
No commit or publication was made. Source hashes/base commit and comparison are
in `audits/a2_spectral_provenance.json` and `audits/a2_spectral_comparison.json`.
