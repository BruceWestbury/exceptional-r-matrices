# Repository guide

| Location | Contents |
|---|---|
| [data/](data/) | 47 JSON files containing matrices, scalars, embeddings, normalizations and the catalogue |
| [schema/](schema/) | Six JSON schemas for validation |
| [macaulay2/](macaulay2/README.md) | ExceptionalDiagrams, 37 auxiliary files, standalone tests and usage instructions |
| [tools/](tools/) | Structural validation, exact arithmetic helpers and package/data comparison |
| [tests/](tests/) | Tests of comparison failure detection |
| [audits/c/a3_relations/](audits/c/a3_relations/REPORT.md) | Ordinary A(3) relation manifest, C verifier and report |
| [audits/c/a2_spectral/](audits/c/a2_spectral/README.md) | C/FLINT unitarity and crossing checks |
| [audits/python/a2_spectral/](audits/python/a2_spectral/README.md) | Python/FLINT unitarity and crossing checks |
| [audits/python/](audits/python/REPORT.md) | Python/FLINT generic Yang–Baxter verifier and report |
| [audits/python/dilute_transcription/](audits/python/dilute_transcription/REPORT.md) | Saved ordinary-to-dilute construction evidence and occupancy correspondence |
| [benchmarks/flint_ybe/](benchmarks/flint_ybe/) | C/FLINT generic Yang–Baxter verifier and results |
| [reports/paper_audit/](reports/paper_audit/) | Exact rational comparison matrices and local embeddings |
| [examples/](examples/README.md) | SageMath import and unitarity example |
| [verification/](verification/) | Saved verification results, logs and input hashes |
| [.github/workflows/](.github/workflows/) | Automated package and data checks |

## Documentation

[README.md](README.md) provides the starting commands.
[FORMAT.md](FORMAT.md) specifies the data and mathematical conventions.
[DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md) lists software requirements and execution
order. [AUDIT_COVERAGE.md](AUDIT_COVERAGE.md) describes what each check establishes,
and [CLEAN_CHECKOUT_REPORT.md](CLEAN_CHECKOUT_REPORT.md) summarizes recorded results.

The [data and verification guide](DATASET_PROVENANCE.md) explains the relationship
between the package and JSON data. The
[maintenance guide](PUBLICATION_DECISIONS.md) describes how to update them together.

[CITATION.cff](CITATION.cff) supplies citation metadata, and [LICENSE](LICENSE)
contains the CC BY 4.0 terms. [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json)
records the detailed inventory and integrity hashes.
