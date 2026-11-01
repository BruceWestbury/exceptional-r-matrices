# Matrix data format

The [catalogue](data/publication.json) is the entry point for format 0.3.0.
It lists each JSON file, its schema and its role. This guide describes how to
interpret the stored scalars, matrices, normalizations and diagram embeddings.

## Data layout

| Path | Contents | Normalization |
|---|---|---|
| `data/local_a2.json` | Ordinary A(2) coefficients, multiplication tables and five characters | Ordinary, alpha=1 |
| `data/a3.json`, `data/representations/` | Ordinary A(3) specification and 110 generator matrices | Ordinary, alpha=1 |
| `data/dilute_a3.json`, `data/dilute_representations/` | Registry and 330 dilute A(3) generators | Raw matrices with registry multipliers |
| `data/dilute_a2.json`, `data/dilute_a2_representations/` | Five representations, with sixteen diagrams each | Raw matrices with registry multipliers |
| `data/spectral_r.json` | Spectral expansion, prefactor, crossing and distinguished values | Polynomial R-matrix |
| `data/dilute_a3_embeddings.json` | Local diagram embeddings and generator correspondence | Apply `paper2` normalization first |
| `data/spectral/` | Two polynomial spectral positions in eleven representations | Polynomial R-matrix |
| `data/basis_maps.json` | Diagonal conjugations, occupancy and basis order | Direction specified per map |
| `data/publication_provenance.json` | Payload hashes and verification metadata | Metadata |

Top-level `provenance` objects give the paper citation, a description and public
source references. The repository manifest maps file paths to SHA-256 hashes;
the data provenance file supplies the payload hashes used by validation.

## Matrices and coordinates

All indices are zero-based. A sparse matrix has `operator`, `rows`, `cols` and
row-major `entries: [[row, column, scalar], ...]`. Every omitted entry is zero;
`entries: []` represents the zero matrix of the declared dimensions.

Vectors act on the **right as rows**. A word `[A,B,C]` represents ABC, multiplied
in that order. Coordinate labels name basis vectors; the integer row and column
indices specify their storage positions.

The three-string representation order is
I, L, X2, Y2, Y2_star, X3, Y3, Y3_star, A, C, C_star. Ordinary and dilute
representations have their own dimensions. Full occupancy comes first in the
dilute basis, followed by the sectors listed in `basis_maps.json`.
Ordinary A(0) and A(1) sectors are one-dimensional identity spaces, A(2) sectors
use the character table, and full A(3) sectors use the ordinary matrices.

## Exact scalar grammar

Scalars lie in QQ(p,q), or QQ(p,q,u) for spectral matrices, with algebraically
independent variables. Expressions use the following grammar:

- Integer literals and declared identifiers.
- Parentheses and unary minus.
- Explicit `+`, `-`, `*` and `/` operations.
- `^` with a signed integer literal exponent.

For example, `(p^2*q^-1-p^-2*q)/(q-q^-1)` is an exact rational function.
Powers bind before unary minus; multiplication/division and addition/subtraction
associate left to right within their respective precedence levels.

Resolve scalar aliases in dependency order. Ordinary matrices use coefficients
from `local_a2.json` and `a3.json`; raw dilute matrices use p and q. Files with
`coefficient_definitions` supply additional local aliases. In an entry such as
`(numerator)/spectral_denominator`, the denominator is part of the entry's value.
Expanding the alias gives the complete rational function, including any
Laurent-clearing monomial in u.

File-valued `*_ref` paths are relative to the containing JSON file.
`field_ref: F` names a coefficient field. Catalogue paths and verification-evidence
paths are relative to the repository root.

## Dilute diagrams and normalization

D0,...,D15 follow ExceptionalDiagrams' `lst2` order; their graphs and indices are
stored in `dilute_a2.json`. D4 is the composite D3*D3. The other graphs use left
boundary 0,1 and reversed right boundary 3,2, with internal vertices starting at 4.
The two-string dilute dimensions are 2 for I, 3 for L and 1 for X2, Y2 and Y2_star.
The latter three representations use ordinary D0–D4 and zero for D5–D15.

For the spectral normalization, multiply each raw diagram matrix by its registry
`paper2_multiplier`. To use the package's `paper` convention instead, select
`paper_multiplier`. Apply the selected factor once. Embeddings are sums of
ordered words in these normalized G matrices, and D4 is then formed as D3*D3.
`generator_expressions` expresses spectral operators in the local diagrams.
In particular, the dilute braid is the full-occupancy ordinary braid plus
D6+D7+D15.

The [basis-map registry](data/basis_maps.json) specifies diagonal maps for
comparison with selected displayed tables in the paper, including dilute A(3)
I and L and dilute A(2) L. For row coordinates,

```text
M_paper = D M_JSON D^-1
v_paper = v_JSON D^-1
```

Apply the selected generator normalization before this change of coordinates.
The A(2) L map is `diag(beta^-1,1,1)`, from vertex counts `[1,0,0]` in its basis
diagrams. Ordinary Y2 has the same basis in the data, package and paper. Direct
package/data comparisons use the common JSON/package coordinates.

## Polynomial spectral normalization

Bracket notation uses p=q^n and u=q^x as shorthand for

```text
[an+bx+c] = (p^a*u^b*q^c - p^-a*u^-b*q^-c)/(q-q^-1).
```

The variables p,q,u remain independent. The stored spectral matrix is

```text
Rpoly(u) = N(u) Rcheck(u)
N(u) = ([6n]^2[n]/([3n]^2[2n])) [n+x+1][x-1][2n+x][3n+x].
```

The nine-term expansion in `data/spectral_r.json` implements the spectral
R-matrix of Section 8 of the [paper](https://arxiv.org/abs/2406.01348).
Its coefficients are Laurent polynomials in u with rational coefficients in
p,q. Distinguished values use the rescaled limits `u^4 Rpoly(u)` at zero and
`u^-4 Rpoly(u)` at infinity, and ordinary substitution at u=1. The JSON records
every scalar factor.

Crossing takes the form

```text
Rot(Rpoly(u)) = Rpoly(p^-3*u^-1).
```

Rotation acts linearly on the diagram basis, swapping (I,U),
(S_ordinary,Sinv_ordinary), (K,H), (E,D_squared), and fixing T,D,O.
First expand the dilute expressions as

```text
one = I + D_squared + O
S_dilute = S_ordinary + D + O
B = D + D_squared.
```

Then apply the specified rotation to each diagram and reduce with the skein
relation. The [A(2) comparison report](audits/A2_SPECTRAL_COMPARISON.md) describes
the coefficientwise verification.

## Validation and import

```sh
python3 tools/validate_publication.py --self-test
```

This command uses Python >=3.10 and jsonschema >=3.2. It checks the local schemas,
dimensions, sparse ordering, indices, scalar grammar, alias dependencies,
references, bases, normalizations, spectral positions, occupancy coordinates and
payload hashes. Ten negative fixtures test rejection of malformed data.
Exact identities are checked by the mathematical programs listed in
[AUDIT_COVERAGE.md](AUDIT_COVERAGE.md).

The [SageMath example](examples/README.md) demonstrates exact import. The
[Macaulay2 guide](macaulay2/README.md) explains package/data comparisons, including
the registry multipliers and spectral prefactor.
