#!/usr/bin/env python3
"""Run with: sage -python examples/import_spectral.py [representation index].
Only JSON is used as mathematical input; no audit or Macaulay2 imports.
"""
import ast
import json
import sys
from pathlib import Path
from sage.all import QQ, PolynomialRing, matrix, identity_matrix

ROOT = Path(__file__).resolve().parents[1]
K = PolynomialRing(QQ, names=('p', 'q')).fraction_field()
p, q = K.gens()

def read(relative):
    return json.loads((ROOT / relative).read_text())

def evaluator(variables, definitions):
    """Restricted exact expression interpreter: never eval() source strings."""
    cache = dict(variables)
    active = set()

    def named(name):
        if name not in cache:
            if name in active:
                raise ValueError('cyclic scalar definition: ' + name)
            active.add(name)
            cache[name] = expression(definitions[name]['expression'])
            active.remove(name)
        return cache[name]

    def node(t):
        if isinstance(t, ast.Constant) and type(t.value) is int:
            return K(t.value)
        if isinstance(t, ast.Name):
            return named(t.id)
        if isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.USub):
            return -node(t.operand)
        if isinstance(t, ast.BinOp):
            a, b = node(t.left), node(t.right)
            if isinstance(t.op, ast.Add): return a + b
            if isinstance(t.op, ast.Sub): return a - b
            if isinstance(t.op, ast.Mult): return a * b
            if isinstance(t.op, ast.Div): return a / b
            if isinstance(t.op, ast.Pow):
                exponent = t.right
                if isinstance(exponent, ast.UnaryOp) and isinstance(exponent.op, ast.USub):
                    exponent = exponent.operand
                if not isinstance(exponent, ast.Constant) or type(exponent.value) is not int:
                    raise ValueError('exponent must be a signed integer literal')
                return a ** int(b)
        raise ValueError('unsupported scalar syntax: ' + ast.dump(t))

    def expression(s):
        return node(ast.parse(s.replace('^', '**'), mode='eval').body)
    return expression

def load_matrix(description, value):
    # The archive stores row-right matrices. No transpose or reversal of products.
    return matrix(K, description['rows'], description['cols'],
                  {(i, j): value(s) for i, j, s in description['entries']}, sparse=True)

def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    ordinary_input = read(f'data/dilute_representations/Dilute_{index}.json')
    spectral = read(f'data/spectral/Dilute_{index}.json')
    formula = read('data/spectral_r.json')
    assert ordinary_input['basis'] == spectral['basis']
    assert spectral['conventions']['action'] == 'row_vectors_right'
    raw_value = evaluator({'p': p, 'q': q}, {})
    generators = {m['operator']: load_matrix(m, raw_value)
                  for m in ordinary_input['matrices']}
    # Generators remain in raw source normalization; Rpoly is already normalized.
    def specialized(u):
        value = evaluator({'p': p, 'q': q, 'u': K(u)}, spectral['coefficient_definitions'])
        return [load_matrix(m, value) for m in spectral['matrices']]
    def normalization(u):
        value = evaluator({'p': p, 'q': q, 'u': K(u)}, formula['coefficient_definitions'])
        return value(formula['scalar_relationship']['normalization_scalar'])
    at_two, at_half = specialized(2), specialized(QQ(1)/2)
    scalar = normalization(2)*normalization(QQ(1)/2)
    target = scalar*identity_matrix(K, spectral['dimension'])
    for position, (a, b) in enumerate(zip(at_two, at_half), 1):
        assert a*b == target, f'unitarity failed at position {position}'
    print(json.dumps({'status': 'PASS', 'representation': spectral['id'],
                      'dimension': spectral['dimension'], 'raw_generators_loaded': len(generators),
                      'positions': [1, 2], 'spectral_values': ['2', '1/2'],
                      'coefficient_field': 'QQ(p,q)',
                      'check': 'Rpoly_i(2)*Rpoly_i(1/2) = N(2)*N(1/2)*Id',
                      'scope': 'exact specialized example; not a generic YBE audit'}, indent=2))

if __name__ == '__main__':
    main()
