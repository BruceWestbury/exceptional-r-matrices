# Exact Sage import example

From any directory, run `sage -python /path/to/repository/examples/import_spectral.py`.
From the repository root:

```sh
timeout -s KILL 60s sage -python examples/import_spectral.py
```

The default is dilute I (index 0, dimension 5). An optional integer argument
selects index 0–10, using the order in `data/dilute_a3.json`. This example was
run successfully with SageMath 10.6.beta2. Sage is optional and is not needed
for structural validation. Sage may need write access to its normal cache.

The script loads all 30 raw generator matrices and both already-normalized
polynomial spectral matrices from JSON. It specializes only `u`, to 2 and 1/2,
and verifies scaled unitarity in both positions over **QQ(p,q)**. No floating
point, finite-field sampling, transposition or audit-module import is used.
Do not apply the raw-generator normalisation multipliers to the spectral files:
they already represent the manuscript's Rpoly.

For another CAS: create the fraction field QQ(p,q,u), resolve named coefficient
aliases in dependency order, parse the restricted expression grammar in FORMAT.md,
and populate a zero matrix from the zero-based triples. Interpret multiplication
as the stored left-to-right product acting on row vectors on the right. Maple,
Mathematica and Magma users will generally add 1 to each stored matrix index.
