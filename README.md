# A uniform trigonometric $R$-matrix for the exceptional series

## The mathematical data and the accompanying software

This repository supports the paper [A uniform trigonometric R-matrix for the exceptional series](https://arxiv.org/abs/2406.01348) (accepted for publication in *Communications in Algebra*).

The main result of the paper is the construction of a spectral $R$-matrix which interpolates the spectral $R$-matrices in the exceptional series of simple Lie algebras. The fundamental property of this $R$-matrix is that it satisfies the parametrised Yang–Baxter equation. This property is verified by a direct calculation in an algebra of dimension 287 over a function field in two variables, with two spectral parameters. This algebra is a direct sum of eleven matrix algebras, and the dimensions of the irreducible representations are 11, 7, 6, 6, 5, 3, 3, 2, 1, 1, 1. The Yang–Baxter equation is verified by checking that it is satisfied in each irreducible representation.

The paper describes the construction and mathematical context for these matrices but does not include all eleven matrices, since this would be neither practical nor particularly useful. The primary aim of this repository is to provide public access to all eleven matrices.

The matrices are stored in JSON, with the intention that they can be read by any computer algebra system. They are intended to be precisely the matrices described in the paper, so that any ambiguity or potential discrepancy can be resolved by comparison with the matrices supplied in this repository. Furthermore, their mathematical properties can be checked independently after reading them into a computer algebra system.

The $R$-matrices are constructed using the representation theory of a smaller algebra. This algebra has dimension 80 and is also a direct sum of matrix algebras. The dimensions of its irreducible representations are 5, 4, 3, 3, 3, 2, 2, 1, 1, 1, 1. The algebra is defined by a finite presentation. This repository also supplies the matrices of all generators in all irreducible representations. These matrices are stored in JSON and can therefore be read by any computer algebra system.

The secondary aim of this repository is to provide explicit checks of the properties of these matrices asserted in the paper. The principal checks are that the defining relations of the smaller algebra are satisfied in every irreducible representation, and that the $R$-matrices satisfy the Yang–Baxter equation in all eleven representations.

The paper also establishes that the interpolating $R$-matrices specialise to known $R$-matrices for the exceptional simple Lie algebras. These identifications are not checked in this repository, since independent, authoritative matrix data for these specialisations are not available.

The repository provides two separate implementations of these checks: one written in C using FLINT and one written in Python using FLINT. Both can be downloaded and run locally. They can also serve as templates for checking the same identities independently in other computer algebra systems.

The repository includes programs for comparing the Macaulay2 and JSON versions of the matrices, allowing for documented changes of basis and normalisation. These comparisons check agreement between the two formats; they do not establish the mathematical properties of the matrices.

The repository provides three ways to work with the constructions in the paper:

- **Portable JSON data:** 542 sparse matrices, with exact coefficients, basis
  conventions, scalar definitions and diagram embeddings.
- **ExceptionalDiagrams:** a Macaulay2 package for diagram operations, skein
  reduction, ordinary and dilute representations, braiding and spectral R-matrices.
- **Exact verification:** C/FLINT and Python/FLINT programs for algebra relations,
  unitarity, crossing and the Yang–Baxter equation, together with saved results.

## Organisation of the repository

### `data/` — The matrices

This is the main mathematical content of the repository. It contains the explicit matrices in JSON format, together with information identifying their representations, generators, coefficients and conventions.

The JSON files are the standard form of the data supplied by the repository. They are intended for use in further calculations and for comparison with the formulas in the paper.

### `macaulay2/` — Matrices in Macaulay2 format

This directory contains matrices in Macaulay2 format supplied by Paul Zinn-Justin. They are included for readers who wish to work with the matrices directly in Macaulay2.

The standard form of the data in this repository is the JSON version in `data/`. The Macaulay2 matrices may use different bases or normalisations. Programs are provided to compare the two versions, allowing for these differences.

### `schema/` — The mathematical format of the data

This directory contains precise specifications of the JSON files.

These specify how matrices, coefficients, parameters and other mathematical information are represented. For example, they distinguish a rational function from an arbitrary string of characters and specify how the entries of a matrix are arranged.

These specifications make it possible to check that the data have the expected form and to write programs that interpret them consistently.

They concern the representation of the mathematics, not the truth of the mathematical identities.

### `examples/` — Using the matrices

This directory contains examples of calculations with the supplied data.

Their purpose is to show how to read the matrices into a computer algebra system and use them as mathematical objects, rather than requiring readers to implement the file formats themselves.

### `tools/` — Programs for calculations with the data

This directory contains programs for reading and examining the matrices and for carrying out calculations with them.

Some programs check that different versions of the matrices agree, allowing for changes of basis or normalisation. Others perform calculations needed to test mathematical identities.

These programs make the data more useful than a collection of tables: they allow calculations to be repeated and adapted to new questions.

### `audits/` — Checking mathematical identities

This directory contains calculations that test relations satisfied by the matrices.

These include defining relations of the representations and identities involving the spectral parameter, such as the Yang–Baxter equation.

The important point is that the relations are evaluated using the supplied matrices, rather than merely being inferred from their construction.

Where the calculations are incomplete, the outstanding cases are identified.

### `verification/` — Results of calculations

This directory contains records of the results obtained by running the checking programs.

These records make it possible to distinguish a mathematical identity that has been checked explicitly from one that is expected on theoretical grounds or remains to be investigated.

Where recorded, the precise versions of the data and programs are identified, so that the calculations can be repeated with the same inputs.

### `tests/` — Checking the programs

A calculation is only useful if the program performing it works as intended.

This directory contains tests of the programs themselves. These include checking known examples and, in some cases, deliberately introducing incorrect data to confirm that an error is detected.

Such tests do not prove the mathematical identities, but they increase confidence that the programs used to check those identities are functioning correctly.

### `benchmarks/` — The cost of exact calculations

This directory contains measurements of the computational resources required for selected calculations.

For example, checking the Yang–Baxter equation with matrices over polynomial rings can involve substantial symbolic computation.

These measurements help other researchers assess the feasibility of repeating or extending the calculations, and compare different methods for exact arithmetic.

### `reports/` — Detailed accounts of calculations

This directory contains longer accounts of particular calculations, including methods, results, difficulties and unresolved questions.

These reports supplement the paper by recording computational details that would be inappropriate to include in a mathematical article but may be important to someone attempting to reproduce or extend the work.

### `verify_release.py` — Repeating the checks

This program runs a collection of checks on the supplied data and programs.

It provides a convenient way to repeat the calculations used to assess the consistency of the files and the mathematical relations that have been tested. The individual calculations and their results are described elsewhere in the repository.

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

The file `FORMAT.md` explains the JSON representation of the mathematical objects, while `AUDIT_COVERAGE.md` describes which mathematical relations have been checked.

`DATASET_PROVENANCE.md` explains where the matrices came from and how they relate to the original calculations and the paper.

The remaining documents give more detailed information about the supplied files, the programs required to use them and the calculations performed before publication.

## Citation and licence

Please cite the accompanying paper when using these data or computations.
[CITATION.cff](CITATION.cff) contains the citation details.

The data, documentation and software are licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
Give appropriate credit, link to the licence and indicate changes when sharing
or adapting the material. Credit Bruce W. Westbury and Paul Zinn-Justin for the
companion repository, and Paul Zinn-Justin for ExceptionalDiagrams.
External dependencies retain their own licences.
