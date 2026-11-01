# Generic Yang–Baxter verification

**All eleven dilute A(3) representations pass the exact generic Yang–Baxter
equation in both Python/FLINT and C/FLINT.** All 287 matrix entries in the YBE
residual and all 574 entries in the two-position polynomial/rational comparisons
vanish exactly.

The [Python results](../../verification/python_ybe/REPORT.md) give timings and
memory by representation; the
[C results](../../benchmarks/flint_ybe/verification_results/results.md) give the
corresponding C summary. Each result directory includes machine-readable records.

## Calculation

Python constructs the rational spectral formula, applies the polynomial
normalization and the supplied embeddings, then evaluates both triple products
over QQ(p,q,u,v). It uses sparse matrix dictionaries, cross-cancelled fractions
and FLINT rational multivariate polynomials in degree-reverse-lexicographic order.
The C implementation uses an expanded spectral construction and exponent
substitution. Each implementation computes its own intermediates and residuals.
They share the JSON specifications and the FLINT library family.

For each representation, denominator and Laurent clearing gives a polynomial
matrix with exponent m=4. Both YBE sides acquire the common factor D³u⁸v⁸,
where D is a nonzero rational function of p,q. Worker records retain the clearing
factors and entrywise residuals. Comparisons with the rational matrices follow
the YBE calculation.

The conclusion is the generic identity in the supplied eleven representations,
with the recorded embeddings and normalization. The paper provides the
categorical interpretation and abstract algebra arguments.

## Reproduction

The [dependency guide](../../DEPENDENCY_AUDIT.md#running-components-separately)
gives the C and Python commands. Python requires python-flint 0.9.0; the C
program requires a C11 compiler, FLINT, GMP and MPFR. The saved runs used
Python 3.10.12, FLINT 3.6.0 through python-flint, and C FLINT runtime 2.8.0.

The Python runner reads the completed C summary after its own workers finish
and adds the comparison to its report. Limits are 60 seconds per representation
and 300 seconds per batch. Saved records include construction, YBE and comparison
times, total wall time, exact residuals and peak resident memory.
