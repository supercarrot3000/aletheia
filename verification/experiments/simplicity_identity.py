"""Replay the finite first-order experiment for INV-SIMPLICITY-IDENTITY."""

import json
import sys
from dataclasses import dataclass
from importlib.metadata import version
from itertools import product

try:
    import z3
except ImportError:
    if __name__ != "__main__":
        raise
    sys.exit("Install verification/experiments/requirements-z3.txt to run this experiment.")

PACKAGE_VERSION = "4.15.4.0"
TIMEOUT_MS = 5_000
DOMAIN_SIZES = (1, 2, 3)


@dataclass(frozen=True)
class Profile:
    name: str
    require_opposition: bool = True
    identify_relata: bool = False
    replace_first: bool = False
    replace_second: bool = False


PROFILES = (
    Profile("common-essence"),
    Profile("unrestricted-identity", identify_relata=True),
    Profile("replacement-first", replace_first=True),
    Profile("replacement-second", replace_second=True),
    Profile("control-without-opposed-pair", require_opposition=False,
            replace_first=True, replace_second=True),
)


def finite_names(size):
    return [f"R{n}" for n in range(size)], [f"E{n}" for n in range(size)]


def valid_witness(profile, size, witness):
    """Check a total finite interpretation without invoking Z3."""
    relata, labels = finite_names(size)
    essence = witness["essence_classes"]
    if set(essence) != set(relata) or not set(essence.values()) <= set(labels):
        return False
    paternity, filiation = witness["paternity"], witness["filiation"]
    if paternity not in essence or filiation not in essence or essence[paternity] != essence[filiation]:
        return False
    opposition = {tuple(pair) for pair in witness["opposition"]}
    if not opposition <= set(product(relata, repeat=2)):
        return False
    if any(x == y or (y, x) not in opposition for x, y in opposition):
        return False
    if profile.require_opposition and (paternity, filiation) not in opposition:
        return False
    if profile.identify_relata and paternity != filiation:
        return False
    for x, y, other in product(relata, repeat=3):
        if essence[x] != essence[y]:
            continue
        if profile.replace_first and ((x, other) in opposition) != ((y, other) in opposition):
            return False
        if profile.replace_second and ((other, x) in opposition) != ((other, y) in opposition):
            return False
    return True


def solve(profile, size):
    relatum_names, labels = finite_names(size)
    ctx = z3.Context()
    relatum, relata = z3.EnumSort("Relatum", relatum_names, ctx=ctx)
    essence_class, _ = z3.EnumSort("EssenceClass", labels, ctx=ctx)
    essence = z3.Function("essence", relatum, essence_class)
    opposition = z3.Function("opposition", relatum, relatum, z3.BoolSort(ctx))
    paternity, filiation = z3.Consts("paternity filiation", relatum)
    solver = z3.Solver(ctx=ctx)
    solver.set(timeout=TIMEOUT_MS)
    solver.add(essence(paternity) == essence(filiation))
    for x in relata:
        solver.add(z3.Not(opposition(x, x)))
    for x, y in product(relata, repeat=2):
        solver.add(opposition(x, y) == opposition(y, x))
    if profile.require_opposition:
        solver.add(opposition(paternity, filiation))
    if profile.identify_relata:
        solver.add(paternity == filiation)
    # Expand universal conditions over the entire finite enumeration.
    for x, y, other in product(relata, repeat=3):
        same_essence = essence(x) == essence(y)
        if profile.replace_first:
            solver.add(z3.Implies(same_essence, opposition(x, other) == opposition(y, other)))
        if profile.replace_second:
            solver.add(z3.Implies(same_essence, opposition(other, x) == opposition(other, y)))

    status = solver.check()
    result = {
        "profile": profile.name,
        "domain_size": size,
        "essence_label_bound": size,
        "status": str(status),
        "smtlib": f"(set-option :timeout {TIMEOUT_MS})\n" + solver.to_smt2(),
    }
    if status == z3.sat:
        model = solver.model()
        witness = {
            "paternity": str(model.eval(paternity, model_completion=True)),
            "filiation": str(model.eval(filiation, model_completion=True)),
            "essence_classes": {
                str(x): str(model.eval(essence(x), model_completion=True)) for x in relata
            },
            "opposition": [
                [str(x), str(y)] for x, y in product(relata, repeat=2)
                if z3.is_true(model.eval(opposition(x, y), model_completion=True))
            ],
        }
        if not valid_witness(profile, size, witness):
            raise ValueError(f"{profile.name}/{size}: solver returned an invalid finite witness")
        result["witness"] = witness
    elif status == z3.unknown:
        result["reason"] = solver.reason_unknown()
    return result


def run():
    installed_version = version("z3-solver")
    native_version = z3.get_full_version()
    if installed_version != PACKAGE_VERSION or native_version.split(".")[:3] != PACKAGE_VERSION.split(".")[:3]:
        raise ValueError(f"Require z3-solver {PACKAGE_VERSION} with its matching native library")
    return {
        "version": 1,
        "investigation": "INV-SIMPLICITY-IDENTITY",
        "z3": {"package": installed_version, "native": native_version},
        "timeout_ms_per_case": TIMEOUT_MS,
        "cases": [solve(profile, size) for profile in PROFILES for size in DOMAIN_SIZES],
    }


def main():
    try:
        result = run()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if any(case["status"] == "unknown" for case in result["cases"]) else 0


if __name__ == "__main__":
    sys.exit(main())
