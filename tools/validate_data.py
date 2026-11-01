#!/usr/bin/env python3
"""Draft-07/grammar validation plus exact sparse-entry zero checks; see FORMAT.md."""

import argparse
import copy
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from jsonschema import Draft7Validator, SchemaError, RefResolver

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"[0-9]+|[A-Za-z][A-Za-z0-9_]*|[()+*/^\-]")
IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_]*\Z")


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads(text):
    def bad_constant(value):
        raise Invalid(f"non-JSON constant: {value}")
    return json.loads(text, object_pairs_hook=unique_keys,
                      parse_constant=bad_constant, parse_float=bad_constant)


class Parser:
    """Small recursive-descent parser. No eval, sympify or code execution."""

    def __init__(self, text):
        require(isinstance(text, str) and text.strip(), "empty scalar expression")
        self.tokens = []
        pos = 0
        while pos < len(text):
            if text[pos] in " \t\r\n":
                pos += 1
                continue
            match = TOKEN.match(text, pos)
            require(match is not None, f"invalid scalar token at {pos}: {text!r}")
            self.tokens.append(match.group())
            pos = match.end()
        self.tokens.append("")
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def take(self):
        value = self.peek()
        self.pos += 1
        return value

    def expression(self):
        node = self.product()
        while self.peek() in ("+", "-"):
            node = (self.take(), node, self.product())
        return node

    def product(self):
        node = self.unary()
        while self.peek() in ("*", "/"):
            node = (self.take(), node, self.unary())
        return node

    def unary(self):
        if self.peek() == "-":
            self.take()
            return ("neg", self.unary())
        return self.power()

    def power(self):
        token = self.take()
        if token == "(":
            node = self.expression()
            require(self.take() == ")", "missing closing parenthesis")
        elif token.isascii() and token.isdigit():
            require(token == "0" or not token.startswith("0"), "leading-zero integer")
            node = ("int", int(token))
        elif IDENTIFIER.fullmatch(token):
            node = ("id", token)
        else:
            raise Invalid(f"expected integer, identifier or parenthesis; got {token!r}")
        if self.peek() == "^":
            self.take()
            wrapped = self.peek() == "("
            if wrapped:
                self.take()
            sign = -1 if self.peek() == "-" else 1
            if sign == -1:
                self.take()
            exponent = self.take()
            require(exponent.isascii() and exponent.isdigit(), "power requires a literal integer")
            require(exponent == "0" or not exponent.startswith("0"), "leading-zero exponent")
            if wrapped:
                require(self.take() == ")", "malformed exponent")
            node = ("pow", node, sign * int(exponent))
        return node


def parse_scalar(text):
    try:
        parser = Parser(text)
        tree = parser.expression()
        require(parser.peek() == "", f"unexpected scalar token {parser.peek()!r}")
        return tree
    except (IndexError, RecursionError) as exc:
        raise Invalid("incomplete or excessively nested scalar expression") from exc


def identifiers(tree):
    if tree[0] == "id":
        return {tree[1]}
    if tree[0] == "int":
        return set()
    children = tree[1:2] if tree[0] in ("neg", "pow") else tree[1:]
    return set().union(*(identifiers(child) for child in children))


def scalar(text, names):
    tree = parse_scalar(text)
    unknown = identifiers(tree) - set(names)
    require(not unknown, f"undeclared scalar identifiers: {sorted(unknown)}")
    return tree


def coefficient_order(data):
    definitions = data["coefficients"]
    variables = set(data["field"]["variables"])
    require(all(IDENTIFIER.fullmatch(n) for n in definitions), "invalid coefficient identifier")
    require(not (set(definitions) & variables), "coefficient shadows field variable")
    dependencies = {}
    for name, definition in definitions.items():
        tree = scalar(definition["expression"], variables | set(definitions))
        dependencies[name] = identifiers(tree) - variables
        if "bar_of" in definition:
            require(definition["bar_of"] in definitions, f"unknown bar_of at {name}")
    result, active, done = [], set(), set()

    def visit(name):
        require(name not in active, f"cyclic coefficient dependency at {name}")
        if name in done:
            return
        active.add(name)
        for dep in sorted(dependencies[name]):
            visit(dep)
        active.remove(name)
        done.add(name)
        result.append(name)

    for name in definitions:
        visit(name)
    return result


