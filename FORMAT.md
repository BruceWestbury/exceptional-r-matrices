# Mathematical catalogue and data conventions

The dataset follows the constructions in the accepted manuscript of
[*A uniform trigonometric R-matrix for the exceptional series*](https://arxiv.org/abs/2406.01348).
The ordinary two-string algebra $A(2)$ (§5) is described by multiplication in
the basis $(1,H,H^2,K,U)$ and its five one-dimensional characters. The ordinary
three-string algebra $A(3)$ (§6) has eleven supplied irreducible representations;
the local operators act at positions 1 and 2.

The dilute construction (§7) allows strings to be absent. Its representation
spaces contain ordinary sectors indexed by occupancy patterns, and its operators
can connect these sectors. Consequently the dilute matrices are not simply
block-diagonal extensions of the ordinary matrices. The spectral element
$\check R(u)$ of §8 belongs to dilute $A(2)$; its two embeddings in dilute $A(3)$
give the matrices needed for the Yang–Baxter equation. Both the polynomial
spectral formula and its evaluated matrices are supplied.

The [catalogue](data/publication.json) lists all 47 JSON files, their schemas and
roles. Its format is 0.3.0; retained ordinary and dilute three-string profiles
use version 0.2.0. All use the scalar and matrix conventions below. For a direct
spectral calculation, choose a representation in the next table and load its
file from [data/spectral/](data/spectral/); no reconstruction from diagrams is
needed.

## Agreement with the paper

The JSON matrices are intended to reproduce the matrices in the accompanying paper, using the conventions and normalisations specified in this document. A comparison with the accepted manuscript identified 75 representation and spectral matrix displays that agree with the JSON data, either directly, after exact simplification, or after explicitly specified changes of basis or normalisation. The remaining auxiliary forms and representations without direct JSON counterparts are not included in this count.

This comparison concerns the correspondence between the published formulas and the supplied data. It is distinct from the mathematical audits, which verify algebraic identities satisfied by the matrices.

## Representations

The following dimensions are those declared in the JSON representation files.
The dilute labels are also recorded in the spectral files and occupancy registry.

| Representation | Ordinary $A(3)$ dimension | Dilute $A(3)$ dimension | Ordinary filename | Dilute and spectral filename |
|---|---:|---:|---|---|
| $I$ | 1 | 5 | `I.json` | `Dilute_0.json` |
| $L$ | 5 | 11 | `L.json` | `Dilute_1.json` |
| $X_2$ | 4 | 7 | `X2.json` | `Dilute_2.json` |
| $Y_2$ | 3 | 6 | `Y2.json` | `Dilute_3.json` |
| $Y_2^*$ | 3 | 6 | `Y2_star.json` | `Dilute_4.json` |
| $X_3$ | 1 | 1 | `X3.json` | `Dilute_5.json` |
| $Y_3$ | 1 | 1 | `Y3.json` | `Dilute_6.json` |
| $Y_3^*$ | 1 | 1 | `Y3_star.json` | `Dilute_7.json` |
| $A$ | 3 | 3 | `A.json` | `Dilute_8.json` |
| $C$ | 2 | 2 | `C.json` | `Dilute_9.json` |
| $C^*$ | 2 | 2 | `C_star.json` | `Dilute_10.json` |

Ordinary files are in [data/representations/](data/representations/), raw dilute
files in [data/dilute_representations/](data/dilute_representations/), and the two
polynomial spectral matrices in [data/spectral/](data/spectral/).
The ordinary $A(2)$ characters are stored together in `local_a2.json`, rather
than as separate matrix files. The five dilute $A(2)$ representations (§7.2) are:

| Representation | Dimension | File in [data/dilute_a2_representations/](data/dilute_a2_representations/) |
|---|---:|---|
| $I$ | 2 | `I.json` |
| $L$ | 3 | `L.json` |
| $X_2$ | 1 | `X2.json` |
| $Y_2$ | 1 | `Y2.json` |
| $Y_2^*$ | 1 | `Y2_star.json` |

## Data layout

| Files | Mathematical contents | Convention |
|---|---|---|
| [local_a2.json](data/local_a2.json) | Ordinary $A(2)$ coefficients, multiplication tables in $(1,H,H^2,K,U)$, relations and five characters (§5). Character columns also include $S,S^{-1}$. | Ordinary, $\alpha=1$. |
| [a3.json](data/a3.json), [representations/](data/representations/) | Ordinary $A(3)$ coefficients, relations and prescriptions (§6); **110 matrices**, ten in each representation: $H_i,K_i,U_i,S_i,S_i^{-1}$ for $i=1,2$. | Ordinary, $\alpha=1$. |
| [dilute_a2.json](data/dilute_a2.json), [dilute_a2_representations/](data/dilute_a2_representations/) | Sixteen local basis diagrams $D_0,\ldots,D_{15}$ (§7.2), with graph descriptions and **80 matrices** across five representations. | Raw matrices; apply the selected registry multiplier. |
| [dilute_a3.json](data/dilute_a3.json), [dilute_representations/](data/dilute_representations/) | Thirty generating operators $G_0,\ldots,G_{29}$ in each of eleven dilute representations: **330 matrices**. These are generators, not all 287 basis diagrams of dilute $A(3)$. | Raw matrices; apply the selected registry multiplier. |
| [dilute_a3_embeddings.json](data/dilute_a3_embeddings.json) | Expressions for the local diagrams at positions 1 and 2, with a dilute spectator identity, and expressions for the operators in the spectral formula (§8). | Sums of ordered words in `paper2`-normalized generators. |
| [spectral_r.json](data/spectral_r.json) | Nine-term generator expansion of $\check R^{\mathrm{poly}}(u)$, its scalar relationship to (8.3), crossing and distinguished values (§8.8). | The paper's polynomial normalization. |
| [spectral/](data/spectral/) | **22 matrices**: `Rpoly1` and `Rpoly2` in each dilute $A(3)$ representation, ready for direct import. | Already normalized; same coordinates as the corresponding dilute representation. |
| [basis_maps.json](data/basis_maps.json) | Occupancy sectors, their ordinary spaces and coordinate order; specified diagonal maps for comparison with selected manuscript tables. | Direction stated for each map. |
| [publication.json](data/publication.json), [publication_provenance.json](data/publication_provenance.json) | Catalogue, payload hashes and verification metadata. | Descriptions of the data, not further matrices. |

There are **542 stored matrices** in total. Multiplication-table entries are
sums of scalar multiples of ordered words; for example, the $H,K$ cell represents
$HK=\tau K$. Character values are ordered by the table's `column_order`.
The files distinguish defining relations, consequences, quotient conditions and
historical diagnostics; the latter are not additional defining relations.
The character label `Y2star` in `local_a2.json` denotes the same $Y_2^*$ labelled
`Y2_star` elsewhere.

Top-level `provenance` objects give the paper citation, a description and public
source references. The [data provenance file](data/publication_provenance.json)
supplies the payload hashes used by validation.

## Schemas

The six [schemas](schema/) describe the following mathematical records. The
catalogue specifies which schema applies to each file; a schema need not
correspond to just one algebra or one directory.

| Schema | Mathematical role and files described |
|---|---|
| [local_a2.schema.json](schema/local_a2.schema.json) | Coefficients, word expressions, multiplication tables, relations and characters of ordinary $A(2)$; used by `data/local_a2.json`. |
| [a3.schema.json](schema/a3.schema.json) | Ordinary $A(3)$ operator positions, coefficients, relation prescriptions, quotient applicability and representation references; used by `data/a3.json`. |
| [representation.schema.json](schema/representation.schema.json) | An ordinary $A(3)$ representation with an ordered basis and ten generator matrices; used by the eleven files in `data/representations/`. |
| [dilute_representation.schema.json](schema/dilute_representation.schema.json) | A raw dilute $A(3)$ representation with its basis and thirty generator matrices; used by the eleven files in `data/dilute_representations/`. |
| [portable_matrices.schema.json](schema/portable_matrices.schema.json) | Matrices with explicit coefficient field and local scalar aliases: the five sixteen-diagram collections in `data/dilute_a2_representations/` and the eleven two-position collections in `data/spectral/`. |
| [publication.schema.json](schema/publication.schema.json) | The seven supplementary specifications: `dilute_a2.json`, `dilute_a3.json`, `dilute_a3_embeddings.json`, `spectral_r.json`, `basis_maps.json`, `publication.json` and `publication_provenance.json`, all under `data/`. These describe diagrams, normalizations, embeddings, spectral coefficients, coordinates and the catalogue. |

Schemas specify the arrangement of these records, not the truth of their
mathematical assertions. The validation command below additionally checks scalar
syntax, dimensions and cross-file references; neither establishes algebraic
identities. Those computations are described in [AUDIT_COVERAGE.md](AUDIT_COVERAGE.md).

## Matrices and coordinates

All indices are zero-based. A sparse matrix has `operator`, `rows`, `cols` and
row-major `entries: [[row, column, scalar], ...]`. Every omitted entry is zero;
`entries: []` represents the zero matrix of the declared dimensions.

Vectors act on the **right as rows**. A word `[A,B,C]` represents ABC, multiplied
in that order; an empty word denotes the identity. Coordinate labels name basis vectors; the integer row and column
indices specify their storage positions.

The dilute indices 0 through 10 correspond to
I, L, X2, Y2, Y2_star, X3, Y3, Y3_star, A, C, C_star. Ordinary and dilute
representations have their own dimensions. Full occupancy comes first in the
dilute basis, followed by the sectors listed in `basis_maps.json`.
Ordinary A(0) and A(1) sectors are one-dimensional identity spaces, A(2) sectors
use the character table, and full A(3) sectors use the ordinary matrices.

## Exact scalar grammar

Scalars lie in $\mathbb Q(p,q)$, or $\mathbb Q(p,q,u)$ for spectral matrices, with algebraically
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
D6+D7+D15. In this normalization the ordinary operators satisfy
$H_{\mathrm{ordinary}}=[n+1]D_3$ and $K_{\mathrm{ordinary}}=[n+1]D_2$,
while the ordinary identity is $D_0$ and $U_{\mathrm{ordinary}}=D_1$.
The full dilute identity is `D0+D5+D8+D15`. Do not confuse the local basis
element `D4=D3*D3` with the spectral expression `D_squared=D5+D8`.

The [basis-map registry](data/basis_maps.json) specifies diagonal maps for
comparison with selected displayed tables in the paper, including dilute A(3)
I and L and dilute A(2) L. For row coordinates,

```text
M_paper = D M_JSON D^-1
v_paper = v_JSON D^-1
```

Apply the selected generator normalization before this change of coordinates.
The A(2) L map is `diag(beta^-1,1,1)`, from vertex counts `[1,0,0]` in its basis
diagrams. Ordinary $Y_2$ currently agrees with the accepted manuscript and
Macaulay2 in the same basis; no extra sign conjugation is required. Direct
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
relation (8.2). The [A(2) comparison report](audits/A2_SPECTRAL_COMPARISON.md) describes
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
