# Ordinary A(3) relation verification

**All 1,605 applicable relation checks pass exactly in the eleven supplied
representations.** The [manifest](manifest.json) contains 150 checks with explicit
coefficients, ordered generator words and representation applicability.

The [saved results](../../../verification/ordinary_a3/results.md) give per-representation
status, time and peak memory. Exact per-relation records are in
[verification/ordinary_a3/](../../../verification/ordinary_a3/).

## Relations checked

The thirty H,K,U defining equalities comprise eighteen local identities,
eleven mixed-position identities and the full quartic. Additional checks cover
both local A(2) multiplication tables, polynomial prescriptions for K and U,
local skein and inverse relations, braid matrices and their inverses, the braid
relation, quintic relations, and the top quotient.

[INVENTORY.md](INVENTORY.md) lists all identifiers and their roles. The thirty
defining checks implement the displayed six-generator presentation in Section 6
of the [paper](https://arxiv.org/abs/2406.01348).

The nine top-quotient checks apply to X3, Y3, Y3_star, A, C and C_star. They include
two cubics, three quartics and the four zero generators K1,K2,U1,U2. Each other
representation has 141 applicable checks; the saved logs mark its nine quotient
entries `NOT APPLICABLE`.

## Arithmetic and scope

The verifier loads all ten ordinary generator matrices from JSON and checks
each residual entry over QQ(p,q). Its FLINT rational-function evaluator expands
scalar aliases and caches ordered words. The saved run used GCC 11.4.0 and
FLINT runtime 2.8.0. Peak resident memory is the process high-water mark.

The result establishes the encoded identities in these representations.
The paper supplies the abstract presentation, basis and faithfulness arguments.
Extending the braid-generator checks to the degree-seven relation requires its
explicit word-and-coefficient formula; this is recorded as an open task in the
manifest.

## Running the check

With a C11 compiler, FLINT development headers, GMP and MPFR installed, run from
the repository root:

```sh
make -C audits/c/a3_relations
mkdir -p checks
audits/c/a3_relations/runner checks/ordinary_a3
```

Use a fresh output location. The runner enforces 60 seconds per representation
and 300 seconds per batch, and writes JSON logs plus a Markdown results table.
