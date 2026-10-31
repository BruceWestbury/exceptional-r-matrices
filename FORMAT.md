# Portable dataset format 0.3.0

This additive profile preserves every existing 0.2.0 data file and schema.
`data/publication.json` is the entry point. Its entries identify each payload's
path, schema and role. The retained status/provenance text is historical; the
catalogue and linked verification reports give current coverage. A valid file
is not thereby author-approved or a proof of an abstract algebra presentation.

## Payload and conventions

| Path | Contents | Normalisation |
|---|---|---|
| `data/local_a2.json` | Ordinary A(2) coefficients, tables and five characters | alpha=1 |
| `data/a3.json`, `data/representations/` | Ordinary A(3) specification and 110 matrices | alpha=1 |
| `data/dilute_a3.json`, `data/dilute_representations/` | Registry and 330 dilute A(3) matrices | raw auxiliary source |
| `data/dilute_a2.json`, `data/dilute_a2_representations/` | Five irreducibles, 16 diagram matrices each | raw auxiliary source |
| `data/spectral_r.json` | Polynomial spectral expansion, scalar, crossing and endpoints | manuscript Rpoly |
| `data/dilute_a3_embeddings.json` | Local diagram embeddings and generator correspondence | apply paper2 first |
| `data/spectral/` | Both Rpoly positions in all eleven representations | manuscript Rpoly |
| `data/basis_maps.json` | Explicit conjugations and occupancy/basis order | direction stated per map |
| `data/publication_provenance.json` | Source hashes, payload hashes and base commit | metadata |

All indices are zero-based. A sparse matrix is an object with `operator`, `rows`,
`cols`, and row-major `entries: [[row, column, scalar], ...]`. Omitted entries
are zero; `entries: []` is a zero matrix, not missing data. Coordinates preserve
the source ordering, without transposition. Vectors act on the **right as rows**;
a word `[A,B,C]` means the product ABC in that order. Neutral coordinate labels
are identifiers: legacy labels beginning at 1 do not change zero-based indices.

Ordinary and dilute representations with the same label can have different
dimensions. The dilute A(3) index order is I,L,X2,Y2,Y2_star,X3,Y3,Y3_star,A,C,C_star.
Occupancy sectors in `basis_maps.json` are copied from the committed construction
audit. They do not supply the 92 unresolved transition-block entries. Ordinary
A(1) and A(0) sectors are one-dimensional identity spaces; A(2) sectors refer to
the character table. Full-occupancy A(3) sectors refer to ordinary matrix files.

## Exact scalar grammar and references

The field is QQ(p,q), or QQ(p,q,u) for spectral files; variables are algebraically
independent. Strings use integers, identifiers, parentheses, unary minus,
`+ - * /` and `^` with a signed integer literal exponent. There are no decimal
floats, implicit products, function calls or arbitrary executable expressions.
For example `(p^2*q^-1-p^-2*q)/(q-q^-1)` is exact. Powers bind before unary minus;
products/divisions and sums/subtractions associate left to right.

Resolve named aliases recursively, without cycles. Ordinary matrices import
`local_a2.json` and `a3.json` coefficients. Raw dilute matrices contain p,q only.
New matrix files declare their field and local `coefficient_definitions`.
An expression `(numerator)/spectral_denominator` is the **actual matrix entry**;
the denominator is a shared storage alias, not a new spectral normalization.
It can include a Laurent-clearing monomial in u. Expand aliases to obtain entries
in the stated fraction field; do not multiply the matrices by the alias again.

Runtime `*_ref` paths in new data are relative to the containing JSON file;
`field_ref: F` in legacy files is a field identifier, not a path. Catalogue paths
and evidence paths are relative to the repository root. Source filenames and
historical absolute paths in provenance are citations only. They need not exist
on a consumer's machine. No import command reads them.

## Dilute A(2), embeddings and normalisation

D0,...,D15 follow the package's `lst2` order; their graphs and source indices
are stored in `dilute_a2.json`. D4 is the composite D3*D3. The other graphs use
left boundary 0,1 and reversed right boundary 3,2; internal vertices start at 4.
I has dimension 2 (full,empty); L has dimension 3 (full,{1},{0}); the other three
representations have dimension 1 (full). I,L are literal copies of `reps2dilute.m2`.
X2,Y2,Y2_star take D0–D4 from ordinary `reps2.m2`; partial diagrams D5–D15 vanish
by the package's top-quotient dispatch. These source files are provenance only.

