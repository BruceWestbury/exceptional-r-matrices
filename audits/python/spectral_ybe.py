#!/usr/bin/env python3
"""Independent exact spectral audit. No imports from other repository audits.

Authority: yangbaxter.tex eq:Rmat (8.3), polynomial display at 798--800.
Construction uses Q(p,q,u); YBE uses Q[p,q,u,v], degree-reverse-lex order.
"""
from __future__ import annotations

import ast
import json
import time
from functools import lru_cache
from pathlib import Path

import flint
from flint import fmpq_mpoly_ctx

ROOT = Path(__file__).resolve().parents[2]
RING = fmpq_mpoly_ctx.get(('p', 'q', 'u'), 'degrevlex')
YBE_RING = fmpq_mpoly_ctx.get(('p', 'q', 'u', 'v'), 'degrevlex')


class Fraction:
    """Reduced fractions; cross-cancel products and use denominator gcd in sums."""

    def __init__(self, numerator=0, denominator=1):
        n, d = RING.constant(numerator) if isinstance(numerator, int) else numerator, (
            RING.constant(denominator) if isinstance(denominator, int) else denominator)
        if not d:
            raise ZeroDivisionError('zero polynomial denominator')
        if not n:
            self.n, self.d = RING.constant(0), RING.constant(1)
            return
        g = n.gcd(d)
        n, d = n / g, d / g
        leading = d.leading_coefficient()
        self.n, self.d = n / leading, d / leading

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Fraction) else Fraction(value)

    def __bool__(self):
        return bool(self.n)

    def __neg__(self):
        return Fraction(-self.n, self.d)

    def __add__(self, other):
        other = self.coerce(other)
        common = self.d.gcd(other.d)
        a, b = self.d / common, other.d / common
        return Fraction(self.n * b + other.n * a, a * other.d)

    __radd__ = __add__

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        g = self.n.gcd(other.d)
        h = other.n.gcd(self.d)
        return Fraction((self.n / g) * (other.n / h),
                        (self.d / h) * (other.d / g))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        return self * Fraction(other.d, other.n)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __pow__(self, exponent):
        if exponent < 0:
            return Fraction(self.d ** -exponent, self.n ** -exponent)
        return Fraction(self.n ** exponent, self.d ** exponent)

    def diagnostic(self):
        return {'numerator': str(self.n), 'denominator': str(self.d)}


P, Q, U = (Fraction(g) for g in RING.gens())


def read(relative):
    return json.loads((ROOT / relative).read_text())


