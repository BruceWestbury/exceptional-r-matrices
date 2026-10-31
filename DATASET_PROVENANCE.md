# Dataset provenance

Research source: repository named Zenodo, clean HEAD `83aed000254bf7aca4836f0d3e3fb47c818ee4fa`.
The source repository and Git history remain untouched. The initial public copy
excluded the research .git directory. Source hashes for every selected file and every original data
JSON file are in PUBLICATION_MANIFEST.json; no original Git object is needed
at runtime. Historical source commits are citations, not public-history claims.

Initial curation preserved all matrix entries, scalar definitions, basis maps and
generator embeddings. Its data transformations were (1) replacing the absolute research
path in dilute_a3.json's provenance label, (2) selecting included report references
in publication.json, and (3) refreshing public payload hashes/classification in
publication_provenance.json. These metadata-only changes are explicit in the
manifest and are checked independently of the mathematical tests.

On 2026-11-01, at the author's request, every ordinary Y2 operator was conjugated
by D=diag(1,-1,1) to adopt the current manuscript and Macaulay2 basis. The obsolete
ordinary Y2 map was removed from basis_maps.json. Dilute and spectral matrices
already use the corresponding source coordinates and were not changed. Current
payload hashes are refreshed; research-source hashes and historical audit results
retain their original meaning. The historical ordinary-to-dilute audit's Y2 sign
map applies only to the pre-change ordinary matrices, not to the current data.

The public format document omits the legacy ordinary-only CLI section. The
existing C/Python audit mathematics is copied byte-for-byte. Publication metadata
remains provisional. No manuscript sources are included.

The author subsequently authorized inclusion of ExceptionalDiagrams. Its 37
auxiliary files were copied unchanged into `macaulay2/`. The package's exported
coefficients b,c now have their own public symbols rather than aliases to private
symbols, fixing installPackage documentation generation without changing their
values or any mathematical calculation. The standalone test script was imported
with its assertions unchanged and given optional group selection for bounded
workers. This is now the maintained package; the research copy is an archive.
`tools/check_macaulay2_data.py` loads only this bundled package and the public
JSON, and checks exact agreement in both package normalizations. Its
optional package tests install a temporary copy and load it after removing the
installation source. No runtime access to the research tree is needed. Original
source hashes retain their historical meaning; the manifest records the newly
included source files and their current destinations.

The included historical assembly report is conditional and incomplete: 298
matrices reconstructed, 32 partial, 92 unknown entries. No missing morphism is
invented or reconstructed during curation. Fresh exact identity checks are
separate evidence and do not resolve that provenance gap.
