# Complete proposed public inventory

189 files. This is an explicit whitelist plus documented generated metadata and fresh verification evidence; no Git history or executables are included.

Proposed structure:

```text
data/                         exact mathematical payload (47 JSON files)
schema/                       six local JSON schemas
tools/                        structural validation and required helpers
audits/c/                     A(2) spectral and ordinary A(3) exact audits
audits/python/                A(2) spectral and generic YBE exact audits
benchmarks/flint_ybe/          independent C generic YBE verifier
reports/paper_audit/           required rational comparison fixtures/embeddings
examples/                     optional Sage importer
verification/                 fresh results, integrity and isolation evidence
*.md, *.json, CITATION.cff     public documentation, manifests, metadata drafts
LICENSE                       explicit draft; no grant yet
```

Selected historical assembly evidence is under audits/python/dilute_transcription;
no source-transcription executable or M2 input is included. Runtime evidence
under each audit is fresh candidate output. Details and reasons for every excluded
tracked research file are in EXCLUDED_FILES.json. Review this inventory before
Git initialisation. No publication action is authorised by this document.

| Proposed path | Treatment |
|---|---|
| `.gitignore` | generated candidate documentation/evidence |
| `.zenodo.json` | generated candidate documentation/evidence |
| `AUDIT_COVERAGE.md` | generated candidate documentation/evidence |
| `CITATION.cff` | generated candidate documentation/evidence |
| `CLEAN_CHECKOUT_REPORT.md` | generated candidate documentation/evidence |
| `DATASET_PROVENANCE.md` | generated candidate documentation/evidence |
| `DEPENDENCIES.json` | generated candidate documentation/evidence |
| `DEPENDENCY_AUDIT.md` | generated candidate documentation/evidence |
| `EXCLUDED_FILES.json` | generated candidate documentation/evidence |
| `FORMAT.md` | portable_documentation_excerpt |
| `LICENSE` | generated candidate documentation/evidence |
| `PUBLICATION_DECISIONS.md` | generated candidate documentation/evidence |
| `PUBLICATION_INVENTORY.md` | generated candidate documentation/evidence |
| `PUBLICATION_MANIFEST.json` | generated candidate documentation/evidence |
| `README.md` | generated candidate documentation/evidence |
| `audits/A2_SPECTRAL_COMPARISON.md` | copied_byte_for_byte |
| `audits/a2_spectral_comparison.json` | copied_byte_for_byte |
| `audits/a2_spectral_spec.json` | copied_byte_for_byte |
| `audits/c/a2_spectral/Makefile` | copied_byte_for_byte |
| `audits/c/a2_spectral/README.md` | copied_byte_for_byte |
| `audits/c/a2_spectral/REPORT.md` | copied_byte_for_byte |
| `audits/c/a2_spectral/exact.h` | copied_byte_for_byte |
| `audits/c/a2_spectral/verification_results/I.stdout.json` | generated candidate documentation/evidence |
| `audits/c/a2_spectral/verification_results/L.stdout.json` | generated candidate documentation/evidence |
| `audits/c/a2_spectral/verification_results/X2.stdout.json` | generated candidate documentation/evidence |
| `audits/c/a2_spectral/verification_results/Y2.stdout.json` | generated candidate documentation/evidence |
| `audits/c/a2_spectral/verification_results/Y2_star.stdout.json` | generated candidate documentation/evidence |
| `audits/c/a2_spectral/verification_results/crossing.stdout.json` | generated candidate documentation/evidence |
| `audits/c/a2_spectral/verification_results/results.json` | generated candidate documentation/evidence |
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
| `audits/python/a2_spectral/verification_results/I.stdout.json` | generated candidate documentation/evidence |
| `audits/python/a2_spectral/verification_results/L.stdout.json` | generated candidate documentation/evidence |
| `audits/python/a2_spectral/verification_results/X2.stdout.json` | generated candidate documentation/evidence |
| `audits/python/a2_spectral/verification_results/Y2.stdout.json` | generated candidate documentation/evidence |
| `audits/python/a2_spectral/verification_results/Y2_star.stdout.json` | generated candidate documentation/evidence |
| `audits/python/a2_spectral/verification_results/crossing.stdout.json` | generated candidate documentation/evidence |
| `audits/python/a2_spectral/verification_results/results.json` | generated candidate documentation/evidence |
| `audits/python/a2_spectral/verify.py` | copied_byte_for_byte |
| `audits/python/dilute_transcription/REPORT.md` | copied_byte_for_byte |
| `audits/python/dilute_transcription/correspondence.json` | copied_byte_for_byte |
| `audits/python/dilute_transcription/final_results.json` | copied_byte_for_byte |
| `audits/python/requirements.txt` | copied_byte_for_byte |
| `audits/python/run.py` | copied_byte_for_byte |
| `audits/python/spectral_ybe.py` | copied_byte_for_byte |
| `audits/run_a2_spectral.py` | copied_byte_for_byte |
| `benchmarks/flint_ybe/Makefile` | copied_byte_for_byte |
| `benchmarks/flint_ybe/results.json` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/runner.c` | copied_byte_for_byte |
| `benchmarks/flint_ybe/verification_results/rep_0.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_1.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_10.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_2.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_3.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_4.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_5.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_6.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_7.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_8.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/rep_9.jsonl` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/results.json` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verification_results/results.md` | generated candidate documentation/evidence |
| `benchmarks/flint_ybe/verifier.c` | copied_byte_for_byte |
| `data/a3.json` | copied_byte_for_byte |
| `data/basis_maps.json` | copied_byte_for_byte |
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
| `data/publication.json` | metadata_only_portability |
| `data/publication_provenance.json` | metadata_only_portability |
| `data/representations/A.json` | copied_byte_for_byte |
| `data/representations/C.json` | copied_byte_for_byte |
| `data/representations/C_star.json` | copied_byte_for_byte |
| `data/representations/I.json` | copied_byte_for_byte |
| `data/representations/L.json` | copied_byte_for_byte |
| `data/representations/X2.json` | copied_byte_for_byte |
| `data/representations/X3.json` | copied_byte_for_byte |
| `data/representations/Y2.json` | copied_byte_for_byte |
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
| `tools/a3_assertions.py` | copied_byte_for_byte |
| `tools/exact_a2.py` | copied_byte_for_byte |
| `tools/validate_data.py` | copied_byte_for_byte |
| `tools/validate_publication.py` | copied_byte_for_byte |
| `verification/a2_spectral.stdout.txt` | generated candidate documentation/evidence |
| `verification/build_a2.stdout.txt` | generated candidate documentation/evidence |
| `verification/build_ordinary.stdout.txt` | generated candidate documentation/evidence |
| `verification/build_ybe.stdout.txt` | generated candidate documentation/evidence |
| `verification/c_ybe.stdout.txt` | generated candidate documentation/evidence |
| `verification/isolation_incident.json` | generated candidate documentation/evidence |
| `verification/ordinary_a3.stdout.txt` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_A.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_C.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_C_star.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_I.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_L.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_X2.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_X3.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_Y2.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_Y2_star.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_Y3.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/rep_Y3_star.jsonl` | generated candidate documentation/evidence |
| `verification/ordinary_a3/results.json` | generated candidate documentation/evidence |
| `verification/ordinary_a3/results.md` | generated candidate documentation/evidence |
| `verification/preservation.json` | generated candidate documentation/evidence |
| `verification/python_ybe.stdout.txt` | generated candidate documentation/evidence |
| `verification/python_ybe/C_comparison_provenance.json` | generated candidate documentation/evidence |
| `verification/python_ybe/REPORT.md` | generated candidate documentation/evidence |
| `verification/python_ybe/comparison.json` | generated candidate documentation/evidence |
| `verification/python_ybe/provenance.json` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_0.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_1.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_10.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_2.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_3.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_4.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_5.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_6.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_7.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_8.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/rep_9.jsonl` | generated candidate documentation/evidence |
| `verification/python_ybe/results.json` | generated candidate documentation/evidence |
| `verification/sage_retry.json` | generated candidate documentation/evidence |
| `verification/sage_retry.stderr.txt` | generated candidate documentation/evidence |
| `verification/sage_retry.stdout.txt` | generated candidate documentation/evidence |
| `verification/structural.json` | generated candidate documentation/evidence |
| `verification/structural.stdout.txt` | generated candidate documentation/evidence |
| `verification/summary.json` | generated candidate documentation/evidence |
| `verify_release.py` | generated candidate documentation/evidence |
