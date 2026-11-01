# Exceptional-series R-matrices

Exact representation matrices and computational tools accompanying Bruce W.
Westbury and Paul Zinn-Justin,
[*A uniform trigonometric R-matrix for the exceptional series*](https://arxiv.org/abs/2406.01348).

The repository provides three ways to work with the constructions in the paper:

- **Portable JSON data:** 542 sparse matrices, with exact coefficients, basis
  conventions, scalar definitions and diagram embeddings.
- **ExceptionalDiagrams:** a Macaulay2 package for diagram operations, skein
  reduction, ordinary and dilute representations, braiding and spectral R-matrices.
- **Exact verification:** C/FLINT and Python/FLINT programs for algebra relations,
  unitarity, crossing and the Yang–Baxter equation, together with saved results.

## Using the data

Start with the [data catalogue](data/publication.json) and the
[format guide](FORMAT.md). The matrices comprise 110 ordinary A(3) generators,
330 dilute A(3) generators, 80 dilute A(2) diagrams and 22 polynomial spectral
matrices. Scalars lie in exact rational-function fields. Matrix indices are
zero-based, and row vectors act on the right.

The format guide explains the normalization factors for raw dilute generators
and the polynomial normalization of the spectral matrices. A
[SageMath example](examples/README.md) demonstrates exact import and unitarity.

## Using Macaulay2

With Macaulay2 and its `VectorGraphics` package installed, run this from the
repository root in Macaulay2:

```m2
needsPackage("ExceptionalDiagrams",
    FileName=>"macaulay2/ExceptionalDiagrams.m2");
s1 = rep(3,(braid())_1,Dilute=>false);
s2 = rep(3,(braid())_2,Dilute=>false);
assert(s1*s2*s1 == s2*s1*s2);
```

The [package guide](macaulay2/README.md) covers installation, spectral matrices,
normalizations and tests. To compare the package with all JSON matrices and run
its package and installation tests:

```sh
python3 tools/check_macaulay2_data.py --package-tests --output /tmp/m2-check.json
```

This command requires Python with `jsonschema` and Macaulay2. It performs 952
exact matrix comparisons, including both normalizations of the raw dilute data.
Choose a fresh output filename for each run.

## Running the verification suite

Structural validation requires Python >=3.10 and `jsonschema` >=3.2:

```sh
python3 tools/validate_publication.py --self-test
```

For the C/Python mathematical suite, install `python-flint==0.9.0`, a C11
compiler, FLINT development headers, GMP and MPFR, then run:

```sh
python3 verify_release.py --run-name checks
```

The runner builds the C programs, checks ordinary A(3) relations, runs both A(2)
spectral implementations, and checks the generic Yang–Baxter equation in C and
Python. It also runs the SageMath example when SageMath is available. Use a fresh
run name; each worker has a 60-second limit and each mathematical batch a
300-second limit. The suite runs on Linux/POSIX and saves JSON results, logs and
a Markdown summary. Macaulay2 verification is a separate command, shown above.

See the [dependency guide](DEPENDENCY_AUDIT.md) for component requirements and
the [verification overview](AUDIT_COVERAGE.md) for the mathematical scope.
[Recorded results](CLEAN_CHECKOUT_REPORT.md) summarize the included evidence.
The [GitHub Actions workflow](.github/workflows/macaulay2.yml) runs structural
validation, package tests and exact package/data comparisons.

## Repository guide

- [Data conventions and verification](DATASET_PROVENANCE.md)
- [File and directory guide](PUBLICATION_INVENTORY.md)
- [Maintenance and contributions](PUBLICATION_DECISIONS.md)
- [Ordinary A(3) relations](audits/c/a3_relations/REPORT.md)
- [A(2) unitarity and crossing](audits/A2_SPECTRAL_COMPARISON.md)
- [Generic Yang–Baxter verification](audits/python/REPORT.md)

## Citation and licence

Please cite the accompanying paper when using these data or computations.
[CITATION.cff](CITATION.cff) contains the citation details.

The data, documentation and software are licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
Give appropriate credit, link to the licence and indicate changes when sharing
or adapting the material. Credit Bruce W. Westbury and Paul Zinn-Justin for the
companion repository, and Paul Zinn-Justin for ExceptionalDiagrams.
External dependencies retain their own licences.
