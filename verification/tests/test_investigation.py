import unittest
from pathlib import Path

from verification.corpus import Corpus

ROOT = Path(__file__).resolve().parents[2]


class ResearchInvestigation(unittest.TestCase):
    def test_all_linked_question_packets_include_the_report_and_source(self):
        corpus = Corpus(ROOT)
        for question in ("Q-GOD-02", "Q-GOD-03", "Q-GOD-04"):
            with self.subTest(question=question):
                packet = corpus.packet(question)
                report = packet["records"]["INV-SIMPLICITY-IDENTITY"]
                self.assertIn("SRC-AQUINAS-SUMMA", packet["records"])
                self.assertIn("I, q. 28, a. 3", packet["documents"][f"corpus/{report['path']}"])

    def test_investigation_source_must_be_a_source_record(self):
        corpus = Corpus(ROOT)
        corpus.records["INV-SIMPLICITY-IDENTITY"]["source_refs"] = ["Q-GOD-03"]
        with self.assertRaisesRegex(ValueError, "must reference a source"):
            corpus.validate_links()
