import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verification.corpus import Corpus
from verification.propositional import evaluate
from verification.replay import FIXTURES, PROOF, TOOLCHAIN, check_bridge, check_regressions, verify_logic

ROOT = Path(__file__).resolve().parents[2]
GAP = "ARG-SIMPLICITY-GAP"
BRIDGE = "ARG-SIMPLICITY-BRIDGE"
RUN_LEAN_TESTS = os.environ.get("ALETHEIA_TEST_LEAN") == "1"


def cli(*args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, "-IB", str(ROOT / "aletheia.py"), *map(str, args)],
        cwd=cwd, capture_output=True, timeout=60,
    )


class ResearchWorkflow(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.candidate = Path(temporary.name)
        shutil.copytree(ROOT / "corpus", self.candidate / "corpus")
        shutil.copy2(ROOT / "ACKNOWLEDGEMENTS.md", self.candidate)

    def edit(self, name, change):
        path = self.candidate / "corpus" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_show_preserves_full_text_and_packet_is_repeatable(self):
        self.assertEqual(cli("show", "IDEA-001").stdout, (ROOT / "corpus/ideas/purple-man.md").read_bytes())
        command = cli("packet", "Q-BEAUTY-03")
        self.assertEqual(command.returncode, 0, command.stderr)
        self.assertEqual(command.stdout, cli("packet", "Q-BEAUTY-03", cwd=self.candidate).stdout)
        packet = json.loads(command.stdout)
        self.assertIn("SRC-001", packet["records"])
        self.assertIn("ACKNOWLEDGEMENTS.md", packet["documents"])
        self.assertIn("strawberries", packet["documents"]["corpus/ideas/purple-man.md"])
        direct = json.loads(cli("packet", "Q-BEAUTY-01").stdout)
        self.assertIn("IDEA-001", direct["records"])
        god = json.loads(cli("packet", "Q-GOD-03").stdout)
        self.assertIn("P-BRIDGE", god["records"])
        self.assertIn("OBJ-SIMPLICITY-SEMANTICS", god["records"])

    def test_wrong_reference_kind_fails_even_when_target_exists(self):
        self.edit("claims.json", lambda data: data[0].update(idea_refs=["C-002"]))
        with self.assertRaisesRegex(ValueError, "must reference a idea"):
            Corpus(self.candidate)

    def test_cycle_is_rejected(self):
        def add_cycle(data):
            gap, bridge = data["arguments"]
            gap["depends_on"] = [BRIDGE]
            bridge["depends_on"] = [GAP]

        self.edit("arguments.json", add_cycle)
        with self.assertRaisesRegex(ValueError, "circular argument dependencies"):
            Corpus(self.candidate)

    def test_path_traversal_is_rejected(self):
        self.edit("index.json", lambda data: data["ideas"][0].update(path="../ACKNOWLEDGEMENTS.md"))
        with self.assertRaisesRegex(ValueError, "invalid corpus file"):
            Corpus(self.candidate)

    def test_duplicate_json_key_is_rejected(self):
        path = self.candidate / "corpus/index.json"
        path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            Corpus(self.candidate)

    def test_candidate_cannot_claim_verification_status(self):
        self.edit("claims.json", lambda data: data[0].update(status="verified"))
        with self.assertRaisesRegex(ValueError, "unsupported claim status"):
            Corpus(self.candidate)

    def test_logic_mutations_expose_removed_bridge_and_contradiction(self):
        corpus = Corpus(ROOT)
        premises, conclusion = corpus.formulas(corpus.records[BRIDGE])
        self.assertEqual(verify_logic(premises, conclusion)["status"], "entailed")
        self.assertEqual(verify_logic(premises[:-1], conclusion)["status"], "countermodel")
        contradictory = [*premises, ["not", premises[0]]]
        self.assertEqual(verify_logic(contradictory, conclusion)["status"], "inconsistent_premises")
        with self.assertRaisesRegex(ValueError, "variable bound exceeded"):
            verify_logic([["var", f"v{i}"] for i in range(17)], ["var", "v0"])

    def test_regressions_detect_mutated_implication(self):
        fixtures = json.loads((ROOT / FIXTURES).read_text(encoding="utf-8"))

        def reverse_implication(expr, assignment):
            if expr[0] == "implies":
                expr = [expr[0], expr[2], expr[1]]
            return evaluate(expr, assignment)

        with patch("verification.propositional.evaluate", side_effect=reverse_implication):
            with self.assertRaisesRegex(ValueError, "regression failed|invalid countermodel"):
                check_regressions(fixtures)

    def test_gate_rejects_changed_control_without_using_candidate_code(self):
        (self.candidate / "aletheia.py").write_text("raise SystemExit(42)\n", encoding="utf-8")
        self.edit("arguments.json", lambda data: data["arguments"][1]["premise_refs"].remove("P-BRIDGE"))
        run = cli("verify", "--candidate", self.candidate, cwd=self.candidate)
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn(b"protected record changed: ARG-SIMPLICITY-BRIDGE", run.stderr)

    def test_gate_rejects_changed_recollection(self):
        path = self.candidate / "corpus/ideas/purple-man.md"
        path.write_text("Summary substituted for source material.", encoding="utf-8")
        run = cli("verify", "--candidate", self.candidate)
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn(b"protected file changed", run.stderr)

    @unittest.skipUnless(RUN_LEAN_TESTS, "set ALETHEIA_TEST_LEAN=1 with the pinned Lean installed")
    def test_independent_receipt_and_stale_replay(self):
        verification = self.candidate / "verification"
        verification.mkdir()
        (verification / "policy.json").write_text("{}", encoding="utf-8")
        (verification / "replay.py").write_text("raise SystemExit(42)\n", encoding="utf-8")
        def append_refuted_attempt(data):
            gap = data["arguments"][0]
            data["arguments"].append({
                **gap, "id": "ARG-NEW-ATTEMPT", "depends_on": [GAP],
                "warrant": "Re-examine the gap under the original assumptions.",
            })

        self.edit("arguments.json", append_refuted_attempt)
        run = cli("verify", "--candidate", self.candidate, cwd=self.candidate)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["arguments"][GAP]["logic"]["witness"],
                         {"simple": True, "composite": False, "relational": True})
        self.assertEqual(result["arguments"][BRIDGE]["lean"]["axioms"], [])
        self.assertEqual(result["arguments"]["ARG-NEW-ATTEMPT"]["logic"]["status"], "countermodel")
        self.assertEqual(result["arguments"][BRIDGE]["semantic_review"], "pending")
        receipt = self.candidate / "receipt.json"
        receipt.write_bytes(run.stdout)
        self.assertEqual(cli("replay", receipt, "--candidate", self.candidate).returncode, 0)
        self.edit("questions.json", lambda data: data[0].update(question="An altered question?"))
        run = cli("replay", receipt, "--candidate", self.candidate)
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn(b"receipt differs", run.stderr)

    @unittest.skipUnless(RUN_LEAN_TESTS, "set ALETHEIA_TEST_LEAN=1 with the pinned Lean installed")
    def test_lean_checks_exact_statement_and_rejects_placeholder(self):
        corpus = Corpus(ROOT)
        premises, conclusion = corpus.formulas(corpus.records[BRIDGE])
        assets = {path: (ROOT / path).read_bytes() for path in (TOOLCHAIN, PROOF)}
        with self.assertRaises(subprocess.CalledProcessError):
            check_bridge(ROOT, assets, premises[:-1], conclusion)
        original = assets[PROOF].decode("utf-8")
        proof_start = original.index("  fun isRelational")
        proof_end = original.index("\n", proof_start)
        assets[PROOF] = (original[:proof_start] + "  sorry" + original[proof_end:]).encode()
        with self.assertRaises(subprocess.CalledProcessError):
            check_bridge(ROOT, assets, premises, conclusion)
