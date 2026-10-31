# Audit coverage

The verification suite tests the public JSON inputs using exact arithmetic.

- C/FLINT ordinary A(3): all applicable relations in the reviewed declarative
  manifest, in eleven representations. The recorded reference count is 1,605
  PASS and 45 NOT APPLICABLE. This includes the complete displayed six-generator
  presentation, not an unprinted degree-seven braid-generator relation.
- Python/FLINT and C/FLINT dilute A(2): unitarity in five representations;
  crossing coefficientwise in all sixteen diagrams, with scalar equivalence
  between rational and manuscript polynomial formulations checked separately.
- Independent Python/FLINT and C/FLINT spectral YBE: all eleven dilute A(3)
  representations, over generic algebraically independent p,q,u,v, not sampling.
  Saved rational matrices are comparison fixtures, not primary YBE input.
- Structural validation: all publication JSON, schemas, scalar grammar, indices,
  cross references and integrity hashes. Structural validity is not a proof.
- Optional Sage: exact specialized unitarity at u=2 and 1/2 over QQ(p,q), both
  positions in dilute I; not another generic YBE proof.

The independent implementations share source specifications and FLINT's library
family; they do not use each other's computed matrices. C generic arithmetic
infrastructure is reused where documented. Geometric diagram rotation and the
abstract basis/presentation conclusions are not re-proved computationally.

Historical construction evidence establishes 298/330 complete ordinary-to-dilute
matrix reconstructions, 32 partial matrices and 92 unresolved transition entries.
All 330 source transcriptions were separately compared with the retained M2
source in the research repository. Those source-comparison calculations cannot
be rerun here: M2 and missing assembly sources are deliberately excluded. The
selected correspondence and final report preserve their provenance and limits.

The old Python ordinary-audit wrapper and research-only report generators are
excluded; no replacement mathematical evaluator is silently substituted.
Fresh results and failures, if any, are reported in CLEAN_CHECKOUT_REPORT.md.