def validate_linear(expression, operators, scalars):
    words = set()
    for term in expression["terms"]:
        word = tuple(term["word"])
        require(set(word) <= set(operators), f"unknown operator in word: {word}")
        require("one" not in word, "use empty word for identity, not 'one'")
        require(word not in words, f"repeated word: {word}")
        words.add(word)
        tree = scalar(term["coefficient"], scalars)
        while tree[0] == "neg":
            tree = tree[1]
        require(tree != ("int", 0), "zero term: use an empty terms array instead")


def semantic_validate(data):
    coefficient_order(data)
    elements = data["elements"]
    require(all(IDENTIFIER.fullmatch(n) for n in elements), "invalid element identifier")
    scalars = set(data["coefficients"]) | set(data["field"]["variables"])
    require(not set(elements) & scalars, "scalar and element namespaces overlap")
    basis, extra = data["basis_order"], data["additional_order"]
    require(len(set(basis + extra)) == len(basis + extra), "duplicate element identifier")
    require(set(basis + extra) == set(elements), "element orders do not cover declarations")
    for name, declaration in elements.items():
        require(declaration["kind"] == ("basis" if name in basis else "additional"), f"wrong kind: {name}")
        if "word" in declaration:
            expected = {"one": [], "H2": ["H", "H"]}
            require(name in expected and declaration["word"] == expected[name], f"unsupported element definition: {name}")
    require(elements["one"].get("word") == [], "missing identity definition")
    require(elements["H2"].get("word") == ["H", "H"], "missing square definition")
    relation_ids = [r["id"] for r in data["relations"]]
    require(all(IDENTIFIER.fullmatch(n) for n in relation_ids), "invalid relation identifier")
    require(len(set(relation_ids)) == len(relation_ids), "duplicate relation identifier")
    roles = {"cubic": "primary", "skein": "primary", "inverse_right": "primary", "inverse_left": "primary", "S_polynomial": "primary", "Sinv_polynomial": "primary", "reduce_H3": "derived", "reduce_H4": "derived", "jacobi_commute_S": "derived", "jacobi_commute_Sinv": "derived", "jacobi_S": "derived", "jacobi_Sinv": "derived"}
    by_id = {r["id"]: r for r in data["relations"]}
    for name, role in roles.items():
        require(name in by_id and by_id[name]["role"] == role, f"missing or misclassified relation {name}")
    for relation in data["relations"]:
        for side in ("lhs", "rhs"):
            validate_linear(relation[side], elements, scalars)
    for name, table in data["tables"].items():
        order = basis if name == "completed" else ["U", "K", "H"]
        require(table["row_order"] == table["column_order"] == order, f"{name}: wrong table orders")
        require(len(table["cells"]) == len(order), f"{name}: missing table row")
        for row in table["cells"]:
            require(len(row) == len(order), f"{name}: missing table cell")
            for cell in row:
                validate_linear(cell, elements, scalars)
        for ref in table.get("reduction_rules", []):
            require(ref in by_id, f"unknown reduction: {ref}")
    require(data["tables"]["completed"]["reduction_rules"] == ["reduce_H4", "reduce_H3"], "unsupported reduction order")
    for power in (3, 4):
        rule = by_id[f"reduce_H{power}"]
        require(rule["lhs"] == {"terms": [{"coefficient": "1", "word": ["H"]*power}]}, "malformed reduction pattern")
        require(all(t["word"] == [] or (len(t["word"]) == 1 and t["word"][0] in basis[1:]) for t in rule["rhs"]["terms"]), "reduction does not land in basis")
    characters = data["characters"]
    require(characters["column_order"] == basis + extra, "character columns differ from declared order")
    require(set(characters["column_provenance"]) == set(characters["column_order"]), "incomplete column provenance")
    require([r["id"] for r in characters["rows"]] == characters["row_order"], "character rows missing, duplicated or reordered")
    for row in characters["rows"]:
        require(len(row["values"]) == len(characters["column_order"]), "incorrect character row size")
        for value in row["values"]:
            scalar(value, scalars)
    check_ids = [c["id"] for c in data["scalar_checks"]]
    require(all(IDENTIFIER.fullmatch(n) for n in check_ids), "invalid scalar-check identifier")
    require(len(check_ids) == len(set(check_ids)), "duplicate scalar-check identifier")
    require({"tau_bracket", "tau_laurent", "tau_ratio", "tau_intermediate", "aI_simplified", "phi_laurent", "source_z", "source_w", "S_K_alternative"} <= set(check_ids), "missing current coefficient comparison")
    for check in data["scalar_checks"]:
        scalar(check["lhs"], scalars)
        scalar(check["rhs"], scalars)
    require('square_square' in data and 'coefficient_evidence' in data, 'missing local square-square specification')
    spec = data['square_square']
    require(spec['relation_ref'] in by_id, 'unknown square-square relation')
    relation = by_id[spec['relation_ref']]
    require(relation['role'] == 'primary' and relation['lhs'] == {'terms': [{'coefficient':'1','word':['H']*3}]}, 'square-square lhs/role')
    expected = [{'coefficient': n, 'word': [] if b == 'one' else [b]}
                for b,n in zip(basis,spec['coefficient_order'])]
    require(relation['rhs'] == {'terms': expected}, 'square-square coefficient/basis correspondence')
    scalar(spec['determinant'], scalars)
    evidence_ids = [e['id'] for e in data['coefficient_evidence']]
    require(len(set(evidence_ids)) == len(evidence_ids), 'duplicate coefficient evidence id')
    require(set(evidence_ids) == {f'b_{i}_{form}' for i in range(5) for form in ('bracket','eigenvalue')}, 'incomplete printed b formula inventory')
    for e in data['coefficient_evidence']:
        require(e['coefficient'] in spec['coefficient_order'], 'unknown local evidence coefficient')
        scalar(e['expression'], scalars)
        scalar(e['residual'], scalars)


