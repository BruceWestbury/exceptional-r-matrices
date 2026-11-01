# Public inventory

233 files. The explicit source inventory and generated-file list are recorded in PUBLICATION_MANIFEST.json. Historical source hashes are preserved; current hashes describe this checkout.

```text
data/                         portable mathematical payload (47 JSON files)
schema/                       six local JSON schemas
macaulay2/                    package, auxiliary files, tests, and usage guide
tools/                        validation and optional exact package comparison
tests/                        comparison failure-detection tests
.github/workflows/            separate Macaulay2 verification job
audits/c/                     A(2) spectral and ordinary A(3) exact audits
audits/python/                A(2) spectral and generic YBE exact audits
benchmarks/flint_ybe/          independent C generic YBE verifier
reports/paper_audit/           rational comparison fixtures and embeddings
examples/                     optional Sage importer
verification/                 saved results and provenance
*.md, *.json, CITATION.cff     documentation and publication metadata
LICENSE                       CC BY 4.0 licence text
```

The Macaulay2 component is optional for JSON consumers and the C/Python audits. Its maintained source and every auxiliary file are included. The original mathematical assertions in the standalone package tests have been grouped for bounded execution; the main package has an installation fix for its coefficient exports.

Historical ordinary-to-dilute assembly evidence remains under audits/python/dilute_transcription/. The missing assembly program is not included. Excluded research files and their reasons are listed in EXCLUDED_FILES.json.

