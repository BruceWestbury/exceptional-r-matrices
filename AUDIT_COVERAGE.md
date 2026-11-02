# Mathematical verification coverage

This guide connects assertions in the accepted manuscript of
[*A uniform trigonometric R-matrix for the exceptional series*](https://arxiv.org/abs/2406.01348)
to exact computations and their recorded evidence. Parameters are algebraically
independent unless a specialization is stated. The paper supplies the abstract
algebraic and categorical arguments; the computations have the scopes below.

The results cited here are **recorded successful runs**, not fresh verification
of the current checkout. Some recorded input hashes differ from current files;
such differences alone are not mathematical failures. Run commands from the
repository root, preferably in a disposable checkout, using fresh output paths.
C programs require a C11 compiler, FLINT, GMP and MPFR; the Python spectral
programs require `python-flint==0.9.0`. Ordinary, A(2) and YBE runners enforce
60-second worker and 300-second batch limits.

## 1. Ordinary A(3) relations

**Statement and reference.** Definition 6.9 defines the localized algebra over
$\mathbb Q(p,q)$ by generators $H_i,K_i,U_i$, $i=1,2$.
Equations (6.27)–(6.38), with $j=3-i$, are

$$
\begin{gathered}
H_iK_i=K_iH_i=\tau K_i,\qquad H_iU_i=U_iH_i=\phi U_i,\\
K_i^2=\phi K_i,\qquad K_iU_i=U_iK_i=0,\qquad U_i^2=\delta U_i,\\
H_1K_2H_1=H_2K_1H_2,\qquad K_iU_jK_i=H_jU_iH_j,\\
K_iU_jH_i=H_jU_iK_j,\qquad K_iU_jU_i=H_jU_i,\\
U_iU_jK_i=U_iH_j,\qquad U_iU_jU_i=U_i,\\
(H_i-\xi)(H_i-\zeta)(H_i-\zeta^*)=b_2K_i+b_1U_i.
\end{gathered}
$$

The full quartic equation (6.39) is also checked, with its Appendix A
coefficients; it is encoded as `quartic_full` in the
[relation manifest](audits/c/a3_relations/manifest.json).

**Scope and method.** The [C/FLINT verifier](audits/c/a3_relations/verify.c)
evaluates ordered words entry by entry over $\mathbb Q(p,q)$ in all eleven
ordinary representations $I,L,X_2,Y_2,Y_2^*,X_3,Y_3,Y_3^*,A,C,C^*$, using
[`data/representations/`](data/representations/). The manifest distinguishes:

- 30 defining equalities from (6.27)–(6.39);
- local multiplication rules and consequences, inverse and polynomial
  prescriptions, and the braid and quintic relations (6.49)–(6.50);
- nine top-quotient checks, including (6.4)–(6.7) and $K_i=U_i=0$.

The [inventory](audits/c/a3_relations/INVENTORY.md) identifies all 150 checks;
these are not 150 distinct defining relations.

**Reproduce.**

```sh
make -C audits/c/a3_relations
audits/c/a3_relations/runner /tmp/exceptional-ordinary-check
```

**Recorded result and limitations.** The
[results](verification/ordinary_a3/results.md) and per-relation
[`rep_*.jsonl` records](verification/ordinary_a3/) report **1,605 successful
checks**. The nine quotient checks apply only to
$X_3,Y_3,Y_3^*,A,C,C^*$; their omission in each of the other five representations
accounts for **45 NOT APPLICABLE** entries. This verifies the encoded relations
in the supplied representations, not completeness or faithfulness of the
abstract presentation. The unprinted degree-seven braid-generator relation is
not included: its explicit words and coefficients are needed. See the
[ordinary audit report](audits/c/a3_relations/REPORT.md).

## 2. Unitarity and spectral normalisation

**Statement and reference.** For the $\check R(u)$ of (8.3), Theorem 8.1 asserts

$$
\check R(u)\check R(u^{-1})=1. \tag{8.11}
$$

Section 8.8 defines $\check R^{\mathrm{poly}}(u)=N(u)\check R(u)$, where

$$
N(u)=\frac{[6n]^2[n]}{[3n]^2[2n]}
[n+x+1][x-1][2n+x][3n+x].
$$

Here $p=q^n$ and $u=q^x$ express the bracket convention, not constraints on the
independent variables. Thus polynomial unitarity is
$\check R^{\mathrm{poly}}(u)\check R^{\mathrm{poly}}(u^{-1})
=N(u)N(u^{-1})1$, not generally the identity matrix.

**Scope and method.** Separate
[Python/FLINT](audits/python/a2_spectral/verify.py) and
[C/FLINT](audits/c/a2_spectral/verify.c) implementations check the five dilute
$A(2)$ representations $I,L,X_2,Y_2,Y_2^*$ over $\mathbb Q(p,q,u)$.
They use [`data/dilute_a2_representations/`](data/dilute_a2_representations/),
the registry normalization, generator expressions in
[`data/dilute_a3_embeddings.json`](data/dilute_a3_embeddings.json),
[`data/spectral_r.json`](data/spectral_r.json) and the shared
[identity specification](audits/a2_spectral_spec.json).
Python multiplies rational matrices directly; C clears denominators exactly
before polynomial multiplication. Both also check the scalar relationship
between rational and polynomial coefficients.

**Reproduce.** Each command also performs the crossing check in Section 3.

```sh
make -C audits/c/a2_spectral
python3 audits/run_a2_spectral.py --backend python --results /tmp/exceptional-python-a2
python3 audits/run_a2_spectral.py --backend c --results /tmp/exceptional-c-a2
```

**Recorded result and limitations.** Both implementations record zero residual
matrices in all five representations: see the
[Python results](audits/python/a2_spectral/verification_results/results.json),
[C results](audits/c/a2_spectral/verification_results/results.json) and the
individual representation `*.stdout.json` files alongside them. The
[comparison report](audits/A2_SPECTRAL_COMPARISON.md) explains the rational and
polynomial checks. These are generic exact identities; interpreting them as an
identity of the abstract algebra uses the paper's representation-theoretic results.

The optional [SageMath example](examples/README.md) instead checks
$\check R_i^{\mathrm{poly}}(2)\check R_i^{\mathrm{poly}}(1/2)
=N(2)N(1/2)1$ at both positions in dilute $I$, over $\mathbb Q(p,q)$:

```sh
timeout -s KILL 60s sage -python examples/import_spectral.py
```

Its [recorded PASS](verification/sage_retry.stdout.txt) is an exact specialised
import check, not a substitute for generic unitarity.

## 3. Crossing symmetry

**Statement and reference.** Theorem 8.1, equation (8.13), states

$$
\operatorname{Rot}(\check R(u))=
\frac{[x][n+x][3n+x+1][2n+x-1]}
{[n+x+1][x-1][2n+x][3n+x]}
\check R(p^{-3}u^{-1}).
$$

With the preceding normalization this is equivalent to

$$
\operatorname{Rot}(\check R^{\mathrm{poly}}(u))
=\check R^{\mathrm{poly}}(p^{-3}u^{-1}). \tag{8.15}
$$

**Scope and method.** The two A(2) implementations check every coefficient in
the sixteen-diagram basis over $\mathbb Q(p,q,u)$, without evaluating in
representations. They expand the dilute operators, apply the prescribed
rotation of Section 8.8,

$$
I\leftrightarrow U,\quad S\leftrightarrow S^{-1},\quad
K\leftrightarrow H,\quad E\leftrightarrow D^2,
\qquad T,D,O\text{ fixed},
$$

and reduce using the normalized skein relation (8.2). Here $S$ is the ordinary
braid component; the dilute braid is first split as prescribed in the paper.
They separately verify the substitution and
$N(u)c(u)=N(p^{-3}u^{-1})$, where $c(u)$ is the prefactor in (8.13).

**Reproduce.** Run the bounded A(2) commands in Section 2. For crossing alone,
after building the C verifier:

```sh
timeout -s KILL 60s python3 audits/python/a2_spectral/verify.py crossing
timeout -s KILL 60s audits/c/a2_spectral/verify crossing
```

**Recorded result and limitations.** The
[Python](audits/python/a2_spectral/verification_results/crossing.stdout.json)
and [C](audits/c/a2_spectral/verification_results/crossing.stdout.json)
records contain sixteen zero rational residuals, sixteen zero polynomial
residuals and zero scalar-consistency residuals. Rotation and the skein relation
are mathematical inputs: the programs do not independently establish their
geometric interpretation or the diagram-basis theorem.

## 4. Parametrised Yang–Baxter equation

**Statement and reference.** Theorem 8.1, equation (8.12), asserts

$$
\check R_1(u)\check R_2(uv)\check R_1(v)
=\check R_2(v)\check R_1(uv)\check R_2(u),
$$

where $\check R_1=\check R\otimes\mathrm{id}^{\square}_1$ and
$\check R_2=\mathrm{id}^{\square}_1\otimes\check R$ use the dilute spectator
identity, as in Section 8.4.

**Scope and method.** The
[C/FLINT verifier](benchmarks/flint_ybe/verifier.c) and
[Python/FLINT verifier](audits/python/spectral_ybe.py) construct both polynomial
spectral matrices from the thirty generators in each of the
[eleven dilute representations](data/dilute_representations/). They check every
entry of the two triple products over $\mathbb Q(p,q,u,v)$, using exact
polynomial arithmetic after denominator clearing. Both sides acquire the same
nonzero scalar, so the corresponding rational-function identity follows in each
representation. Numerical or finite-field sampling is not used.

The implementations have separate spectral construction and evaluation code,
but share mathematical inputs, conventions and the FLINT library family.
They also share [`local_embeddings.json`](reports/paper_audit/local_embeddings.json)
and the rational reference matrices `reports/paper_audit/spectral_*.json`.
The latter are used only for comparison with
$\check R^{\mathrm{poly}}=N\check R$, not to construct the spectral matrices.

**Reproduce.**

```sh
make -C benchmarks/flint_ybe
benchmarks/flint_ybe/runner /tmp/exceptional-c-ybe
python3 audits/python/run.py --output /tmp/exceptional-python-ybe
```

After its own calculations, the Python runner reads the saved
`benchmarks/flint_ybe/results.json` for its C/Python comparison report. It does
**not** automatically read the new `/tmp/exceptional-c-ybe/results.json`, and has
no command-line option selecting that file. Compare the two new output
`results.json` files directly to avoid replacing saved evidence. The existing
full-suite launcher instead temporarily supplies the newly generated C result
at the expected path and restores the saved file afterwards.

**Recorded result and limitations.** All eleven representations passed in
[C](benchmarks/flint_ybe/verification_results/results.md) and
[Python](verification/python_ybe/REPORT.md). Adjacent `rep_*.jsonl` records
report zero YBE residuals and successful rational/polynomial comparisons.
These computations verify generic identities in the supplied matrices; the
abstract algebra and categorical interpretation require the paper's arguments.

## 5. Additional evidence and limitations

The Macaulay2 [package tests](macaulay2/tests/exceptional-diagrams.m2) additionally
check bar invariance (8.10), braid identities, unitarity and restrictions of fully
occupied diagrams to ordinary summands (§7.2). The
[recorded run](verification/macaulay2.json) reports successful native tests and
`identities`, `recipes`, `context` and `restrictions` groups in both `paper` and
`paper2` normalizations. These are package-internal checks, not independent
JSON/FLINT proofs. Optional `multiplication` and `ybe` suites exist in the test
file but were not run by that recorded launcher invocation.

```sh
python3 tools/check_macaulay2_data.py --package-tests --output /tmp/exceptional-m2.json
```

This launcher enforces 60-second workers and **separate 300-second budgets**
for data comparisons, each package configuration and installation. Its recorded
total was **439 seconds**, not a single 300-second batch.

The following distinctions and limits apply throughout:

- **Identity verification** evaluates an encoded mathematical equality exactly.
  Structural JSON validation checks format and references; Macaulay2/JSON
  comparison checks agreement of two data forms; manuscript/JSON comparison
  checks fidelity to displayed entries. The latter three are consistency or
  data-fidelity checks, not additional mathematical proofs.
- The computations do not independently prove an abstract presentation,
  completeness, faithfulness, irreducibility or the basis and dimension
  arguments established in the paper. The degree-seven braid relation is not
  included in the current ordinary audit.
- No dedicated public verification was identified for the dilute generator
  identities (8.4)–(8.6) or special values (8.7)–(8.9). They must not be inferred
  from successful unitarity or YBE checks, or from formulas stored in JSON.
  Bar invariance (8.10) has the package evidence described above.
- No independent comparison with known exceptional Lie algebra R-matrices is
  supplied for §8.9, including its $A_1$ and $A_2$ fusion descriptions. Generic
  YBE does not establish these identifications. The manuscript's expectation
  language for the general minimal-affinisation interpretation remains distinct
  from its proved identities. Specialising rational identities also requires
  the relevant expressions to be defined.
- The [ordinary-to-dilute construction evidence](audits/python/dilute_transcription/REPORT.md)
  covers 298 complete and 32 partial matrices: all 8,518 reconstructed entries
  agree, but 92 transition entries remain independently unreconstructed.
  Package agreement with all 330 matrices does not close that construction gap.
