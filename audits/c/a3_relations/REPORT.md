# Independent C/FLINT ordinary A(3) relation audit

**All 1,605 applicable encoded relation checks PASS exactly in all eleven ordinary representations.** There are no nonzero residuals, C errors or timeouts. Forty-five checks are NOT APPLICABLE because they belong to the top quotient. The unprinted degree-seven braid-generator relation remains unresolved and was not evaluated.

The batch took **2.406868 seconds**, with hard limits of 60 seconds per representation and 300 seconds per batch. No limit was extended and no mathematical calculation was repeated. Compilation took 0.52 seconds separately. The largest ordinary representation is L, dimension **5** (not dilute L of dimension 11).

| Representation | Dimension | PASS | Not applicable | Wall s | Peak MiB |
|---|---:|---:|---:|---:|---:|
| I | 1 | 141 | 9 | 0.0761 | 8.38 |
| X3 | 1 | 150 | 0 | 0.0508 | 8.82 |
| Y3 | 1 | 150 | 0 | 0.0767 | 8.45 |
| Y3_star | 1 | 150 | 0 | 0.0763 | 8.68 |
| C | 2 | 150 | 0 | 0.1269 | 8.85 |
| C_star | 2 | 150 | 0 | 0.1374 | 8.86 |
| A | 3 | 150 | 0 | 0.1931 | 8.99 |
| Y2 | 3 | 141 | 9 | 0.2650 | 9.07 |
| Y2_star | 3 | 141 | 9 | 0.2693 | 9.25 |
| X2 | 4 | 141 | 9 | 0.3872 | 9.59 |
| L | 5 | 141 | 9 | 0.7465 | 10.67 |

GCC 11.4.0, `-O2 -std=c11 -Wall -Wextra`; one FLINT thread; installed FLINT package 2.8.4-2build1 (header/runtime strings 2.8.0). Exact fractions of rational-coefficient multivariate polynomials were used throughout. Peak RSS includes the word cache. No performance obstruction was encountered.

## 1. Relations verified exactly

The 150-item manifest contains repeated checks in different logical roles; it does not assert 150 independent defining equations. Every record gives the ordered words, exact coefficient strings, applicable representation names, ordinary alpha=1 normalization and source. Local aliases are expanded explicitly. See INVENTORY.md for the per-identifier listing.

The **30 displayed H,K,U defining equalities** are all covered:

- At each position: HK=tau K, KH=tau K, HU=phi U, UH=phi U, K²=phi K, KU=0, UK=0, U²=delta U, and the cubic for H: 18 equalities in total.
- H1 K2 H1 = H2 K1 H2, and the five mixed patterns K_i U_j K_i, K_i U_j H_i, K_i U_j U_i, U_i U_j K_i, U_i U_j U_i for both i=1,2: 11 equalities.
- The full quartic (6.39): one equality, with the current c1,c15 and positive derived b3 contribution as printed, without historical coefficient overrides.

These match the explicit list in **Definition 6.9, (6.27)–(6.39), threestring.tex:189–242**. The b coefficients agree in form with the alternative eigenvalue definitions at appendix.tex:82–92; the c expressions and c0 closure are copied from the current specification and compared with appendix.tex:118–164 during review. No values were solved from the matrices.

Additional checks include both local A(2) multiplication tables (68 cells across positions), all 13 local relation templates at each position (26), and the K/U Lagrange prescriptions at each position (four). The latter are consequences, not additional axioms: threestring.tex:248–261. The H quintics are likewise consequences.

The ordinary S/Sinv polynomial prescriptions, inverses, braid relation and S quintics are checked, including duplicate local checks where applicable. Current manuscript anchors are (6.48), threestring.tex:651–657, and (6.49)–(6.50), lines 663–667; local cubic (5.34) is at twostring.tex:615–619. Some copied JSON line references predate inserted manuscript text; stable equation labels and these current anchors govern the comparison.

The original JSON matrices are the inputs. Loading all ten generators and verifying their prescriptions avoids silently replacing a stored generator by a computed one that might hide a disagreement. Every applicable residual matrix was inspected entrywise, not merely on its diagonal.

## 2. Python checks not repeated in C

