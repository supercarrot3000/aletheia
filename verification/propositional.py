"""Small exhaustive propositional checker; no eval and no external dependency."""
from itertools import product


def variables(expr):
    if not isinstance(expr, list) or not expr:
        raise ValueError("invalid expression")
    op, *args = expr
    if op == 'var' and len(args) == 1 and isinstance(args[0], str) and args[0]:
        return {args[0]}
    if (op == 'not' and len(args) == 1) or (op == 'implies' and len(args) == 2) or (op == 'and' and len(args) >= 2):
        return set().union(*(variables(a) for a in args))
    raise ValueError(f"unsupported expression: {expr!r}")


def evaluate(expr, assignment):
    op, *args = expr
    if op == 'var': return assignment[args[0]]
    if op == 'not': return not evaluate(args[0], assignment)
    if op == 'and': return all(evaluate(a, assignment) for a in args)
    if op == 'implies': return not evaluate(args[0], assignment) or evaluate(args[1], assignment)
    raise ValueError(op)


def check(premises, conclusion):
    names = sorted(set().union(*(variables(e) for e in [*premises, conclusion])))
    if len(names) > 16:
        return {'status': 'unknown', 'reason': 'variable bound exceeded'}
    has_model = False
    for values in product((False, True), repeat=len(names)):
        assignment = dict(zip(names, values))
        if all(evaluate(e, assignment) for e in premises):
            has_model = True
            if not evaluate(conclusion, assignment):
                return {'status': 'countermodel', 'witness': assignment}
    return {'status': 'entailed' if has_model else 'inconsistent_premises'}
