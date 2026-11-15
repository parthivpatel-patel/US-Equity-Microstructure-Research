"""Constructed-fixture tests; no historical SEC data are used."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase373_combined_panel_gate import audit

HEADERS = ['security', 'date', 'exchange', 'cohort', 'hidden_count',
           'total_count', 'hidden_volume', 'total_volume']
BASE = ['AAA', '2025-10-31', 'XNAS', 'treated', '1', '2', '3', '4']


class CombinedGateTests(unittest.TestCase):
    def check_rows(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'panel.csv'
            with path.open('w', newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(HEADERS)
                writer.writerows(rows)
            return audit(path)

    def test_valid_panel(self):
        result = self.check_rows([BASE])
        self.assertTrue(result['passed'])
        self.assertFalse(result['source_authenticated'])
        self.assertFalse(result['treatment_authenticated'])

    def test_precision_violation_is_caught(self):
        row = BASE.copy()
        row[4:6] = ['9007199254740993', '9007199254740992']
        result = self.check_rows([row])
        self.assertFalse(result['passed'])
        self.assertEqual(result['exact_integer']['errors'][0]['issue'],
                         'numerator_exceeds_denominator')

    def test_duplicate_key(self):
        self.assertFalse(self.check_rows([BASE, BASE])['passed'])

    def test_cohort_switch(self):
        other = BASE.copy()
        other[1], other[3] = '2025-11-04', 'control'
        self.assertFalse(self.check_rows([BASE, other])['passed'])

    def test_fractional_measure(self):
        row = BASE.copy()
        row[4] = '1.5'
        self.assertFalse(self.check_rows([row])['passed'])

    def test_empty_panel(self):
        self.assertFalse(self.check_rows([])['passed'])


if __name__ == '__main__':
    unittest.main()