| Path | Treatment |
|---|---|
| `.github/workflows/macaulay2.yml` | generated documentation, integration tooling, or verification evidence |
| `.gitignore` | generated documentation, integration tooling, or verification evidence |
| `.zenodo.json` | generated documentation, integration tooling, or verification evidence |
| `AUDIT_COVERAGE.md` | generated documentation, integration tooling, or verification evidence |
| `CITATION.cff` | generated documentation, integration tooling, or verification evidence |
| `CLEAN_CHECKOUT_REPORT.md` | generated documentation, integration tooling, or verification evidence |
| `DATASET_PROVENANCE.md` | generated documentation, integration tooling, or verification evidence |
| `DEPENDENCIES.json` | generated documentation, integration tooling, or verification evidence |
| `DEPENDENCY_AUDIT.md` | generated documentation, integration tooling, or verification evidence |
| `EXCLUDED_FILES.json` | generated documentation, integration tooling, or verification evidence |
| `FORMAT.md` | updated_basis_convention_documentation |
| `LICENSE` | generated documentation, integration tooling, or verification evidence |
| `PUBLICATION_DECISIONS.md` | generated documentation, integration tooling, or verification evidence |
| `PUBLICATION_INVENTORY.md` | generated documentation, integration tooling, or verification evidence |
| `PUBLICATION_MANIFEST.json` | inventory and source/current integrity hashes |
| `README.md` | generated documentation, integration tooling, or verification evidence |
| `audits/A2_SPECTRAL_COMPARISON.md` | copied_byte_for_byte |
| `audits/a2_spectral_comparison.json` | copied_byte_for_byte |
| `audits/a2_spectral_spec.json` | copied_byte_for_byte |
| `audits/c/a2_spectral/Makefile` | copied_byte_for_byte |
| `audits/c/a2_spectral/README.md` | copied_byte_for_byte |
| `audits/c/a2_spectral/REPORT.md` | copied_byte_for_byte |
| `audits/c/a2_spectral/exact.h` | copied_byte_for_byte |
| `audits/c/a2_spectral/verification_results/I.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/c/a2_spectral/verification_results/L.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/c/a2_spectral/verification_results/X2.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/c/a2_spectral/verification_results/Y2.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/c/a2_spectral/verification_results/Y2_star.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/c/a2_spectral/verification_results/crossing.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/c/a2_spectral/verification_results/results.json` | generated documentation, integration tooling, or verification evidence |
| `audits/c/a2_spectral/verify.c` | copied_byte_for_byte |
| `audits/c/a3_relations/INVENTORY.md` | copied_byte_for_byte |
| `audits/c/a3_relations/Makefile` | copied_byte_for_byte |
| `audits/c/a3_relations/REPORT.md` | copied_byte_for_byte |
| `audits/c/a3_relations/json_reader.h` | copied_byte_for_byte |
| `audits/c/a3_relations/manifest.json` | copied_byte_for_byte |
| `audits/c/a3_relations/runner.c` | copied_byte_for_byte |
| `audits/c/a3_relations/verify.c` | copied_byte_for_byte |
| `audits/python/REPORT.md` | copied_byte_for_byte |
| `audits/python/a2_spectral/README.md` | copied_byte_for_byte |
| `audits/python/a2_spectral/REPORT.md` | copied_byte_for_byte |
| `audits/python/a2_spectral/requirements.txt` | copied_byte_for_byte |
| `audits/python/a2_spectral/verification_results/I.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/python/a2_spectral/verification_results/L.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/python/a2_spectral/verification_results/X2.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/python/a2_spectral/verification_results/Y2.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/python/a2_spectral/verification_results/Y2_star.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/python/a2_spectral/verification_results/crossing.stdout.json` | generated documentation, integration tooling, or verification evidence |
| `audits/python/a2_spectral/verification_results/results.json` | generated documentation, integration tooling, or verification evidence |
| `audits/python/a2_spectral/verify.py` | copied_byte_for_byte |
| `audits/python/dilute_transcription/REPORT.md` | historical_report_with_current_basis_note |
| `audits/python/dilute_transcription/correspondence.json` | copied_byte_for_byte |
| `audits/python/dilute_transcription/final_results.json` | copied_byte_for_byte |
| `audits/python/requirements.txt` | copied_byte_for_byte |
| `audits/python/run.py` | copied_byte_for_byte |
| `audits/python/spectral_ybe.py` | copied_byte_for_byte |
| `audits/run_a2_spectral.py` | copied_byte_for_byte |
| `benchmarks/flint_ybe/Makefile` | copied_byte_for_byte |
| `benchmarks/flint_ybe/results.json` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/runner.c` | copied_byte_for_byte |
| `benchmarks/flint_ybe/verification_results/rep_0.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_1.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_10.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_2.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_3.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_4.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_5.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_6.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_7.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_8.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/rep_9.jsonl` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/results.json` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verification_results/results.md` | generated documentation, integration tooling, or verification evidence |
| `benchmarks/flint_ybe/verifier.c` | copied_byte_for_byte |
| `data/a3.json` | copied_byte_for_byte |
| `data/basis_maps.json` | remove_obsolete_ordinary_Y2_map_2026_11_01 |
| `data/dilute_a2.json` | copied_byte_for_byte |
| `data/dilute_a2_representations/I.json` | copied_byte_for_byte |
| `data/dilute_a2_representations/L.json` | copied_byte_for_byte |
| `data/dilute_a2_representations/X2.json` | copied_byte_for_byte |
| `data/dilute_a2_representations/Y2.json` | copied_byte_for_byte |
| `data/dilute_a2_representations/Y2_star.json` | copied_byte_for_byte |
| `data/dilute_a3.json` | metadata_only_portability |
| `data/dilute_a3_embeddings.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_0.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_1.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_10.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_2.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_3.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_4.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_5.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_6.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_7.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_8.json` | copied_byte_for_byte |
| `data/dilute_representations/Dilute_9.json` | copied_byte_for_byte |
| `data/local_a2.json` | copied_byte_for_byte |
| `data/publication.json` | updated_publication_metadata_and_licensing |
| `data/publication_provenance.json` | updated_publication_metadata_and_licensing |
| `data/representations/A.json` | copied_byte_for_byte |
| `data/representations/C.json` | copied_byte_for_byte |
| `data/representations/C_star.json` | copied_byte_for_byte |
| `data/representations/I.json` | copied_byte_for_byte |
| `data/representations/L.json` | copied_byte_for_byte |
| `data/representations/X2.json` | copied_byte_for_byte |
| `data/representations/X3.json` | copied_byte_for_byte |
| `data/representations/Y2.json` | author_requested_basis_conjugation_2026_11_01 |
| `data/representations/Y2_star.json` | copied_byte_for_byte |
| `data/representations/Y3.json` | copied_byte_for_byte |
| `data/representations/Y3_star.json` | copied_byte_for_byte |
| `data/spectral/Dilute_0.json` | copied_byte_for_byte |
| `data/spectral/Dilute_1.json` | copied_byte_for_byte |
| `data/spectral/Dilute_10.json` | copied_byte_for_byte |
| `data/spectral/Dilute_2.json` | copied_byte_for_byte |
| `data/spectral/Dilute_3.json` | copied_byte_for_byte |
| `data/spectral/Dilute_4.json` | copied_byte_for_byte |
| `data/spectral/Dilute_5.json` | copied_byte_for_byte |
| `data/spectral/Dilute_6.json` | copied_byte_for_byte |
| `data/spectral/Dilute_7.json` | copied_byte_for_byte |
| `data/spectral/Dilute_8.json` | copied_byte_for_byte |
| `data/spectral/Dilute_9.json` | copied_byte_for_byte |
| `data/spectral_r.json` | copied_byte_for_byte |
| `examples/README.md` | copied_byte_for_byte |
| `examples/import_spectral.py` | copied_byte_for_byte |
| `macaulay2/ExceptionalDiagrams.m2` | coefficient_export_symbols_fixed_for_installation |
| `macaulay2/ExceptionalDiagrams/GB3.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/Rmat.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/basis33.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/cf.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/cfprime.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/decompositions3dilute.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem2.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_0.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_1.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_10.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_2.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_3.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_4.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_5.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_6.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_7.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_8.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/idem3_9.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps2.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps2dilute.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_0.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_1.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_10.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_2.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_3.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_4.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_5.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_6.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_7.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_8.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3_9.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3dilute_0.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3dilute_1.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3dilute_2.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3dilute_3.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/reps3dilute_4.m2` | author_authorized_package_import_unchanged |
| `macaulay2/ExceptionalDiagrams/trim.m2` | author_authorized_package_import_unchanged |
| `macaulay2/README.md` | generated documentation, integration tooling, or verification evidence |
| `macaulay2/tests/exceptional-diagrams.m2` | original_test_assertions_with_bounded_group_selection |
| `reports/paper_audit/local_embeddings.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_0.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_1.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_10.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_2.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_3.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_4.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_5.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_6.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_7.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_8.json` | copied_byte_for_byte |
| `reports/paper_audit/spectral_9.json` | copied_byte_for_byte |
| `schema/a3.schema.json` | copied_byte_for_byte |
| `schema/dilute_representation.schema.json` | copied_byte_for_byte |
| `schema/local_a2.schema.json` | copied_byte_for_byte |
| `schema/portable_matrices.schema.json` | copied_byte_for_byte |
| `schema/publication.schema.json` | copied_byte_for_byte |
| `schema/representation.schema.json` | copied_byte_for_byte |
| `tests/test_macaulay2_checker.py` | generated documentation, integration tooling, or verification evidence |
| `tools/a3_assertions.py` | copied_byte_for_byte |
| `tools/check_macaulay2_data.py` | generated documentation, integration tooling, or verification evidence |
| `tools/exact_a2.py` | copied_byte_for_byte |
| `tools/validate_data.py` | copied_byte_for_byte |
| `tools/validate_publication.py` | copied_byte_for_byte |
| `verification/a2_spectral.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/build_a2.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/build_ordinary.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/build_ybe.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/c_ybe.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/isolation_incident.json` | generated documentation, integration tooling, or verification evidence |
| `verification/macaulay2.json` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_A.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_C.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_C_star.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_I.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_L.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_X2.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_X3.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_Y2.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_Y2_star.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_Y3.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/rep_Y3_star.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/results.json` | generated documentation, integration tooling, or verification evidence |
| `verification/ordinary_a3/results.md` | generated documentation, integration tooling, or verification evidence |
| `verification/preservation.json` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/C_comparison_provenance.json` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/REPORT.md` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/comparison.json` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/provenance.json` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_0.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_1.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_10.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_2.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_3.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_4.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_5.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_6.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_7.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_8.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/rep_9.jsonl` | generated documentation, integration tooling, or verification evidence |
| `verification/python_ybe/results.json` | generated documentation, integration tooling, or verification evidence |
| `verification/sage_retry.json` | generated documentation, integration tooling, or verification evidence |
| `verification/sage_retry.stderr.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/sage_retry.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/structural.json` | generated documentation, integration tooling, or verification evidence |
| `verification/structural.stdout.txt` | generated documentation, integration tooling, or verification evidence |
| `verification/summary.json` | generated documentation, integration tooling, or verification evidence |
| `verify_release.py` | generated documentation, integration tooling, or verification evidence |
