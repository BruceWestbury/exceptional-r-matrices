# Dataset provenance

Research source: repository named Zenodo, clean HEAD `83aed000254bf7aca4836f0d3e3fb47c818ee4fa`.
The source repository and Git history remain untouched. The public candidate has
no .git directory. Source hashes for every selected file and every original data
JSON file are in PUBLICATION_MANIFEST.json; no original Git object is needed
at runtime. Historical source commits are citations, not public-history claims.

All matrix entries, scalar definitions, basis maps and generator embeddings are
preserved. The only data transformations are (1) replacing the absolute research
path in dilute_a3.json's provenance label, (2) selecting included report references
in publication.json, and (3) refreshing public payload hashes/classification in
publication_provenance.json. These metadata-only changes are explicit in the
manifest and are checked independently of the mathematical tests.

The public format document omits the legacy ordinary-only CLI section. Audit
mathematics is copied byte-for-byte. Publication metadata and README are drafts.
No private manuscript/M2 content is copied. Source filenames and hashes remain
as citations to preserve mathematical provenance, not as runtime requirements.

The included historical assembly report is conditional and incomplete: 298
matrices reconstructed, 32 partial, 92 unknown entries. No missing morphism is
invented or reconstructed during curation. Fresh exact identity checks are
separate evidence and do not resolve that provenance gap.
