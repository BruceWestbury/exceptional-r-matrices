# SageMath import example

The example imports exact matrices from JSON and checks scaled unitarity in
both spectral positions. From the repository root:

```sh
timeout -s KILL 60s sage -python examples/import_spectral.py
```

The default representation is dilute I (index 0, dimension 5). An integer
argument selects another representation from indices 0–10, in the order given
by [data/dilute_a3.json](../data/dilute_a3.json). The script also accepts invocation
by absolute path from another directory. It was tested with SageMath 10.6.beta2;
SageMath uses its usual writable cache directory.

## What the example computes

The script loads 30 raw generator matrices and the two polynomial spectral
matrices. It evaluates the spectral parameter at u=2 and u=1/2 and checks scaled
unitarity over QQ(p,q). Arithmetic is exact. The spectral files already carry
the polynomial normalization specified in [FORMAT.md](../FORMAT.md).

## Importing into another algebra system

Create QQ(p,q,u), resolve scalar aliases in dependency order, and parse the
restricted expression grammar in the format guide. Populate a zero matrix from
the stored zero-based triples. Vectors act on the right as rows, and generator
words are multiplied in the stored order. Systems with one-based matrix indices,
such as Maple, Mathematica and Magma, should add 1 to each stored index.
