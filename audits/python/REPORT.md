# Independent Python/FLINT spectral YBE audit

**All eleven representations PASS exact generic symbolic YBE, and all polynomial/rational comparisons PASS.** All 287 YBE residual entries and all 574 comparison residual entries are exactly zero. There are no unresolved representations in the corrected batch.

Python 3.10.12, python-flint 0.9.0, FLINT 3.6.0; one thread. The C evidence used FLINT package 2.8.4 (runtime version string 2.8.0), so the timings also reflect different library versions.

| Representation | Dim. | Python/C | Construct s | YBE s | Compare s | Python wall s | C wall s | Python peak MiB |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| X3 | 1 | PASS / PASS | 0.0280 | 0.0052 | 0.0012 | 0.0752 | 0.0305 | 23.91 |
| Y3 | 1 | PASS / PASS | 0.0204 | 0.0034 | 0.0022 | 0.0521 | 0.0306 | 22.78 |
| Y3_star | 1 | PASS / PASS | 0.0191 | 0.0037 | 0.0019 | 0.0575 | 0.0305 | 22.79 |
| C | 2 | PASS / PASS | 0.0308 | 0.0192 | 0.0033 | 0.1247 | 0.0611 | 23.79 |
| C_star | 2 | PASS / PASS | 0.0278 | 0.0223 | 0.0040 | 0.1233 | 0.0566 | 23.79 |
| A | 3 | PASS / PASS | 0.0478 | 0.0406 | 0.0069 | 0.2420 | 0.0863 | 25.66 |
| I | 5 | PASS / PASS | 0.0378 | 0.1943 | 0.1107 | 0.8779 | 0.2050 | 32.85 |
| Y2 | 6 | PASS / PASS | 0.0600 | 0.2545 | 0.1081 | 1.0067 | 0.2503 | 33.95 |
| Y2_star | 6 | PASS / PASS | 0.0619 | 0.2698 | 0.1092 | 1.0196 | 0.2540 | 34.14 |
| X2 | 7 | PASS / PASS | 0.0745 | 0.3749 | 0.1100 | 1.3369 | 0.3355 | 37.48 |
| L | 11 | PASS / PASS | 0.1444 | 1.5433 | 0.3139 | 4.4475 | 0.9598 | 68.65 |

The successful batch took **9.3686 seconds**. The initial metadata-error batch took **0.7294 seconds**; combined measured batch time was **10.0980 seconds**. Initial limit: 300 seconds; corrected retry limit: 299 seconds; every representation retained its 60-second ceiling. No timeout limit was extended.

The initial attempt recorded ERROR for all representations: JSON serialization rejected a FLINT integer Laurent exponent after construction/clearing. It never reached YBE. The traceback established a logging defect; the only mathematical-worker change was converting that metadata value to a Python int. Original logs and source hashes are retained in results/. The runner was additionally given a downward-only batch-limit option. No mathematical formula, normalization or expected result was changed.

The successful run uses sparse matrix dictionaries, rational-coefficient FLINT polynomials in degree-reverse-lex order, cross-cancelled fractions, the literal manuscript equation (8.3), and FLINT composition. This differs from the C expanded-formula construction and exponent substitution. C results were consulted only after the Python batches; no computed C matrices entered construction. Both implementations share the JSON specifications and the FLINT arithmetic library.

For L, exact YBE took about 1.54 seconds; the complete worker took 4.45 seconds. Construction took 0.14 seconds and rational comparison 0.31 seconds. Additional wall time is largely expression-size reporting: converting each 817,200-term triple product into Python dictionaries. This is reporting overhead, not an unresolved algebraic bottleneck. The 68.65 MiB peak includes those statistics. No optimization was needed to meet the limits.

The independently recorded clearing factors have m=4 in every case. Both sides carry D³u⁸v⁸; the nonzero D(p,q) and the entrywise clearing checks are recorded in results_verified/results.json. The exact factors and the separate manuscript normalization are explained in README.md. All matrix comparisons use the existing rational artifacts only after YBE. No specialization or probabilistic zero test is used.

Conditional scope: this establishes the complete generic YBE in the eleven supplied representations, with the documented normalization and embeddings. It does not independently prove diagrammatic conventions or the complete defining presentation. No manuscript discrepancy was found.

Files: spectral_ybe.py (independent mathematics), run.py (isolated runner and report generation), requirements.txt, authority.json, results/ (preserved first-attempt errors), results_verified/ (complete successful evidence and C comparison). README.md gives fresh-checkout commands.

All artifacts are in the research repository, under audits/python/. No manuscript, authoritative JSON, C verifier, historical audit evidence or Macaulay2 file was modified. Nothing was committed or published.
