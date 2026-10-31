# Dependency audit

No selected mathematical worker requires Macaulay2, the external manuscript,
private assembly sources or Git objects. Original mathematical code is copied
unchanged; metadata-only transformations are recorded in PUBLICATION_MANIFEST.json.

| Public entry point | Repository dependencies | Software |
|---|---|---|
| tools/validate_publication.py | all data/schema; validate_data.py; a3_assertions.py | Python, jsonschema |
| audits/c/a3_relations/runner | verifier, manifest and ordinary JSON | C11, FLINT, GMP, MPFR |
| audits/run_a2_spectral.py | separate C/Python workers, shared spec; dilute A2 JSON, embeddings, local coefficients, spectral formula | Python launcher; respective FLINT backend |
| benchmarks/flint_ybe/runner | verifier; local coefficients, dilute A3 registry/matrices; local_embeddings and spectral_N comparison fixtures | C11, FLINT, GMP, MPFR |
| audits/python/run.py | spectral_ybe.py and same JSON fixtures; C results loaded only after Python workers finish | Python, python-flint |
| examples/import_spectral.py | dilute I and exported polynomial matrices/scalar | optional Sage |

The Python YBE report needs `benchmarks/flint_ybe/results.json`; run the C audit
first as documented. This is a reporting dependency, not C input to Python
mathematics. C does not invoke Python for arithmetic.

`validate_data.py` is a retained grammar/validation helper, not the public
whole-dataset command. Its optional legacy scalar consumer `exact_a2.py` requires
SymPy; this helper is retained to close the module's local import dependencies.
No exploratory research script is selected.

Excluded dependency chains: ordinary Python audit_representations.py imports
exploratory source witnesses; exact_a3.py's diagnostic branch reads historical
Git objects; old A3 summarizer reads a historical Python report; old A2 summarizer
checks manuscript hashes; dilute transcription/regeneration tools read M2.
Their replacements are NOT assumed approved. The independent portable C ordinary
manifest audit is included instead; source-transcription evidence remains labeled
historical rather than independently rerun.

References to `.m2`, `.tex`, source commits and source hashes inside provenance
are citations only, not runtime file dependencies. Selected rational fixtures
are necessary for exact comparison and are not superseded failed calculations.
Static review covered every selected Python/C source and Makefile; dynamic file
access evidence and isolation limitations are recorded in CLEAN_CHECKOUT_REPORT.md.
