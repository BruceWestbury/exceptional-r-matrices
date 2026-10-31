# ExceptionalDiagrams

Paul Zinn-Justin's Macaulay2 package provides diagram operations, skein reduction,
ordinary and dilute representations on two and three strings, braiding, and the
spectral R-matrix for the exceptional series. This directory is the maintained
package source. Keep `ExceptionalDiagrams.m2` beside the `ExceptionalDiagrams/`
auxiliary directory when copying or installing it.

## Requirements and loading

Use Macaulay2 with the `VectorGraphics` package available. `Factor` is optional:
the package falls back to ordinary polynomial/fraction arithmetic without it.
Python, JSON readers, and the C/FLINT audit programs are not package dependencies.

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

To install a copy for subsequent sessions:

```m2
path = prepend(toAbsolutePath "macaulay2/",path);
installPackage("ExceptionalDiagrams",
    FileName=>"macaulay2/ExceptionalDiagrams.m2");
```

Then use `needsPackage "ExceptionalDiagrams"` and `check "ExceptionalDiagrams"`.
The latter runs the package's five built-in `TEST` blocks. Macaulay2's
[package documentation](https://www.macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_creating_spa_sppackage.html)
describes this installation and test mechanism.

## Normalizations and representations

The default configuration is `"alpha"=>"paper", "parameters"=>"generic"`.
It gives the ordinary manuscript normalization. For the dilute normalization in
Section 8, load the following in a fresh session:

```m2
needsPackage("ExceptionalDiagrams",
    FileName=>"macaulay2/ExceptionalDiagrams.m2",
    Configuration=>{"alpha"=>"paper2","parameters"=>"generic"});
```

The three-string indices are I, L, X2, Y2, Y2_star, X3, Y3, Y3_star, A, C,
C_star, numbered 0 through 10; two-string indices use the first five labels.
Set `Dilute` explicitly when an input diagram could act in either algebra.
`rep` on a zero diagram also needs `Strands=>2` or `Strands=>3`.

The JSON ordinary matrices use `paper` normalization. The dilute generator JSON
stores raw auxiliary matrices, before either package rescaling: use the registry's
`paper_multiplier` or `paper2_multiplier`, respectively. The spectral JSON stores
the polynomial prefactor times the `paper2` representation of `Rmatrix()`.
See [FORMAT.md](../FORMAT.md) for that prefactor and the remaining manuscript
basis maps. Ordinary Y2 uses the same basis throughout. Package and dilute JSON
coordinates already agree, so manuscript basis maps must not be reapplied when
comparing those two sources.

## Verification

From the repository root:

```sh
python3 tools/check_macaulay2_data.py --package-tests --output /tmp/m2-check.json
```

Without `--package-tests`, this checks all 542 stored matrices against the actual
package over QQ(p,q,u), including both normalizations of the 410 raw dilute
matrices (952 matrix comparisons in total). It also checks the scalar rescalings.
Python requires `jsonschema`; all arithmetic is performed by Macaulay2. No
manuscript, research directory, SymPy, or python-flint is needed. Differences are
reported with representation, normalization, operator, and zero-based entry.
Use `--representation Y2` for a focused check. The checker never updates matrices
or overwrites an existing report.

The runner can also be invoked by absolute path from another working directory;
its input paths are resolved relative to the checkout, not that directory.

`--package-tests` additionally runs the five built-in tests and the standalone
generic suite in both normalizations. The extended suite is divided into groups,
with the 80-diagram restriction checks run separately for each representation;
the slower `paper2` L checks use four ranges of 20 diagrams. The assertions are
unchanged. It installs a disposable copy, removes the installation source, and
exercises the installed package in fresh sessions
outside the checkout. All generated installation files and test scripts are
temporary. Workers are limited to 60 seconds. Matrix comparisons, each package
normalization, and installation have separate 300-second batch limits.

The standalone suite is also available directly:

```sh
M2 --script macaulay2/tests/exceptional-diagrams.m2 paper generic
M2 --script macaulay2/tests/exceptional-diagrams.m2 paper2 generic
```

Its optional `multiplication` and `ybe` suites retain their original behavior;
the default integration check uses the generic basic suite. The existing C and
Python audits remain independent tests of the JSON data. Agreement with the
package does not independently reconstruct the missing assembly morphisms
described in [AUDIT_COVERAGE.md](../AUDIT_COVERAGE.md).

For future changes, edit this maintained package, update affected JSON deliberately,
and require the comparison and independent audits to pass. A deterministic export
tool can be added later; the current checker does not silently synchronize files.
The repository's [licence status](../LICENSE) also applies to this package.
