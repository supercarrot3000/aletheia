"""Independent local replay, using only the trusted verifier's executable files."""

import re
import subprocess
import tempfile
from pathlib import Path

from verification.corpus import Corpus, digest, strict_json
from verification.propositional import check, evaluate, variables


TOOLCHAIN = "lean-toolchain"
PROOF = "verification/lean/Bridge.lean"
POLICY = "verification/policy.json"
FIXTURES = "verification/fixtures/logic.json"


def verify_logic(premises, conclusion):
    result = check(premises, conclusion)
    if result["status"] == "unknown":
        raise ValueError(result["reason"])
    if result["status"] == "countermodel":
        witness = result["witness"]
        if not all(evaluate(premise, witness) for premise in premises) or evaluate(conclusion, witness):
            raise ValueError("invalid countermodel produced by checker")
    return result


def lean_formula(expr, names):
    op, *args = expr
    if op == "var":
        return names[args[0]]
    rendered = [lean_formula(arg, names) for arg in args]
    if op == "not":
        return f"(¬ {rendered[0]})"
    if op == "and":
        return "(" + " ∧ ".join(rendered) + ")"
    return "(" + " → ".join(rendered) + ")"


def check_bridge(root, assets, premises, conclusion):
    pin = assets[TOOLCHAIN].decode().strip()
    version = subprocess.run(["elan", "run", pin, "lean", "--version"], cwd=root,
                             check=True, capture_output=True, text=True, timeout=20).stdout.strip()
    expected = re.fullmatch(r"leanprover/lean4:v([0-9.]+)", pin)
    if expected is None or not version.startswith(f"Lean (version {expected[1]},"):
        raise ValueError(f"Lean version does not match {pin}: {version}")
    atoms = set().union(*(variables(expr) for expr in [*premises, conclusion]))
    # The trusted demonstration theorem takes these propositions in this order.
    if atoms != {"simple", "composite", "relational"}:
        raise ValueError("bridge proof requires the three simplicity atoms")
    names = {"simple": "p0", "composite": "p1", "relational": "p2"}
    statement = " → ".join(lean_formula(expr, names) for expr in [*premises, conclusion])
    proof = assets[PROOF].decode("utf-8") + (
        f"\ntheorem checkedStatement (p0 p1 p2 : Prop) : {statement} :=\n"
        "  simplicityBridge p0 p1 p2\n\n#print axioms checkedStatement\n"
    )
    with tempfile.TemporaryDirectory(prefix="aletheia-lean-") as temporary:
        path = Path(temporary) / "Certificate.lean"
        path.write_text(proof, encoding="utf-8")
        run = subprocess.run(["elan", "run", pin, "lean", str(path)], cwd=root,
                             check=True, capture_output=True, text=True, timeout=30)
    if run.stdout.splitlines() != [
        "'simplicityBridge' does not depend on any axioms",
        "'checkedStatement' does not depend on any axioms",
    ]:
        raise ValueError("Lean bridge axiom audit differs from the expected empty ledger")
    return {"toolchain": pin, "version": version, "theorem": "checkedStatement",
            "theorem_type": f"∀ (p0 p1 p2 : Prop), {statement}", "axioms": []}


def read_verifier_assets(root):
    paths = [
        "aletheia.py", "verification/corpus.py", "verification/propositional.py",
        "verification/replay.py", TOOLCHAIN, PROOF, POLICY, FIXTURES,
    ]
    return {path: (root / path).read_bytes() for path in paths}


def asset_manifest(assets):
    return {path: digest(content) for path, content in sorted(assets.items())}


def check_regressions(fixtures):
    results = {}
    for fixture in fixtures:
        result = verify_logic(fixture["premises"], fixture["conclusion"])
        if result["status"] != fixture["expected"]:
            raise ValueError(f"trusted regression failed: {fixture['id']}")
        results[fixture["id"]] = result
    return results


def verify(trusted_root, candidate_root):
    baseline = Corpus(trusted_root)
    candidate = Corpus(candidate_root)
    assets = read_verifier_assets(trusted_root)
    policy = strict_json(assets[POLICY])
    if policy["version"] != 1:
        raise ValueError("unsupported verifier policy")
    for path in policy["preserved_files"]:
        if candidate.read(path) != baseline.read(path):
            raise ValueError(f"protected file changed: {path}")
    for programme in policy["preserved_programmes"]:
        if candidate.programmes.get(programme) != baseline.programmes[programme]:
            raise ValueError(f"protected programme mapping changed: {programme}")
    for ident in policy["preserved_records"]:
        if (candidate.records.get(ident) != baseline.records[ident]
                or candidate.kinds.get(ident) != baseline.kinds[ident]
                or candidate.locations.get(ident) != baseline.locations[ident]):
            raise ValueError(f"protected record changed: {ident}")
    regression_results = check_regressions(strict_json(assets[FIXTURES]))
    results = {}
    for argument in candidate.by_kind("argument"):
        ident = argument["id"]
        premises, conclusion = candidate.formulas(argument)
        try:
            result = verify_logic(premises, conclusion)
        except ValueError as error:
            raise ValueError(f"{ident}: {error}") from error
        results[ident] = {
            "logic": result, "profile": argument["profile_ref"],
            "premise_refs": argument.get("premise_refs", []),
            "objection_refs": argument.get("objection_refs", []),
            "semantic_review": "pending",
        }
    for ident, expected in policy["required_outcomes"].items():
        if results[ident]["logic"]["status"] != expected:
            raise ValueError(f"{ident}: expected {expected}")
    bridge = candidate.records["ARG-SIMPLICITY-BRIDGE"]
    results[bridge["id"]]["lean"] = check_bridge(trusted_root, assets, *candidate.formulas(bridge))
    return {
        "version": 1,
        "scope": "local replay of encoded arguments",
        "candidate": candidate.manifest(),
        "trusted_baseline": baseline.manifest(),
        "trusted_verifier": asset_manifest(assets),
        "regressions": regression_results,
        "arguments": results,
    }
