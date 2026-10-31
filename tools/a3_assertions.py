"""CAS-neutral resolution of explicit local references and spectral expansion.

No mathematical coefficients or relations are defined here: these functions
only manipulate the structured inputs, preserving operator word order.
"""
from copy import deepcopy
from itertools import combinations


def spectral_expansion(operator, roots):
    terms = []
    for k in range(len(roots)+1):
        coefficient = "1" if k == 0 else "+".join(
            "*".join("("+r+")" for r in subset) for subset in combinations(roots, k))
        if k:
            coefficient = ("" if k % 2 == 0 else "-") + "(" + coefficient + ")"
        terms.append({"coefficient": coefficient, "word": [operator]*(len(roots)-k)})
    return {"terms": terms}


def resolve_local(assertion, algebra, local):
    """Only named relation or named table cell; no executable templates."""
    ref = assertion["ref"]
    if "relation" in ref:
        original = next(r for r in local["relations"] if r["id"] == ref["relation"])
        sides = {side: original[side] for side in ("lhs", "rhs")}
    else:
        table = local["tables"][ref["table"]]
        sides = {
            "lhs": {"terms": [{"coefficient": "1", "word": [ref["left"], ref["right"]]}]},
            "rhs": table["cells"][table["row_order"].index(ref["left"])][table["column_order"].index(ref["right"])]}
    binding = next(b["operators"] for b in algebra["local_bindings"] if b["position"] == assertion["position"])

    def word(names):
        result = []
        for name in names:
            definition = local["elements"][name]
            if "word" in definition:  # Validated identity/square aliases only.
                result.extend(word(definition["word"]))
            else:
                result.append(binding[name])
        return result

    result = {k: deepcopy(v) for k, v in assertion.items() if k not in ("ref", "position")}
    for side, expression in sides.items():
        result[side] = {"terms": [dict(t, word=word(t["word"])) for t in expression["terms"]]}
    return result


def all_resolved(algebra, local):
    return [resolve_local(r, algebra, local) for r in algebra["local_assertions"]] + algebra["relations"]


def diagnostic_relation(diagnostic, algebra):
    result = deepcopy(next(r for r in algebra["relations"] if r["id"] == diagnostic["base_relation"]))
    # A separately printed preliminary display can survive a wholesale
    # replacement of the formal base relation. Keep its literal sides explicit.
    result.update(deepcopy(diagnostic.get("source_sides", {})))
    result["id"] = diagnostic["id"]
    for change in diagnostic["rhs_coefficient_multipliers"]:
        term = result["rhs"]["terms"][change["term"]]
        term["coefficient"] = f'({change["factor"]})*({term["coefficient"]})'
    if diagnostic.get('reverse_words', False):
        for side in ('lhs','rhs'):
            for term in result[side]['terms']:
                term['word'].reverse()
    return result
