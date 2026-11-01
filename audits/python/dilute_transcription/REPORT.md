# Ordinary-to-dilute construction evidence

The saved reconstruction check establishes **298 complete generator matrices**
and **32 partial matrices** among the 330 dilute A(3) generators. All 8,518
reconstructed entries have exact zero residuals. A complete independent
construction additionally requires **92 transition-block entries**.

The [recorded results](final_results.json) also give exact agreement for all
330 matrices with the package's raw matrices, twenty displayed-table comparisons,
and 682 normalization checks. The [package comparison tool](../../../macaulay2/README.md#verification)
provides a runnable check of agreement with the bundled ExceptionalDiagrams.

| Representation | Dimension | Complete matrices | Partial matrices | Entries requiring construction |
|---|---:|---:|---:|---:|
| I | 5 | 22 | 8 | 8 |
| L | 11 | 18 | 12 | 44 |
| X2 | 7 | 26 | 4 | 16 |
| Y2 | 6 | 26 | 4 | 12 |
| Y2_star | 6 | 26 | 4 | 12 |
| X3 | 1 | 30 | 0 | 0 |
| Y3 | 1 | 30 | 0 | 0 |
| Y3_star | 1 | 30 | 0 | 0 |
| A | 3 | 30 | 0 | 0 |
| C | 2 | 30 | 0 | 0 |
| C_star | 2 | 30 | 0 | 0 |

## Occupancy construction

A dilute representation decomposes by source and target occupancy. Full
occupancy comes first, followed by the two-occupancy sectors 12,02,01 using
zero-based labels. L then has single occupancies 2,1,0, and I ends with empty
occupancy. Thus the dimensions are I=1+3+1, L=5+3+3, X2=4+3, and Y2=Y2_star=3+3.
The six top representations retain their ordinary dimensions.

Each generator graph selects its active occupancy block, and the other blocks
are zero. Endomorphism and identity blocks are reconstructed from ordinary H1/H2,
the A(2) character table, one-dimensional A(1)/A(0) identities, and identity
transport between equal occupancy spaces. Normalization factors follow from
vertex counts and the package formulas.

The [basis registry](../../../data/basis_maps.json) gives the conventions for
using the repository data. Ordinary Y2 and the package share a basis. Selected
I and L comparisons with the paper's displayed tables use the specified diagonal
maps after generator normalization. The saved reconstruction counts include
alignment of the ordinary and dilute bases.

## Transition blocks requiring construction

| Representation | Generators |
|---|---|
| I | G10, G14, G17, G19, G21, G24, G25, G28 |
| L | G0, G4, G7, G8, G10, G11, G14, G16, G25, G27, G28, G29 |
| X2 | G10, G14, G25, G28 |
| Y2 | G10, G14, G25, G28 |
| Y2_star | G10, G14, G25, G28 |

These blocks involve ordinary maps between different occupancy counts: cup and
cap maps between A(0)/A(2) or A(1)/A(3), trivalent A(1)/A(2) maps, and rectangular
A(2)/A(3) maps. Completing their construction requires explicit Hom(a,b) matrices
in compatible multiplicity bases, including relative cup, cap and trivalent
normalizations. The result records list the relevant coordinates for each block.

Package agreement, displayed-table comparisons and exact spectral identities
provide complementary checks of the stored values. The independent construction
coverage is precisely the 298 complete and 32 partial matrices tabulated above.
