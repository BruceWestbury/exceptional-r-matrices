"""Exploratory SymPy consumer of local JSON; not a format/backend commitment.

All backend-specific scalar construction and bar substitution live here.
No source manuscript or exploratory program is read to obtain current data.
"""

from functools import reduce
from itertools import permutations

from sympy import QQ
from sympy.polys.fields import field

from validate_data import Invalid, coefficient_order, load_validated, parse_scalar


class ExactA2:
    def __init__(self, path=None, *, data=None):
        # data is used only after structural validation by another profile.
        self.data = load_validated(path) if data is None else data
        self.field, self.p, self.q = field(",".join(self.data["field"]["variables"]), QQ)
        self.values = dict(zip(self.data["field"]["variables"], (self.p, self.q)))
        for name in coefficient_order(self.data):
            self.values[name] = self.scalar(self.data["coefficients"][name]["expression"])
        self.relations = {r["id"]: r for r in self.data["relations"]}
        self.scalar_checks = {r["id"]: r for r in self.data["scalar_checks"]}
        self.characters = [dict(zip(self.data["characters"]["column_order"],
                                   map(self.scalar, row["values"])))
                           for row in self.data["characters"]["rows"]]

    def extend_coefficients(self, definitions):
        """Evaluate a validated, non-shadowing algebra-level extension."""
        if set(definitions) & set(self.values):
            raise Invalid('duplicate coefficient ownership in exact consumer')
        combined = dict(self.data, coefficients={**self.data["coefficients"], **definitions})
        for name in coefficient_order(combined):
            if name in definitions:
                self.values[name] = self.scalar(definitions[name]["expression"])

    def scalar(self, text):
        def interpret(node):
            op = node[0]
            if op == "int":
                return self.field(node[1])
            if op == "id":
                return self.values[node[1]]
            left = interpret(node[1])
            if op == "neg":
                return -left
            if op == "pow":
                if not left and node[2] <= 0:
                    raise Invalid("zero to nonpositive power is not supported")
                return left ** node[2]
            right = interpret(node[2])
            if op == "+":
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                return left / right
            raise Invalid(f"unknown scalar operation: {op}")
        return interpret(parse_scalar(text))

    def bar(self, value):
        return self.field.from_expr(value.as_expr().subs(
            {self.p.as_expr(): self.p.as_expr()**-1,
             self.q.as_expr(): self.q.as_expr()**-1}, simultaneous=True))

    def character_expression(self, expression, character):
        return sum((self.scalar(t["coefficient"]) * reduce(
            lambda a, b: a*b, (character[x] for x in t["word"]), self.field.one)
                    for t in expression["terms"]), self.field.zero)

    def reduced_cell(self, cell):
        """Exact whole-word replacement for completed table RHSs, not a CAS rewriter."""
        terms = []
        rules = [self.relations[r] for r in self.data["tables"]["completed"]["reduction_rules"]]
        for term in cell["terms"]:
            replacement = next((r["rhs"]["terms"] for r in rules
                                if term["word"] == r["lhs"]["terms"][0]["word"]), None)
            if replacement is None:
                terms.append(term)
            else:
                terms.extend({"coefficient": f'({term["coefficient"]})*({t["coefficient"]})',
                              "word": t["word"]} for t in replacement)
        result = {b: self.field.zero for b in self.data["basis_order"]}
        for term in terms:
            word = term["word"]
            if word != [] and (len(word) != 1 or word[0] not in result):
                raise Invalid(f"table does not close in declared basis: {word}")
            result[word[0] if word else "one"] += self.scalar(term["coefficient"])
        return result

    def square_square_analysis(self):
        """Solve from characters only; no b formula is used in elimination."""
        if hasattr(self, '_square_square_result'):
            return self._square_square_result
        spec = self.data['square_square']
        basis = self.data['basis_order']
        relation = self.relations[spec['relation_ref']]
        C = [[r[b] for b in basis] for r in self.characters]
        y = [self.character_expression(relation['lhs'], r) for r in self.characters]
        # Put sparse columns first to limit rational-function expression swell.
        order = sorted(range(5), key=lambda j: sum(bool(row[j]) for row in C))
        A = [[row[j] for j in order]+[value] for row,value in zip(C,y)]
        inversions = sum(order[i] > order[j] for i in range(5) for j in range(i+1,5))
        determinant = self.field((-1)**inversions)
        for k in range(5):
            pivot = next((i for i in range(k,5) if A[i][k]), None)
            if pivot is None:
                raise Invalid('square-square characters do not separate the basis')
            if pivot != k:
                A[k],A[pivot] = A[pivot],A[k]
                determinant = -determinant
            value = A[k][k]
            determinant *= value
            A[k] = [v/value for v in A[k]]
            for i in range(5):
                if i != k and A[i][k]:
                    value = A[i][k]
                    A[i] = [v-value*w for v,w in zip(A[i],A[k])]
        solution = [self.field.zero]*5
        for i,j in enumerate(order):
            solution[j] = A[i][-1]
        if determinant != self.scalar(spec['determinant']) or not determinant:
            raise Invalid('square-square determinant certificate failed')
        for i,row in enumerate(C):
            if sum((c*v for c,v in zip(row,solution)),self.field.zero) != y[i]:
                raise Invalid('square-square linear-system solution failed')
        for name,value in zip(spec['coefficient_order'],solution):
            if self.values[name] != value:
                raise Invalid('square-square unique solution disagrees with stored '+name)
        evidence=[]
        for item in self.data['coefficient_evidence']:
            residual=self.scalar(item['expression'])-self.values[item['coefficient']]
            passed=(residual==self.scalar(item['residual']) and
                    bool(residual)==(item['status']=='disagrees'))
            if not passed:
                raise Invalid('printed coefficient regression failed: '+item['id'])
            evidence.append(dict(id=item['id'],passed=passed,status=item['status']))
        self._square_square_result = dict(matrix=C,rhs=y,determinant=determinant,solution=solution,evidence=evidence)
        return self._square_square_result

    def audit(self):
        failures = []
        result = self.square_square_analysis()
        print('JSON square-square exact 5x5 solve, nonzero determinant and unique b coefficients: PASS', flush=True)
        for item in result['evidence']:
            action = 'rejected' if item['status']=='disagrees' else 'agrees'
            print(f"JSON printed {item['id']} {action}: PASS", flush=True)

        def report(name, residuals):
            bad = [(i, r) for i, r in enumerate(residuals) if r != self.field.zero]
            print(f"JSON {name}: {'FAIL' if bad else 'PASS'}", flush=True)
            if bad:
                failures.append(name)
                print(f"  first nonzero residual [{bad[0][0]}] = {bad[0][1]}")

        # Canonical zero coefficients require field equality, not schema syntax.
        expressions = [side for r in self.data["relations"] for side in (r["lhs"], r["rhs"])]
        expressions += [cell for table in self.data["tables"].values() for row in table["cells"] for cell in row]
        for expr in expressions:
            for term in expr["terms"]:
                if self.scalar(term["coefficient"]) == self.field.zero:
                    raise Invalid(f"noncanonical zero coefficient: {term}")
        for item in self.data["scalar_checks"]:
            report("coefficient " + item["id"], [self.scalar(item["lhs"]) - self.scalar(item["rhs"])])
        for name, definition in self.data["coefficients"].items():
            if "bar_of" in definition:
                report("bar coefficient " + name, [self.values[name] - self.bar(self.values[definition["bar_of"]])])
        for name, declaration in self.data["elements"].items():
            if "word" in declaration:
                rhs = {"terms": [{"coefficient": "1", "word": declaration["word"]}]}
                report("element definition " + name, [r[name]-self.character_expression(rhs, r) for r in self.characters])
        for table_name, table in self.data["tables"].items():
            residuals = []
            for i, left in enumerate(table["row_order"]):
                for j, right in enumerate(table["column_order"]):
                    cell = table["cells"][i][j]
                    residuals.extend(r[left]*r[right]-self.character_expression(cell, r) for r in self.characters)
                    if table_name == "completed":
                        reduced = self.reduced_cell(cell)
                        residuals.extend(self.character_expression(cell, r)-sum(
                            (c*r[b] for b, c in reduced.items()), self.field.zero) for r in self.characters)
            size = len(table["cells"])**2
            label = f"{table_name} table ({size} cells, {5*size} character products)"
            if table_name == "completed":
                label += "; cubic reductions checked"
            report(label, residuals)
        for relation in self.data["relations"]:
            report(relation["role"] + " " + relation["id"], [
                self.character_expression(relation["lhs"], r)-self.character_expression(relation["rhs"], r)
                for r in self.characters])
        # Full 5x5 determinant of the stored character/basis matrix. A nonzero
        # determinant makes these five characters faithful on the proposed span.
        basis = self.data["basis_order"]
        determinant = self.field.zero
        for perm in permutations(range(len(basis))):
            inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i+1, len(perm)))
            determinant += (-1)**inversions * reduce(lambda a, b: a*b,
                (self.characters[i][basis[j]] for i, j in enumerate(perm)), self.field.one)
        if not determinant:
            failures.append("character basis rank")
        print(f"JSON character basis rank 5: {'PASS' if determinant else 'FAIL'}")
        if failures:
            raise Invalid("exact JSON audit failures: " + ", ".join(failures))
        print("JSON exact audit: all current local assertions PASS; no historical formulas used as definitions.")
