import json
import unittest
from pathlib import Path
from verification.propositional import check, evaluate

ROOT = Path(__file__).resolve().parents[2]

class TestLogic(unittest.TestCase):
    def test_fixtures(self):
        for f in json.loads((ROOT / 'verification/fixtures/logic.json').read_text()):
            with self.subTest(fixture=f['id']):
                r = check(f['premises'], f['conclusion'])
                self.assertEqual(r['status'], f['expected'])
                if r['status'] == 'countermodel':
                    self.assertTrue(all(evaluate(p, r['witness']) for p in f['premises']))
                    self.assertFalse(evaluate(f['conclusion'], r['witness']))

    def test_invalid_formula(self):
        with self.assertRaises(ValueError):
            check([], ['arbitrary_code', 'x'])

class TestCorpus(unittest.TestCase):
    def test_ids_and_references(self):
        corpus = ROOT / 'corpus'
        idx = json.loads((corpus / 'index.json').read_text())
        ideas = idx['ideas']
        questions = json.loads((corpus / idx['questions']).read_text())
        claims = json.loads((corpus / idx['claims']).read_text())
        sources = idx.get('sources', [])
        records = ideas + questions + claims + sources
        ids = [r['id'] for r in records]
        self.assertEqual(len(ids), len(set(ids)))
        for rec in ideas:
            self.assertTrue((corpus / rec['path']).is_file())
        for path in idx['programmes']:
            self.assertTrue((corpus / path).is_file())
        for claim in claims:
            for ref in claim.get('idea_refs', []) + claim.get('question_refs', []):
                self.assertIn(ref, ids)

    def test_idea_source_provenance(self):
        corpus = ROOT / 'corpus'
        idx = json.loads((corpus / 'index.json').read_text())
        sources = {s['id']: s for s in idx['sources']}
        for idea in idx['ideas']:
            for ref in idea.get('source_refs', []):
                self.assertIn(ref, sources)
                path = corpus / sources[ref]['path']
                source = json.loads(path.read_text())
                self.assertEqual(source['id'], ref)
                self.assertEqual(source['recollection']['idea_ref'], idea['id'])
                self.assertTrue((path.parent / source['acknowledgement_path']).is_file())
                if source['identification_status'] == 'unresolved':
                    self.assertIsNone(source['author'])
                    self.assertIsNone(source['original_title'])
                    self.assertFalse(source['broadcast']['station_confirmed'])
