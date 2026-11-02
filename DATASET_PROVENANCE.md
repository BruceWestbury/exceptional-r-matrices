# Data conventions and verification

The data implement the ordinary and dilute representations described in
[*A uniform trigonometric R-matrix for the exceptional series*](https://arxiv.org/abs/2406.01348)
and in the bundled [ExceptionalDiagrams package](macaulay2/README.md).

## Mathematical data

The [catalogue](data/publication.json) lists each JSON file, its schema and its
role. The ordinary A(3) data use the paper's ordinary normalization. Dilute
A(2) and A(3) generator files store raw matrices together with registry factors
for the package's `paper` and `paper2` normalizations. Spectral files store the
polynomial R-matrices in the normalization described in [FORMAT.md](FORMAT.md).

Ordinary Y2 uses a common basis in the paper, the JSON data and ExceptionalDiagrams.
The dilute JSON and package also share coordinates. The
[basis-map registry](data/basis_maps.json) specifies the diagonal conjugations
used to compare selected dilute matrices with the displayed tables in the paper.

## Agreement and identities

The [package comparison tool](tools/check_macaulay2_data.py) evaluates the bundled
Macaulay2 package over exact rational-function fields and compares all 542 JSON
matrices. Both normalization choices for the raw dilute matrices are tested,
giving 952 matrix comparisons. Scalar rescalings, built-in package tests,
standalone tests and installation checks have dedicated recorded results.

The C/FLINT and Python/FLINT programs verify the ordinary relations and spectral
identities. They use explicit JSON coefficients, generator words, embeddings and
rotation rules. The [coverage guide](AUDIT_COVERAGE.md) distinguishes these
identity checks from package agreement and the partial ordinary-to-dilute
construction check.

## Integrity and reproducibility

[data/publication_provenance.json](data/publication_provenance.json) supplies
payload hashes checked by the structural validator. Saved verification records
identify the inputs used for each calculation.

For a fresh verification, follow the [main README](README.md). For data or package
changes, follow the [correction guidance](README.md#corrections), update affected
integrity records and record the relevant checks.

The data, documentation and software are distributed under [CC BY 4.0](LICENSE).
