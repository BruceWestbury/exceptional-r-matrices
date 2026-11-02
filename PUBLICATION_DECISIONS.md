# Maintenance and contributions

This repository brings together exact matrix data, ExceptionalDiagrams and
reproducible algebraic checks. Contributions can improve the mathematical data,
package functionality, verification coverage or documentation.

## Updating data and code

1. Describe the affected representation, diagram or identity and its normalization.
   Give a small example and the expected behavior.
2. Update the maintained package in `macaulay2/` and the corresponding JSON entries
   together when a change affects their common mathematical content.
3. Run structural validation and the relevant exact checks. For package or matrix
   changes, run the package comparison and the C/Python identity checks that
   exercise the affected objects.
4. Update the format guide and usage examples when conventions or interfaces
   change. Refresh payload hashes after editing their inputs.
5. Save new verification results under a fresh run name and describe their scope
   in the change summary.

Commands and dependencies are in [README.md](README.md) and
[DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md). The package's GitHub Actions workflow
provides structural validation, failure-detection tests and exact package/data
checks.

## Further verification work

Two useful extensions are an independent construction of the 92 remaining
ordinary-to-dilute transition entries and an explicit encoding of the
degree-seven relation for the braid-generator presentation. The
[coverage guide](AUDIT_COVERAGE.md#further-construction-checks) describes the
required mathematical inputs.

## Releases, citation and licence

A release should identify the revision, summarize mathematical and interface
changes, and link its verification results. Keep [CITATION.cff](CITATION.cff)
consistent with the accompanying paper's bibliographic details.

Data, documentation and software use [CC BY 4.0](LICENSE). Preserve the authorship
credits and describe modifications when redistributing adapted material.
