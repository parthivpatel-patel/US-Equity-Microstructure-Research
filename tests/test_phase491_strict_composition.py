"""Integration regression tests for Phase 491 strict composition entry point."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase491_strict_composition import audit


class StrictCompositionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.elig = Path(self.temp.name) / 'elig.csv'
        self.panel = Path(self.temp.name) / 'panel.csv'
        self.write(self.elig, ['security', 'exchange', 'date'], [
            ['A', 'X', '2025-10-01'], ['A', 'X', '2025-10-02'],
            ['B', 'Y', '2025-10-02']])
        self.write(self.panel, ['security', 'exchange', 'date', 'outcome'], [
            ['A', 'X', '2025-10-01', '0'], ['A', 'X', '2025-10-02', '1']])

    @staticmethod
    def write(path, header, rows):
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows(rows)

    def run_audit(self):
        return audit(self.elig, self.panel, '2025-10-02')

    def test_counts_and_zero(self):
        result = self.run_audit()
        self.assertEqual(result['pre']['observed_zero_cells'], 1)
        self.assertEqual(result['post']['missing_eligible_cells'], 1)
        self.assertEqual(result['post']['by_exchange']['Y']['missing'], 1)

    def test_extra_panel_field_rejected(self):
        with self.panel.open('a') as stream:
            stream.write('C,X,2025-10-02,2,EXTRA\n')
        with self.assertRaisesRegex(ValueError, 'malformed CSV row'):
            self.run_audit()

    def test_extra_eligibility_field_rejected(self):
        with self.elig.open('a') as stream:
            stream.write('C,X,2025-10-02,EXTRA\n')
        with self.assertRaisesRegex(ValueError, 'malformed CSV row'):
            self.run_audit()

    def test_missing_outcome_rejected(self):
        with self.panel.open('a') as stream:
            stream.write('C,X,2025-10-02\n')
        with self.assertRaisesRegex(ValueError, 'malformed CSV row'):
            self.run_audit()

    def test_duplicate_rejected(self):
        with self.panel.open('a') as stream:
            stream.write('A,X,2025-10-01,0\n')
        with self.assertRaisesRegex(ValueError, 'duplicate key'):
            self.run_audit()

    def test_nonfinite_rejected(self):
        with self.panel.open('a') as stream:
            stream.write('B,Y,2025-10-02,nan\n')
        with self.assertRaisesRegex(ValueError, 'nonfinite outcome'):
            self.run_audit()

    def test_repeated_audits(self):
        self.assertEqual(self.run_audit(), self.run_audit())


if __name__ == '__main__':
    unittest.main()
