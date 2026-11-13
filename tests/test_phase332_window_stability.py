import csv
import tempfile
import unittest
from pathlib import Path
from scripts.phase332_window_stability import audit

FIELDS = ['outcome','window_days','pre_placebo_count','pre_placebo_at_least_as_negative','pre_placebo_at_least_as_extreme_abs','nov_minus_oct_pp']

class StabilityTests(unittest.TestCase):
    def run_rows(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'rows.csv'
            with p.open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=FIELDS)
                w.writeheader()
                w.writerows(rows)
            return audit(p)

    def row(self, days='3', contrast='-0.2', negative='2', extreme='3'):
        return dict(zip(FIELDS, ['count', days, '10', negative, extreme, contrast]))

    def test_sign_reversal(self):
        result = self.run_rows([self.row(), self.row('5','0.1')])['count']
        self.assertFalse(result['sign_stable'])
        self.assertEqual(result['contrast_range_pp'], '0.3')

    def test_stable(self):
        self.assertTrue(self.run_rows([self.row(contrast='-0.2'), self.row('5','-0.1')])['count']['sign_stable'])

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): self.run_rows([self.row(), self.row()])

    def test_invalid_tail_rejected(self):
        with self.assertRaises(ValueError): self.run_rows([self.row(negative='4')])

    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): self.run_rows([self.row(contrast='NaN')])

    def test_zero_rejected(self):
        with self.assertRaises(ValueError): self.run_rows([self.row(contrast='0')])

if __name__ == '__main__':
    unittest.main()
