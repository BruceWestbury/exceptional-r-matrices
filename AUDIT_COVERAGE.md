# Verification coverage

The suite combines structural validation, agreement with ExceptionalDiagrams,
and exact algebraic identities in the supplied representations.

| Check | Scope | Recorded result |
|---|---|---|
| JSON validation | 47 files, six schemas, 542 matrices, scalar grammar, references and payload hashes | PASS; ten malformed-data fixtures rejected |
| Macaulay2 comparison | All 542 matrices; both normalizations for 410 raw dilute matrices | 952 exact matrix comparisons PASS |
| Macaulay2 package | Five built-in `TEST` blocks, standalone generic tests and installed-package checks in both normalizations | PASS |
| Ordinary A(3) relations | 150 encoded checks with representation-specific applicability | 1,605 exact checks PASS |
| Dilute A(2) unitarity | Five representations over QQ(p,q,u), in C and Python | PASS |
| Dilute A(2) crossing | All sixteen diagram coefficients, in C and Python | PASS |
| Dilute A(3) Yang–Baxter equation | Eleven representations over QQ(p,q,u,v), in C and Python | PASS |
| SageMath import | Scaled unitarity at u=2 and u=1/2 over QQ(p,q), both positions in dilute I | PASS |

## Interpretation

The mathematical workers use exact rational functions in algebraically
independent variables. The C and Python implementations construct and evaluate
the spectral matrices separately. They share the JSON specifications and the
FLINT library family; their completed results are compared afterwards.

The ordinary A(3) checks cover the displayed six-generator H,K,U relations,
local multiplication tables, braid prescriptions, braid and quintic relations,
and the top quotient. Nine quotient checks apply to the six top representations;
the other five representations each have 141 applicable checks.

Crossing uses the diagram basis and rotation specified in the paper. The
computational conclusions concern the encoded identities and the supplied
representations. The paper provides the categorical conventions and arguments
for the abstract presentations, bases and dimensions. Specialization of the
rational identities requires the relevant expressions to be defined.

Package comparisons establish exact agreement between two usable forms of the
data. The C/Python checks establish the stated algebraic identities for those
matrices. Structural validation checks the data format and internal consistency.

## Further construction checks

The saved ordinary-to-dilute reconstruction evidence covers 298 of 330 complete
matrices and 32 partial matrices. All 8,518 reconstructed entries agree exactly.
A complete independent reconstruction additionally requires 92 transition-block
entries, using rectangular ordinary morphisms with compatible cup, cap and
trivalent-vertex normalizations. See the
[construction report](audits/python/dilute_transcription/REPORT.md).

Extending the braid-generator presentation checks to the degree-seven relation
requires an explicit word-and-coefficient formula. The existing manifest gives
complete computational coverage of the displayed H,K,U equalities.

## Results and commands

[Recorded results](CLEAN_CHECKOUT_REPORT.md) link the saved evidence.
The [main README](README.md#running-the-verification-suite) gives the suite
commands, and the [package guide](macaulay2/README.md#verification) gives the
Macaulay2 checks. Each run records its inputs and results so that its scope can
be assessed alongside the code and data.
