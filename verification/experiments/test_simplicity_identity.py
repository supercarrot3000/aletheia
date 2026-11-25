import io
import json
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from unittest.mock import patch

import z3

from verification.experiments import simplicity_identity as experiment


class SimplicityExperiment(unittest.TestCase):
    def test_expected_matrix_and_queries_replay(self):
        expected = {
            "common-essence": ["unsat", "sat", "sat"],
            "unrestricted-identity": ["unsat", "unsat", "unsat"],
            "replacement-first": ["unsat", "unsat", "unsat"],
            "replacement-second": ["unsat", "unsat", "unsat"],
            "control-without-opposed-pair": ["sat", "sat", "sat"],
        }
        receipt = experiment.run()
        self.assertEqual(len(receipt["cases"]), 15)
        for row in receipt["cases"]:
            with self.subTest(profile=row["profile"], size=row["domain_size"]):
                wanted = expected[row["profile"]][row["domain_size"] - 1]
                self.assertEqual(row["status"], wanted)
                solver = z3.Solver(ctx=z3.Context())
                solver.from_string(row["smtlib"])
                self.assertEqual(str(solver.check()), wanted)
                self.assertEqual("witness" in row, wanted == "sat")

    def test_witness_check_detects_mutated_interpretations(self):
        case = experiment.PROFILES[0]
        witness = experiment.solve(case, 2)["witness"]
        self.assertTrue(experiment.valid_witness(case, 2, witness))
        changed = deepcopy(witness)
        changed["essence_classes"][changed["filiation"]] = "E9"
        self.assertFalse(experiment.valid_witness(case, 2, changed))
        changed = deepcopy(witness)
        changed["opposition"] = []
        self.assertFalse(experiment.valid_witness(case, 2, changed))
        changed = deepcopy(witness)
        changed["paternity"] = changed["filiation"]
        self.assertFalse(experiment.valid_witness(case, 2, changed))
        for case in experiment.PROFILES[1:4]:
            self.assertFalse(experiment.valid_witness(case, 2, witness))

    def test_unknown_is_reported_and_fails_the_experiment(self):
        case = experiment.PROFILES[0]
        with patch.object(z3.Solver, "check", return_value=z3.unknown):
            with patch.object(z3.Solver, "reason_unknown", return_value="test timeout"):
                row = experiment.solve(case, 2)
        self.assertEqual(row["status"], "unknown")
        self.assertEqual(row["reason"], "test timeout")
        with patch.object(experiment, "run", return_value={"cases": [row]}):
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(experiment.main(), 1)
        self.assertEqual(json.loads(output.getvalue())["cases"][0]["status"], "unknown")