Stored Python evidence was read **after** the C batch. The eleven full-quartic records and thirty applicable top-quotient records agree directly, giving 41 per-relation stored comparisons. The remaining comparison uses the Python report's category totals and empty acceptance-failure lists, together with inspection of the Python evaluator's coverage. No unavailable per-check transcript is invented and no Python mathematical calculation was rerun.

The C audit covers all current matrix identities in the declarative local relations, polynomial prescriptions, formal A(3) relations and local tables. It does **not** repeat these additional Python checks:

- Separate cubic-reduced versions of the 25 completed local-table cells at each position.
- Factored-versus-expanded H/S quintic and top-cubic checks.
- Bar/rotation construction checks, prescribed-zero assertions outside the four top-quotient zero generators, and independent printed-matrix source witnesses.
- Triangularity, local-character matching, braid diagonals, Bratteli restrictions and exact specialization certificates for generic absolute irreducibility.
- Local scalar/bar identities, character-based coefficient determination, character-basis rank, historical coefficient/residual regression checks, and free-word quotient-source comparisons.

These are auxiliary or identification checks, not missing equalities from the displayed six-generator definition. Source scripts inspected: exact_a2.py, exact_a3.py, a3_assertions.py, audit_a3.py and audit_representations.py. Their implementations and evidence remain unchanged. Python-only evidence is retained in reports/a3_representations.md, reports/a3_relations.md and reports/a3_representation_residuals.json.

## 3. Manuscript claims not encoded

**The degree-seven braid relation remains unavailable.** The accepted manuscript states at threestring.tex:722–729 that braid plus quintic gives a 600-dimensional algebra and requires an additional degree-seven relation, which is too complicated to print. No explicit words or coefficients occur in that passage, the existing JSON unavailable_assertions entry, or the inspected evaluators. None was guessed or reconstructed.

The manifest retains this item with null words and coefficients. The complete result grid contains eleven ERROR/UNRESOLVED encoding records with `evaluated: false` and null residuals. These do not represent nonzero mathematical residuals or failed C computations. Raw C logs contain only encoded checks; the reporting layer makes the omitted item explicit.

**Completeness statement:** the manifest covers every displayed equality of the accepted paper's localized six-generator H,K,U presentation (Definition 6.9), and these all vanish in the eleven supplied representations. It is **not** a complete braid-only S1,S2 presentation audit because the degree-seven relation is unavailable. Nor is checking representations a new proof that the displayed relations give precisely the intended algebra, that the representations are faithful as a collection, or that every diagrammatic identity over the coefficient ring follows. The original five-boundary square-pentagon diagram identity, bimodule presentations and basis/rank arguments are not independently reverified here. There is no further missing displayed H,K,U equation identified in this inventory.

## 4. Quotient applicability

Top quotient checks apply only to **X3, Y3, Y3_star, C, C_star and A**. The four exact zero checks K1=K2=U1=U2=0 pass in these representations, independently confirming the manifest's declared applicability.

The two top cubics and three top quartics are the displayed quotient presentation (6.4)–(6.7), threestring-top.tex:50–99, included by threestring.tex:138. These five relations plus the four zero checks are marked NOT APPLICABLE on **I, L, X2, Y2 and Y2_star**: 45 scope exclusions. They are not failed full-algebra relations. No quotient equation was substituted for the full quartic.

## Reproducibility and provenance

README.md gives the C-only build/run commands. manifest.json is the mathematical input to the evaluator; it is not an unrelated list copied only into the report. verify.c implements a separate FLINT rational-function parser/evaluator and ordered-word cache. Only JSON reading and resource-launch code were reused/adapted from the spectral benchmark; none of its spectral calculations or computed intermediates was copied.

Raw per-relation C logs retain exact residuals (empty lists for zero), execution time and source. Peak memory at each relation is the cumulative process high-water mark, not an isolated per-relation allocation. Results and the post-run Python evidence comparison are machine-readable under results/. The optional summarize.py performs JSON reporting only, never mathematical evaluation.

All files are in the research repository under audits/c/a3_relations/. Source and input hashes and the base Git commit are in source_provenance.json. No results exist only in an external scratch workspace. No manuscript, authoritative JSON, existing audit, historical evidence, spectral verifier or Macaulay2 file was altered. No commit or publication was made.