SCHEMAS = {
    "exceptional-series-local-a2": "local_a2.schema.json",
    "exceptional-series-a3": "a3.schema.json",
    "exceptional-series-representation": "representation.schema.json",
}

# Required release collection, from the author's inventory and lem:A3toprep /
# lem:A3rep. This is a structural dimension contract, not matrix input.
REPRESENTATIONS = {"I": 1, "L": 5, "X2": 4, "Y2": 3, "Y2_star": 3,
                   "X3": 1, "Y3": 1, "Y3_star": 1, "A": 3, "C": 2, "C_star": 2}


def validate_collection(records, *, complete=True):
    ids = [r["id"] for r in records]
    require(len(ids) == len(set(ids)), "duplicate representation identifier")
    require(set(ids) <= set(REPRESENTATIONS), "unknown representation identifier")
    for record in records:
        require(record["dimension"] == REPRESENTATIONS[record["id"]],
                "wrong expected representation dimension: " + record["id"])
    if complete:
        require(set(ids) == set(REPRESENTATIONS),
                "incomplete representation collection; missing: " + ", ".join(sorted(set(REPRESENTATIONS)-set(ids))))
        require(sum(r["dimension"]**2 for r in records) == 80, "incorrect total squared dimension")


def collection_self_test():
    complete = [{"id": n, "dimension": d} for n, d in REPRESENTATIONS.items()]
    validate_collection(complete)
    cases = [
        ("missing representation", lambda d: d.pop()),
        ("duplicate representation", lambda d: d.append(copy.deepcopy(d[0]))),
        ("wrong expected dimension", lambda d: d[0].update(dimension=2)),
        ("incorrect total squared dimension", lambda d: d[1].update(dimension=4)),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(complete)
        mutate(changed)
        try:
            validate_collection(changed)
        except Invalid:
            print(f"negative {name} rejected: PASS")
        else:
            raise Invalid("accepted invalid collection: " + name)


def schema_validator(schema, filename):
    # Restrict all resolution to these reviewed, local schemas. Never fetch.
    store = {(ROOT / "schema" / name).as_uri(): loads((ROOT / "schema" / name).read_text())
             for name in SCHEMAS.values()}

    def blocked(uri):
        raise Invalid(f"nonlocal schema reference: {uri}")

    resolver = RefResolver((ROOT / "schema" / filename).as_uri(), schema,
                           store=store, handlers={"http": blocked, "https": blocked, "file": blocked})
    return Draft7Validator(schema, resolver=resolver)


def algebra_context(algebra):
    local = load_validated(ROOT / "data" / algebra["local_ref"])
    require(algebra["version"] == local["version"], "inconsistent format versions")
    require(algebra["field_ref"] == local["field"]["id"], "unknown field reference")
    require(not set(algebra["coefficients"]) & (set(local["coefficients"]) | set(local["field"]["variables"])),
            "algebra coefficient shadows an imported coefficient")
    require(algebra['coefficient_imports']['source'] == algebra['local_ref'], 'coefficient owner mismatch')
    require(set(algebra['coefficient_imports']['required']) <= set(local['coefficients']), 'missing owned local coefficient')
    combined = dict(local, coefficients={**local["coefficients"], **algebra["coefficients"]})
    coefficient_order(combined)
    return local, set(combined["coefficients"]) | set(local["field"]["variables"])


def validate_relations(relations, operators, scalars):
    ids = [r["id"] for r in relations]
    require(len(ids) == len(set(ids)), "duplicate relation identifier")
    for relation in relations:
        for side in ("lhs", "rhs"):
            validate_linear(relation[side], operators, scalars)


def validate_algebra(data):
    local, scalars = algebra_context(data)
    require(not set(local["elements"]) & scalars, "local operator/scalar namespace collision")
    require(set(data["operators"]) == set(data["operator_order"]), "operator declarations incomplete")
    require(not set(data["operators"]) & scalars, "operator/scalar namespace collision")
    for name, declaration in data["operators"].items():
        require(name == declaration["local_operator"] + str(declaration["position"]), "incorrect indexed operator declaration")
    require([b["position"] for b in data["local_bindings"]] == [1, 2], "incorrect local binding positions")
    for binding in data["local_bindings"]:
        require(binding["operators"] == {n: n+str(binding["position"]) for n in ("H", "K", "U", "S", "Sinv")}, "incorrect local substitution")
    validate_relations(data["relations"], data["operators"], scalars)
    validate_assertion_set(data, local, scalars)
    validate_relations(data["polynomial_prescriptions"], local["elements"], scalars)
    require([r["id"] for r in data["polynomial_prescriptions"]] == ["K_from_H", "U_from_H"], "missing polynomial prescription")
    require(all(r["role"] == "derived" for r in data["polynomial_prescriptions"]), "polynomial consistency role")
    ids, paths = [], []
    for rep in data["representations"]:
        require(rep["id"] in REPRESENTATIONS, "unknown registered representation identifier")
        require(rep["path"] == f'representations/{rep["id"]}.json', "representation path/id mismatch")
        require((ROOT / "data" / rep["path"]).is_file(), "missing registered representation file")
        ids.append(rep["id"])
        paths.append(rep["path"])
    require(len(ids) == len(set(ids)) and len(paths) == len(set(paths)), "duplicate representation registry entry")


def validate_assertion_set(data, local, scalars):
    from a3_assertions import all_resolved, spectral_expansion
    groups = ("relations", "local_assertions", "polynomial_prescriptions", "coefficient_checks",
              "unavailable_assertions", "diagnostics", "quotient_comparisons")
    ids = [r["id"] for group in groups for r in data[group]]
    require(len(ids) == len(set(ids)), "duplicate assertion identifier across groups")
    local_ids = {r["id"] for r in local["relations"]}
    for assertion in data["local_assertions"]:
        ref = assertion["ref"]
        if "relation" in ref:
            require(ref["relation"] in local_ids, "broken local relation reference")
            expected_id = ref["relation"] + str(assertion["position"])
            expected_kind = "defining" if ref["relation"] == "cubic" else "additional_braid"
            require(ref["relation"] in {"cubic", "inverse_left", "inverse_right", "S_polynomial", "Sinv_polynomial"}, "unsupported local presentation reference")
        else:
            table = local["tables"][ref["table"]]
            require(ref["left"] in table["row_order"] and ref["right"] in table["column_order"], "broken local table reference")
            expected_id = ref["left"] + ref["right"] + str(assertion["position"])
            expected_kind = "defining"
        require(assertion["id"] == expected_id and assertion["kind"] == expected_kind,
                "misidentified or misclassified local assertion")
    resolved = all_resolved(data, local)
    validate_relations(resolved, data["operators"], scalars)
    by_id = {r["id"]: r for r in resolved}
    required = {"HKH", "quartic_full"}
    required |= {n+str(i) for n in ("HK", "KH", "HU", "UH", "KK", "KU", "UK", "UU", "cubic", "KUK", "KUH", "KUU", "UUK", "UUU") for i in (1, 2)}
    defining = {r["id"] for r in resolved if r["kind"] == "defining"}
    require(defining == required == set(data["defining_relation_ids"]), "incomplete or contaminated full defining-relation set")
    additional = {"braid"} | {n+str(i) for n in ("S_quintic", "inverse_left", "inverse_right", "S_polynomial", "Sinv_polynomial") for i in (1, 2)}
    require(additional == {r["id"] for r in resolved if r["kind"] == "additional_braid"}, "incomplete additional braid set")
    quotient = {"top_cubic1", "top_cubic2", "top_quartic_a", "top_quartic_aa", "top_quartic_b"}
    require(quotient == {r["id"] for r in resolved if r["kind"] == "quotient_only"}, "incorrect quotient assertion inventory")
    for r in resolved + data["polynomial_prescriptions"]:
        require((r["scope"] == "top_quotient") == (r["kind"] == "quotient_only"), "quotient/full assertion scope mismatch")
        if r["kind"] == "defining":
            require(r["role"] == "primary", "defining relation must be primary")
        if "spectral" in r:
            spec = r["spectral"]
            require(spec["operator"] in data["operators"], "unknown spectral operator")
            for root in spec["roots"]:
                scalar(root, scalars)
            require(r["lhs"] == spectral_expansion(spec["operator"], spec["roots"]) and r["rhs"] == {"terms": []}, "spectral polynomial expansion mismatch")
    require({q["id"] for q in data["quotients"]} == {"top_quotient"} and len(data["quotients"]) == 1, "quotient declarations")
    require(data["quotients"][0]["zero_operators"] == ["K1", "K2", "U1", "U2"], "incorrect top quotient conditions")
    for c in data["coefficient_checks"]:
        for side in ("lhs", "rhs", "residual"):
            scalar(c[side], scalars)
        require((c["expectation"] == "not_equal") == (c["status"] == "unresolved"), "coefficient comparison status mismatch")
    scalar(data['audit_history']['first_residual'][2], scalars)
    for diagnostic in data["diagnostics"]:
        require(diagnostic["base_relation"] in by_id, "unknown diagnostic base relation")
        if "source_sides" in diagnostic:
            require(not diagnostic["rhs_coefficient_multipliers"] and not diagnostic.get("reverse_words", False),
                    "literal diagnostic sides cannot also be transformed")
            for side in ("lhs", "rhs"):
                validate_linear(diagnostic["source_sides"][side], data["operators"], scalars)
        require(set(diagnostic["coefficient_overrides"]) <= scalars - {'p','q'}, "unknown diagnostic coefficient override")
        for expression in diagnostic["coefficient_overrides"].values():
            scalar(expression, scalars)
        positions = []
        for change in diagnostic["rhs_coefficient_multipliers"]:
            require(change["term"] < len(by_id[diagnostic["base_relation"]]["rhs"]["terms"]), "diagnostic term index out of range")
            scalar(change["factor"], scalars)
            positions.append(change["term"])
        require(len(positions) == len(set(positions)), "duplicate diagnostic term index")
    require(any(r["id"] == "braid_degree_seven" and r["degree"] == 7 for r in data["unavailable_assertions"]), "missing braid-presentation limitation")
    diagnostic_bases = {d['id']:by_id[d['base_relation']] for d in data['diagnostics']}
    comparison_relations = dict(by_id, **diagnostic_bases)
    for c in data['quotient_comparisons']:
        require(c['full_relation'] in by_id and by_id[c['full_relation']]['scope']=='full_a3', 'invalid full comparison relation')
        require(all(n in comparison_relations and comparison_relations[n]['scope']==c['quotient'] for n in c['summands']), 'invalid quotient summand')

    def sources(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "source" and isinstance(item, list):
                    require(all(re.match(r"^Paper, (?:Section [0-9]+(?:\.[0-9]+)*|Appendix)\b", s) for s in item), "malformed public paper reference")
                else:
                    sources(item)
        elif isinstance(value, list):
            for item in value:
                sources(item)
    sources(data)


def algebra_self_test(data, schema):
    def term(d):
        return d["relations"][0]["lhs"]["terms"][0]

    def promote_quotient(d):
        r = next(r for r in d["relations"] if r["kind"] == "quotient_only")
        r.update(kind="defining", scope="full_a3")
        d["defining_relation_ids"].append(r["id"])

    def preliminary(d):
        return next(x for x in d["diagnostics"] if x["id"] == "top_preliminary_b")

    cases = [
        ("duplicate assertion identifier", lambda d: d["relations"].append(copy.deepcopy(d["relations"][0]))),
        ("unknown algebra coefficient", lambda d: term(d).update(coefficient="missing_coefficient")),
        ("unknown algebra operator", lambda d: term(d)["word"].append("missing_operator")),
        ("malformed word", lambda d: term(d).update(word="S1 S2 S1")),
        ("cyclic algebra coefficient", lambda d: d["coefficients"]["c_0"].update(expression="c_0")),
        ("conflicting coefficient ownership", lambda d: d['coefficients'].update(b_3={'expression':'e2','origin':'computed','source':['Paper, Appendix']})),
        ("invalid assertion role", lambda d: d["relations"][0].update(role="defining")),
        ("invalid assertion scope", lambda d: d["relations"][0].update(scope="all_algebras")),
        ("broken substitution", lambda d: d["local_bindings"][0]["operators"].update(H="H3")),
        ("quotient promoted to full presentation", promote_quotient),
        ("missing defining relation", lambda d: d["relations"].remove(next(r for r in d["relations"] if r["id"] == "quartic_full"))),
        ("broken local cell reference", lambda d: d["local_assertions"][0]["ref"].update(left="S")),
        ("malformed source reference", lambda d: d["relations"][0].update(source=["unlocated"])),
        ("incorrect spectral expansion", lambda d: next(r for r in d["relations"] if "spectral" in r)["spectral"]["roots"].__setitem__(3,"p^6")),
        ("unknown literal diagnostic operator", lambda d: preliminary(d)["source_sides"]["lhs"]["terms"][0]["word"].append("unknown")),
        ("transformed literal diagnostic", lambda d: preliminary(d).update(reverse_words=True)),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(data)
        mutate(changed)
        try:
            validate(changed, schema)
        except Invalid:
            print(f"negative {name} rejected: PASS")
        else:
            raise Invalid(f"negative test accepted invalid data: {name}")


def validate_representation(data):
    algebra = load_validated(ROOT / "data/a3.json")
    local, scalars = algebra_context(algebra)
    require(data["version"] == algebra["version"], "inconsistent format versions")
    require(data["field_ref"] == algebra["field_ref"], "unknown representation field")
    require(data["id"] in {r["id"] for r in algebra["representations"]}, "unregistered representation")
    n = data["dimension"]
    validate_collection([data], complete=False)
    if "cut_length" in data:
        expected_cut = 0 if data["id"] == "I" else 1 if data["id"] == "L" else 2 if data["id"] in {"X2", "Y2", "Y2_star"} else 3
        require(data["cut_length"] == expected_cut, "incorrect representation cut length")
    require(len(data["basis"]["order"]) == n, "basis length differs from dimension")
    require(len(set(data["basis"]["order"])) == n, "duplicate basis coordinate")
    names = [m["operator"] for m in data["matrices"]]
    require(len(set(names)) == len(names), "duplicate matrix operator")
    require(names == algebra["operator_order"], "missing, unknown or reordered matrix operator")
    for matrix in data["matrices"]:
        if matrix["provenance"].get("method") == "zero":
            require(matrix["operator"] in {"K1", "K2", "U1", "U2"}, "unsupported prescribed zero operator")
            require(matrix["entries"] == [], "prescribed zero matrix contains entries")
        require(matrix["rows"] == matrix["cols"] == n, "matrix dimensions disagree with representation")
        positions = []
        for i, j, expression in matrix["entries"]:
            require(0 <= i < n and 0 <= j < n, "matrix index out of range")
            positions.append((i, j))
            scalar(expression, scalars)
        require(len(set(positions)) == len(positions), "duplicate matrix position")
        require(positions == sorted(positions), "entries must be in row-major order")
    expected = {("rotation", n+"2", n+"1") for n in ("H", "K", "U", "S", "Sinv")}
    expected |= {("bar", "Sinv"+str(i), "S"+str(i)) for i in (1, 2)}
    checks = data["construction_checks"]
    require(len({c["id"] for c in checks}) == len(checks), "duplicate construction check id")
    require({(c["kind"], c["target"], c["operand"]) for c in checks} == expected, "incomplete or unknown construction checks")
    # This one semantic invariant needs field arithmetic, isolated in the
    # experimental consumer. Grammar/structural validation still uses no CAS.
    from exact_a2 import ExactA2
    exact = ExactA2(data=local)
    exact.extend_coefficients(algebra["coefficients"])
    for matrix in data["matrices"]:
        for i, j, expression in matrix["entries"]:
            require(bool(exact.scalar(expression)), f'explicit zero entry in {matrix["operator"]} at ({i},{j})')


def validate(data, schema):
    filename = SCHEMAS.get(data.get("format"))
    require(filename is not None, "unknown data format")
    errors = sorted(schema_validator(schema, filename).iter_errors(data), key=lambda e: str(list(e.path)))
    if errors:
        error = errors[0]
        raise Invalid(f"schema at /{'/'.join(map(str, error.path))}: {error.message}")
    {"exceptional-series-local-a2": semantic_validate,
     "exceptional-series-a3": validate_algebra,
     "exceptional-series-representation": validate_representation}[data["format"]](data)


def load_validated(path=None):
    path = Path(path) if path else ROOT / "data/local_a2.json"
    data = loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "data root must be a JSON object")
    require(isinstance(data.get("$schema"), str), "missing or non-string schema declaration")
    schema_path = (path.parent / data.get("$schema", "")).resolve()
    filename = SCHEMAS.get(data.get("format"))
    require(filename is not None and schema_path == ROOT / "schema" / filename,
            "unsupported declared schema (local only)")
    schema = loads(schema_path.read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)
    validate(data, schema)
    if data["format"] == "exceptional-series-representation":
        require(path.resolve() == ROOT / "data/representations" / (data["id"] + ".json"), "representation filename/id mismatch")
    return data


def representation_self_test(data, schema):
    def entry(d):
        return d["matrices"][0]["entries"][0]

    cases = [
        ("duplicate matrix position", lambda d: d["matrices"][0]["entries"].append(copy.deepcopy(entry(d)))),
        ("out-of-range matrix position", lambda d: entry(d).__setitem__(0, d["dimension"])),
        ("explicit zero matrix entry", lambda d: entry(d).__setitem__(2, "0")),
        ("cancelled zero matrix entry", lambda d: entry(d).__setitem__(2, "p-p")),
        ("wrong matrix dimensions", lambda d: d["matrices"][0].update(rows=d["dimension"]+1)),
        ("missing required operator", lambda d: d["matrices"].pop()),
        ("duplicate matrix operator", lambda d: d["matrices"][1].update(operator="H1")),
        ("malformed matrix coefficient", lambda d: entry(d).__setitem__(2, "2p")),
        ("undeclared matrix coefficient", lambda d: entry(d).__setitem__(2, "not_declared")),
        ("incorrect representation basis size", lambda d: d["basis"]["order"].pop()),
        ("duplicate representation basis", lambda d: d["basis"]["order"].append(d["basis"]["order"][0])),
        ("invalid provenance category", lambda d: d["matrices"][0]["provenance"].update(origin="independently_checked")),
        ("unknown construction operator", lambda d: d["construction_checks"][0].update(target="unknown")),
        ("incorrect action convention", lambda d: d["conventions"].update(action="unspecified")),
        ("bad algebra reference", lambda d: d.update(algebra_ref="../missing.json")),
        ("cross-file identifier mismatch", lambda d: d.update(id="unregistered")),
        ("missing zero operator", lambda d: d["matrices"].__delitem__(4)),
        ("invalid source method", lambda d: d["matrices"][2]["provenance"].update(method="guessed")),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(data)
        mutate(changed)
        try:
            validate(changed, schema)
        except Invalid:
            print(f"negative {name} rejected: PASS")
        else:
            raise Invalid(f"negative test accepted invalid data: {name}")


def self_test(data, schema):
    cases = [
        ("undeclared coefficient", lambda d: d["coefficients"]["tau"].update(expression="missing")),
        ("cyclic dependency", lambda d: d["coefficients"]["delta"].update(expression="tau")),
        ("missing table cell", lambda d: d["tables"]["completed"]["cells"][0].pop()),
        ("duplicate basis identifier", lambda d: d["basis_order"].__setitem__(1, "one")),
        ("unknown word operator", lambda d: d["relations"][0]["lhs"]["terms"][0]["word"].append("unknown")),
        ("incorrect character row size", lambda d: d["characters"]["rows"][0]["values"].pop()),
        ("malformed scalar", lambda d: d["coefficients"]["tau"].update(expression="2p")),
        ("repeated word", lambda d: d["relations"][0]["lhs"]["terms"].append(copy.deepcopy(d["relations"][0]["lhs"]["terms"][0]))),
        ("zero term", lambda d: d["relations"][0]["lhs"]["terms"][0].update(coefficient="0")),
        ("unknown reduction", lambda d: d["tables"]["completed"]["reduction_rules"].append("missing")),
        ("missing primary identity", lambda d: d["relations"].pop(0)),
        ("duplicate character row", lambda d: d["characters"]["rows"][1].update(id="Y2")),
    ]
    for name, mutate in cases:
        changed = copy.deepcopy(data)
        mutate(changed)
        try:
            validate(changed, schema)
        except Invalid:
            print(f"negative {name} rejected: PASS")
        else:
            raise Invalid(f"negative test accepted invalid data: {name}")
    try:
        loads('{"nested":{"x":1,"x":2}}')
    except Invalid:
        print("negative duplicate JSON key rejected: PASS")
    else:
        raise Invalid("accepted duplicate JSON key")
    for malformed in ("p**2", "p^q", "p^2^3", "p(1)", "1.0", "1e3", "p//q", "__import__('os')", "", "p+"):
        try:
            scalar(malformed, {"p", "q"})
        except Invalid:
            continue
        raise Invalid(f"accepted invalid syntax: {malformed}")
    require(parse_scalar("-p^2") == ("neg", ("pow", ("id", "p"), 2)), "unary precedence")
    require(parse_scalar("p^(-2)") == parse_scalar("p^-2"), "signed power grammar")
    # Independent two-position format fixture: validate ordered braid words,
    # never a claim that this local character audit proves the A(3) braid.
    example = {"id": "braid", "role": "primary", "origin": "copied", "source": ["Paper, Section 6"],
               "lhs": {"terms": [{"coefficient": "1", "word": ["S1", "S2", "S1"]}]},
               "rhs": {"terms": [{"coefficient": "1", "word": ["S2", "S1", "S2"]}]}}
    Draft7Validator({"$ref": "#/definitions/relation", "definitions": schema["definitions"]}).validate(example)
    for side in ("lhs", "rhs"):
        validate_linear(example[side], {"S1", "S2"}, {"p", "q"})
    require(example["lhs"] != example["rhs"], "word order was lost")
    print("grammar and ordered two-position relation fixture: PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--allow-incomplete", action="store_true", help="incremental validation; explicitly waive only the eleven-file completeness gate")
    args = parser.parse_args()
    try:
        paths = sorted((ROOT / "data").rglob("*.json"))
        require(bool(paths), "no JSON data files")
        records = []
        for path in paths:
            data = load_validated(path)
            if data["format"] == "exceptional-series-representation":
                records.append(data)
            print(f"{path.relative_to(ROOT)} schema, references, dimensions, scalar grammar: PASS")
            if args.self_test:
                schema = loads((ROOT / "schema" / SCHEMAS[data["format"]]).read_text())
                if data["format"] == "exceptional-series-local-a2":
                    self_test(data, schema)
                elif data["format"] == "exceptional-series-representation":
                    representation_self_test(data, schema)
                elif data["format"] == "exceptional-series-a3":
                    algebra_self_test(data, schema)
        if args.self_test:
            collection_self_test()
        algebra = load_validated(ROOT / "data/a3.json")
        require({r["id"] for r in records} == {r["id"] for r in algebra["representations"]}, "representation files and registry differ")
        validate_collection(records, complete=not args.allow_incomplete)
        print(f"Representation collection: {len(records)}/11 files; squared dimension {sum(r['dimension']**2 for r in records)}/80" + (" (incremental mode)" if args.allow_incomplete else ": PASS"))
        print(f"Validated {len(paths)} data file(s); mathematical equality is not structural validation.")
        return 0
    except (Invalid, ValueError, OSError, RecursionError, SchemaError, ZeroDivisionError) as exc:
        print(f"validation: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