To evaluate local generator formulas, multiply each raw diagram matrix by its
registry `paper2_multiplier`. The registry also supplies `paper_multiplier` for
the distinct alpha convention; these factors are alternatives, not sequential
rescalings. Embeddings are sums of ordered words in the normalized G matrices.
D4 is subsequently D3*D3. `generator_expressions` then expresses the spectral
operators in these local diagrams. In particular the ordinary braid supported
on full occupancy differs from the dilute braid by D6+D7+D15.

Displayed-table comparison may additionally require a diagonal basis map.
`basis_maps.json` records I,L (dilute A3) and the source-derived A2:L map.
Ordinary Y2 already uses the manuscript and Macaulay2 basis; no sign conjugation
is needed. With row coordinates, the stated map M_paper = D M_JSON D^-1 means
row coordinates transform as v_paper = v_JSON D^-1. Apply any required generator
normalisation first. The A2:L map diag(beta^-1,1,1) comes from vertex counts
[1,0,0] in its basis diagrams, and was checked against the tables; it was not
fitted to the matrices. Before-map residuals remain in the export evidence.

## Polynomial spectral object

For p=q^n and u=q^x as bracket notation only,
`[an+bx+c]=(p^a*u^b*q^c-p^-a*u^-b*q^-c)/(q-q^-1)`.
The variables remain independent. The JSON records exactly

Rpoly(u) = ([6n]^2[n]/([3n]^2[2n])) [n+x+1][x-1][2n+x][3n+x] Rcheck(u).

The source is accepted `yangbaxter.tex`, equation (8.3), lines 134–148, and the
polynomial definition at lines 798–800. The nine-term expansion is algebraically
expanded from these formulas. No arbitrary common denominator replaces this
normalisation. The coefficients and matrices are Laurent in u with rational
p,q coefficients. Thus 0 and infinity are **rescaled limits**, not direct finite
substitutions. The JSON specifies u^4 Rpoly at 0, u^-4 Rpoly at infinity, and
ordinary substitution at u=1, including every scalar factor.

Crossing is Rot(Rpoly(u))=Rpoly(p^-3*u^-1), with supplied linear diagram rotation
pairs (I,U), (S_ordinary,Sinv_ordinary), (K,H), (E,D_squared), and fixed T,D,O.
Split `one=I+D_squared+O`, `S_dilute=S_ordinary+D+O`, and `B=D+D_squared`
before applying rotation. Rotation is not matrix transpose, an algebra
homomorphism, or merely interchange of the dilute braid and its inverse.
The diagrammatic convention itself is not re-proved here.

## Validation, import and evidence

```sh
python3 tools/validate_publication.py --self-test
```

This offline command needs Python >=3.10 and jsonschema >=3.2. It checks all
catalogue JSON against local draft-07 schemas, dimensions, sparse ordering and
indices, expression grammar and alias dependencies, cross-file references,
bases, normalisations, spectral positions, occupancy coordinates and payload
hashes. Negative tests cover malformed indices, duplicate entries, names,
dimensions, basis, positions, references, cycles and code-like expressions.
It does **not** simplify scalars, certify nonzero denominators or check identities.
Legacy validators and audits are unchanged; the original validator is not the
entry point for this larger dataset.

The bounded export comparisons in `reports/dataset_release/export/` are separate
exact mathematical evidence. They compare all 22 spectral matrices both to the
rational artifacts times the manuscript scalar and to reconstruction from JSON
formula/embeddings/raw generators, and check serialization. A(2) source copies,
ordinary full-corner characters and displayed tables are also compared exactly.
The exporter reuses tested Python/FLINT arithmetic, not a new independent backend.
Independent generic YBE evidence remains in the C and Python audit directories.

See `examples/import_spectral.py` for exact Sage import; Sage is optional.
The payload, schemas and core validator have no manuscript or Macaulay2 runtime
dependency. The optional bundled package and its exact comparison runner are
documented in `macaulay2/README.md`. That runner evaluates the actual package
against the JSON, applying the registry's normalization factors and the spectral
prefactor. Both use the same source coordinates; the remaining manuscript basis
maps are not applied again. Research-only regeneration tools and the historical
profile remain excluded.