def scalar(text, lookup):
    """Parse only the specified scalar grammar; never eval input text."""
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return Fraction(node.value)
        if isinstance(node, ast.Name):
            return lookup(node.id)
        if isinstance(node, ast.UnaryOp):
            a = visit(node.operand)
            if isinstance(node.op, ast.USub):
                return -a
            if isinstance(node.op, ast.UAdd):
                return a
        if isinstance(node, ast.BinOp):
            a = visit(node.left)
            if isinstance(node.op, ast.Pow):
                exponent = ast.literal_eval(node.right)
                if type(exponent) is not int:
                    raise ValueError('noninteger exponent')
                return a ** exponent
            b = visit(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
            if isinstance(node.op, ast.Div):
                return a / b
        raise ValueError(f'unsupported scalar AST: {ast.dump(node)}')
    return visit(ast.parse(text.replace('^', '**'), mode='eval').body)


def bracket(n=0, x=0, constant=0):
    monomial = P ** n * U ** x * Q ** constant
    return (monomial - monomial ** -1) / (Q - Q ** -1)


# Matrices are dictionaries {(row, column): nonzero exact scalar}.
def identity(dimension):
    return {(i, i): Fraction(1) for i in range(dimension)}


def linear_combination(*terms):
    result = {}
    for coefficient, matrix in terms:
        for ij, value in matrix.items():
            result[ij] = result.get(ij, 0) + coefficient * value
    return {ij: value for ij, value in result.items() if value}


def multiply(left, right):
    """Sparse row join, works for both fractions and FLINT polynomials."""
    rows = {}
    for (k, j), value in right.items():
        rows.setdefault(k, []).append((j, value))
    result = {}
    for (i, k), a in left.items():
        for j, b in rows.get(k, ()):
            ij = (i, j)
            result[ij] = result.get(ij, 0) + a * b
    return {ij: value for ij, value in result.items() if value}


def construct(index):
    document = read(f'data/dilute_representations/Dilute_{index}.json')
    registry = read('data/dilute_a3.json')
    ordinary = read('data/local_a2.json')
    embeddings = read('reports/paper_audit/local_embeddings.json')['positions']
    dimension = document['dimension']

    @lru_cache(None)
    def coefficient(name):
        if name in {'p', 'q', 'u'}:
            return {'p': P, 'q': Q, 'u': U}[name]
        if name == 'beta':
            return scalar(registry['normalization_prescriptions']['beta'], coefficient)
        return scalar(ordinary['coefficients'][name]['expression'], coefficient)

    generators = {}
    specs = {s['operator']: s for s in registry['generators']}
    for matrix in document['matrices']:
        label = matrix['operator']
        factor = scalar(specs[label]['paper2_multiplier'], coefficient)
        generators[label] = {(i, j): scalar(value, coefficient) * factor
                             for i, j, value in matrix['entries']}
    assert len(generators) == 30
    relations = {r['id']: r for r in ordinary['relations']}
    matrices = []
    # Literal rational coefficients of manuscript (8.3), before normalization.
    n, n1, n2, n3, n6 = (bracket(1), bracket(1, constant=1), bracket(2),
                          bracket(3), bracket(6))
    x = bracket(x=1)
    prefactor = 1 / (bracket(1, 1, 1) * bracket(0, 1, -1))
    innerfactor = n2 * n3 * n1 * x / (n6 * bracket(2, 1))
    weights = {
        'identity': n1,
        'S': -P ** -1 * U ** -1 * x / (Q - Q ** -1),
        'Sinv': P * U * x / (Q - Q ** -1),
        'K': -innerfactor * n,
        'T': innerfactor,
        'B': -innerfactor / n,
        'E': -innerfactor * bracket(x=2) / (x * bracket(3, 1)),
        'U': innerfactor / n * (n6 * bracket(2, 1) / (n3 * bracket(3, 1)) - 1),
        'O': -innerfactor * (bracket(12, 2) / (bracket(6, 1) * bracket(3, 1)) + 2 / n),
    }
    # Keep the paper's scalar separate from later arithmetic clearing.
    manuscript_factor = (n6 ** 2 * n / (n3 ** 2 * n2)
                         * bracket(1, 1, 1) * bracket(0, 1, -1)
                         * bracket(2, 1) * bracket(3, 1))
    for position in ('1', '2'):
        local = {}
        for label, words in embeddings[position].items():
            summands = []
            for word in words:
                product = identity(dimension)
                for generator in word:
                    product = multiply(product, generators[f'G{generator}'])
                summands.append((1, product))
            local[int(label)] = linear_combination(*summands)

        def local_sum(*indices):
            return linear_combination(*((1, local[i]) for i in indices))

        ops = {'H': linear_combination((n1, local[3])),
               'K': linear_combination((n1, local[2])), 'U': local[1]}
        ops['H2'] = multiply(ops['H'], ops['H'])
        spectral_ops = {'identity': identity(dimension), 'K': local[2],
                        'U': local[1], 'O': local[15], 'T': local_sum(9, 10, 11, 12),
                        'B': local_sum(5, 6, 7, 8), 'E': local_sum(13, 14)}
        for label in ('S', 'Sinv'):
            summands = [(1, local_sum(6, 7, 15))]
            for term in relations[label + '_polynomial']['rhs']['terms']:
                product = local[0]
                for operator in term['word']:
                    product = multiply(product, ops[operator])
                summands.append((scalar(term['coefficient'], coefficient), product))
            spectral_ops[label] = linear_combination(*summands)
        rational_matrix = linear_combination(
            *((prefactor * weight, spectral_ops[label]) for label, weight in weights.items()))
        matrices.append(linear_combination((manuscript_factor, rational_matrix)))
    return dimension, matrices, manuscript_factor


def clear_denominators(matrices):
    """One monic LCM for both positions, verified entrywise exactly."""
    denominator = RING.constant(1)
    for matrix in matrices:
        for value in matrix.values():
            denominator = denominator * (value.d / denominator.gcd(value.d))
    exponents = {monomial[2] for monomial in denominator.monoms()}
    if len(exponents) != 1:
        raise ValueError('remaining denominator is not D(p,q) times a power of u')
    shift = int(exponents.pop())
    factor_pq = denominator / RING.gen(2) ** shift
    assert factor_pq.degrees()[2] <= 0 and denominator
    polynomials = []
    for matrix in matrices:
        result = {}
        for ij, value in matrix.items():
            result[ij] = value.n * (denominator / value.d)
            assert result[ij] * value.d == value.n * denominator
        polynomials.append(result)
    return polynomials, {'D_pq': str(factor_pq), 'u_shift': shift,
                         'common_multiplier': str(denominator),
                         'YBE_common_scalar': f'({factor_pq})^3*u^{2*shift}*v^{2*shift}',
                         'entrywise_clearing_verified': True}


def compare_rational(index, dimension, matrices, factor):
    # Only called after construction and YBE. Never provides construction input.
    artifact = read(f'reports/paper_audit/spectral_{index}.json')
    variables = {'p': P, 'q': Q, 'u': U}
    failures = []
    for position, matrix in enumerate(matrices, 1):
        data = artifact['positions'][str(position)]
        assert data['dimension'] == dimension
        prior = {(i, j): scalar(s, variables.__getitem__) for i, j, s in data['entries']}
        for i in range(dimension):
            for j in range(dimension):
                residual = matrix.get((i, j), Fraction()) - factor * prior.get((i, j), Fraction())
                if residual:
                    failures.append({'position': position, 'entry': [i, j],
                                     'residual': residual.diagnostic()})
    return failures


def audit(index, emit):
    start = time.monotonic()
    emit({'phase': 'construction_started'})
    dimension, matrices, factor = construct(index)
    construction = time.monotonic() - start
    emit({'phase': 'construction_complete', 'construction_seconds': construction})
    clearing_start = time.monotonic()
    polynomials, clearing = clear_denominators(matrices)
    clearing_seconds = time.monotonic() - clearing_start
    emit({'phase': 'clearing_complete', 'clearing': clearing,
          'clearing_seconds': clearing_seconds})
    ybe_start = time.monotonic()
    p, q, u, v = YBE_RING.gens()

    def at(matrix, spectral):
        return {ij: a.compose(p, q, spectral, ctx=YBE_RING) for ij, a in matrix.items()}

    first, second = polynomials
    lhs = multiply(multiply(at(first, u), at(second, u * v)), at(first, v))
    emit({'phase': 'left_triple_complete', 'elapsed_ybe_seconds': time.monotonic() - ybe_start})
    rhs = multiply(multiply(at(second, v), at(first, u * v)), at(second, u))
    failures = []
    for i in range(dimension):
        for j in range(dimension):
            residual = lhs.get((i, j), 0) - rhs.get((i, j), 0)
            if residual:
                failures.append({'entry': [i, j], 'cleared_residual': str(residual)})
    ybe_seconds = time.monotonic() - ybe_start
    emit({'phase': 'YBE_complete', 'ybe_seconds': ybe_seconds,
          'nonzero_residuals': failures})
    comparison_start = time.monotonic()
    comparison_failures = compare_rational(index, dimension, matrices, factor)
    result = {'status': 'FAIL' if failures or comparison_failures else 'PASS',
              'index': index, 'dimension': dimension,
              'construction_seconds': construction, 'clearing_seconds': clearing_seconds,
              'ybe_seconds': ybe_seconds,
              'comparison_seconds': time.monotonic() - comparison_start,
              'worker_seconds': time.monotonic() - start,
              'clearing': clearing, 'ybe_residuals': failures,
              'rational_comparison_residuals': comparison_failures,
              'checked_ybe_entries': dimension ** 2,
              'checked_comparison_entries': 2 * dimension ** 2,
              'R_terms': [sum(len(a.to_dict()) for a in m.values()) for m in polynomials],
              'triple_terms': [sum(len(a.to_dict()) for a in m.values()) for m in (lhs, rhs)]}
    emit(result)
    return result
