# ExceptionalDiagrams

Paul Zinn-Justin's Macaulay2 package provides diagram operations, skein reduction,
ordinary and dilute representations on two and three strings, braiding, and
spectral R-matrices for the exceptional series. The package consists of
`ExceptionalDiagrams.m2` and its adjacent `ExceptionalDiagrams/` auxiliary directory.
Keep these together when copying or installing it.

## Requirements and loading

Install Macaulay2 with `VectorGraphics`. The optional `Factor` package enables
factored arithmetic; ordinary polynomial and fraction arithmetic is also supported.
From the repository root, in Macaulay2:

```m2
needsPackage("ExceptionalDiagrams",
    FileName=>"macaulay2/ExceptionalDiagrams.m2");

s1 = rep(3,(braid())_1,Dilute=>false);
s2 = rep(3,(braid())_2,Dilute=>false);
assert(s1*s2*s1 == s2*s1*s2);

rr = rep(1,Rmatrix(),Dilute=>true);
assert(rr*sub(rr,u=>1/u) == id_(source rr));
```

To install a copy for later sessions:

```m2
path = prepend(toAbsolutePath "macaulay2/",path);
installPackage("ExceptionalDiagrams",
    FileName=>"macaulay2/ExceptionalDiagrams.m2");
```

Then load it with `needsPackage "ExceptionalDiagrams"` and run its five built-in
`TEST` blocks with `check "ExceptionalDiagrams"`.

## Normalizations and representations

The default configuration is `"alpha"=>"paper", "parameters"=>"generic"`, giving
the ordinary normalization. For the dilute normalization used in Section 8 of
the paper, start a fresh session and use:

```m2
needsPackage("ExceptionalDiagrams",
    FileName=>"macaulay2/ExceptionalDiagrams.m2",
    Configuration=>{"alpha"=>"paper2","parameters"=>"generic"});
```

Three-string representations are indexed from 0 through 10 in the order
I, L, X2, Y2, Y2_star, X3, Y3, Y3_star, A, C, C_star. Two-string indices use the
first five labels. Set `Dilute` explicitly when a diagram could act in either
algebra. For `rep` on a zero diagram, also supply `Strands=>2` or `Strands=>3`.

Ordinary JSON matrices use `paper` normalization. Raw dilute JSON matrices acquire
the selected normalization through `paper_multiplier` or `paper2_multiplier` in
the registry. Spectral JSON matrices equal the polynomial prefactor times the
`paper2` representation of `Rmatrix()`.
[FORMAT.md](../FORMAT.md) defines that prefactor and the paper's displayed-table
basis maps. Package/data comparisons use their shared coordinates, including
the common ordinary Y2 basis.

## Verification

The comparison runner requires Python with `jsonschema` and Macaulay2. From the
repository root:

```sh
python3 tools/check_macaulay2_data.py --output /tmp/m2-comparison.json
```

This performs 952 exact matrix comparisons over QQ(p,q,u), covering all 542
stored matrices and both normalizations of the 410 raw dilute matrices, plus
scalar checks. Macaulay2 performs the arithmetic. Differences identify the
representation, normalization, operator and zero-based entry. Use
`--representation Y2` for a focused check and a fresh output filename for each run.
The runner resolves its inputs relative to the checkout and also accepts
invocation by absolute path.

To include package and installation tests:

```sh
python3 tools/check_macaulay2_data.py --package-tests --output /tmp/m2-check.json
```

This additionally runs the five built-in tests and standalone generic suite in
both normalizations. Restriction checks are grouped by representation, with the
`paper2` L checks split into four groups of twenty diagrams. Installation checks
exercise a temporary installed package in fresh sessions outside the checkout.
Workers have 60-second limits; matrix comparisons, each package normalization
and installation have separate 300-second batch limits.

The standalone generic suite can also be run directly:

```sh
M2 --script macaulay2/tests/exceptional-diagrams.m2 paper generic
M2 --script macaulay2/tests/exceptional-diagrams.m2 paper2 generic
```

The script also offers `multiplication` and `ybe` suites. The
[verification overview](../AUDIT_COVERAGE.md) explains the relationship between
package agreement, algebraic identities and construction evidence.

## Development and licence

Edit the package here, update affected JSON entries together with mathematical
changes, and run the comparison and relevant identity checks. The
[maintenance guide](../PUBLICATION_DECISIONS.md) describes the repository workflow.

ExceptionalDiagrams, including its auxiliary files and tests, is distributed
under [CC BY 4.0](../LICENSE). Please retain Paul Zinn-Justin's authorship credit.
