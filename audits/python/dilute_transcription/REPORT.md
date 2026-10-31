# Ordinary-to-dilute A(3) transcription audit

**The construction is only partially independently verified.** With the documented Y2 basis map, **298 of 330 generator matrices are completely reconstructed entrywise** from ordinary data and occupancy rules. **32 matrices are only partially verified**, with **92 active-block entries not independently reconstructed**. Their surrounding forced-zero blocks pass. All 8,518 reconstructed entries have exact zero residual. No matrix is wholly unassessed, but that does not make the 32 active blocks reconstructed.

Separately, **all 330 matrices match the retained raw Macaulay2 source files**, and **all 20 displayed manuscript S1,T1,B1,E1 tables pass** in the recorded normalizations/bases. Neither result supplies the missing independent construction of the 92 entries.

| Representation | Dilute dimension | Completely verified | Partially verified | Unknown entries | Wall s | Peak MiB |
|---|---:|---:|---:|---:|---:|---:|
| I | 5 | 22 | 8 | 8 | 0.1404 | 22.06 |
| L | 11 | 18 | 12 | 44 | 0.4107 | 22.80 |
| X2 | 7 | 26 | 4 | 16 | 0.2362 | 22.66 |
| Y2 | 6 | 26 | 4 | 12 | 0.1921 | 22.53 |
| Y2_star | 6 | 26 | 4 | 12 | 0.1903 | 22.41 |
| X3 | 1 | 30 | 0 | 0 | 0.0338 | 19.82 |
| Y3 | 1 | 30 | 0 | 0 | 0.0439 | 21.00 |
| Y3_star | 1 | 30 | 0 | 0 | 0.0373 | 21.21 |
| A | 3 | 30 | 0 | 0 | 0.0626 | 21.68 |
| C | 2 | 30 | 0 | 0 | 0.0687 | 21.46 |
| C_star | 2 | 30 | 0 | 0 | 0.0525 | 21.53 |

The initial batch and Y2-only follow-up used **1.6726 seconds** in total. The initial batch had a 300-second ceiling, each representation a 60-second hard limit, and the follow-up a 60-second total ceiling. No timed-out calculation was retried or extended. These runs stayed below the existing cumulative 300-second allowance. Python-flint 0.9.0 / FLINT 3.6.0, one thread; all comparisons are over Q(p,q).

## Construction established from the sources

The dilute category is a direct sum over source and target occupancy patterns, not just a direct sum of ordinary diagonal blocks (`dilute.tex:16–33,52–54`). The retained package loads precomputed files (`ExceptionalDiagrams.m2:866–876`) and routes the six top representations through the ordinary files, killing partial diagrams (`repTop`, `repData`, `repBasis`, lines 898–919). It does not contain the generating assembly program: its reference to `diagrams-rep.m2` could not be resolved in the repository or the inspected parent tree.

The manuscript and diagram vacancy marks specify occupancy order. Full occupancy comes first; the two-occupancy sectors are 12,02,01 (zero-based labels); L then has single occupancies 2,1,0; I ends with empty occupancy. This gives dimensions I=1+3+1, L=5+3+3, X2=4+3, Y2=3+3, Y2_star=3+3. The six top representations retain their ordinary dimensions. Each coordinate and its ordinary space is recorded explicitly in correspondence.json. Full-occupancy alignment is tested against ordinary H1/H2, rather than inferred from dilute entries.

The graph declarations identify each generator's one potentially active occupancy block. Every other block must vanish. Endomorphism/identity blocks can be reconstructed from ordinary H1/H2, the A(2) character table, A(1)/A(0) identities, or identity transport between identical occupancy copies. All recorded multipliers are checked independently from graph vertex counts and package formulas: **682 normalization comparisons pass**. Structural dimensions, neutral coordinate labels and occupancy support pass.

## Exact discrepancy and its resolution

The initial identity-coordinate assumption for **Y2** failed at four raw entries:

- G3 (ordinary H1), coordinates (1,0) and (2,1).
- G9 (ordinary H2), coordinates (0,1) and (1,2).

The stored entry is the negative of the untransformed expected entry in each case. The full expected/stored fractions and exact residuals, with occupancy and normalization, are retained in initial_basis_mismatches.json and results/rep_3.jsonl. For example, at G3(1,0), stored minus expected is

`-2*q*(p^14+p^10-p^8+p^6-p^4-1)/(p^8*q^2-p^6)`.

This is a **coordinate-convention discrepancy**, not an established erroneous dilute entry: the stored matrices agree with Paul's raw source and with the accepted displayed tables. The prior audit `reports/paper_audit/a2_results_ordinarygauge_3.json` already records `D=diag(1,-1,1)` between ordinary JSON and manuscript coordinates. Applying that fixed map only to the full-occupancy ordinary input resolves all four residuals exactly in the follow-up. The final manifest names the map and its provenance. No transformation was fitted and no authoritative entry, formula or normalization was changed.

## Unresolved morphism blocks

- **I**: G10, G14, G17, G19, G21, G24, G25, G28.
- **L**: G0, G4, G7, G8, G10, G11, G14, G16, G25, G27, G28, G29.
- **X2**: G10, G14, G25, G28.
- **Y2**: G10, G14, G25, G28.
- **Y2_star**: G10, G14, G25, G28.

These are ordinary maps between different occupancy counts: cup/cap maps involving A0/A2 or A1/A3, trivalent A1/A2 maps, and rectangular A2/A3 maps. The ordinary JSON files store endomorphisms, not these maps in compatible multiplicity bases. Products and endomorphism identities do not by themselves fix their individual scalings. The audit therefore marks the entire potential active block unknown; it does not use its stored dilute values to manufacture expectations, nor solve a change of basis to force agreement.

To complete the audit, supply the missing assembly source or an explicit ordinary Hom(a,b) matrix specification in the recorded bases, including relative cup/cap and trivalent-vertex normalization. `unresolved_blocks.json` lists the precise representation, generator, source/target occupancy, row/column coordinates and required source. The absence of a reconstruction is not evidence that an entry is wrong.

## Manuscript and raw-source comparisons

The 20 literal tables come from `yangbaxter.tex:560–793`, with exact per-table locations and TeX cells retained in correspondence.json. They test combinations S1,T1,B1,E1 of the stored G matrices in paper2 normalization. Position-2 rotation conventions and spectral identities are not re-audited.

I and L table comparisons require the previously recorded common diagonal gauges. Their computational provenance is explicit; they are not newly fitted and do not resolve unknown block morphisms. The ordinary Y2 map is kept distinct from these dilute table gauges. Passing these combinations does not isolate every individual unresolved block entry.

Raw-source comparison uses independent literal parsing of the retained `.m2` files, without executing Macaulay2. The top mapping is derived from graph identity, not taken on trust from the stored matrix values. All source-fidelity residuals vanish. This verifies the transcription of Paul's precomputed data, not the correctness of the missing program that assembled it.

## Outcome and provenance

Final independent reconstruction: 298 complete matrices, 32 partial, no remaining nonzero residual among reconstructed entries. Initial diagnostics: four exact basis mismatches, resolved using an existing documented map and preserved verbatim. Missing construction information: 32 transition blocks / 92 entries. Consequently **complete ordinary-to-dilute transcription verification has not been established**.

Results, source hashes, basis conventions, the initial and final manifests, the bounded follow-up and exact diagnostics reside under audits/python/dilute_transcription/. No result exists only in an external scratch workspace. Existing data, manuscript, Macaulay2 files, previous audits and evidence are unchanged. Nothing was committed or published.
