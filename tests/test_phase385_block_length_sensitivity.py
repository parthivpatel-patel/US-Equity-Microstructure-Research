"""Constructed fixtures only; no SEC observations."""
import sys
import unittest
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase384_block_resampling import enumerate_circular_block_means
from phase385_block_length_sensitivity import audit_block_lengths

def audit(values, lengths, **kwargs):
    return audit_block_lengths(values, lengths, enumerate_circular_block_means, **kwargs)

class TestAudit(unittest.TestCase):
    def test_two_dates_iid_variance(self):
        r = audit([0, 2], [1, 2])['results']
        self.assertEqual(r[0]['resampling_variance'], Fraction(1, 2))
        self.assertEqual(r[0]['distinct_means'], 3)
        self.assertEqual(r[1]['resampling_variance'], 0)
        self.assertTrue(r[1]['degenerate'])
    def test_three_dates_full_length_degenerate(self):
        r = audit([0, 1, 2], [3])['results'][0]
        self.assertEqual((r['minimum'], r['maximum'], r['draws']), (1, 1, 3))
    def test_constant_series(self):
        self.assertTrue(all(r['degenerate'] for r in audit([4, 4, 4], [1, 2, 3])['results']))
    def test_unsorted_lengths_sorted(self):
        self.assertEqual([r['block_length'] for r in audit([0, 2], [2, 1])['results']], [1, 2])
    def test_fraction_values(self):
        self.assertEqual(audit([Fraction(1, 3), Fraction(2, 3)], [1])['results'][0]['observed_mean'], Fraction(1, 2))
    def test_invalid_lengths(self):
        for ls in ([], [0], [3], [1, 1], [True]):
            with self.subTest(ls=ls), self.assertRaises(ValueError):
                audit([0, 2], ls)
    def test_invalid_values(self):
        for vals in ([], [0, 0.5], [True, 1]):
            with self.subTest(vals=vals), self.assertRaises(ValueError):
                audit(vals, [1])
    def test_budget(self):
        with self.assertRaises(ValueError):
            audit([0, 1, 2, 3], [1], max_draws=10)
    def test_no_inference_claims(self):
        r = audit([0, 2], [1])
        self.assertFalse(r['confidence_interval_validated'])
        self.assertFalse(r['two_way_dependence_handled'])

if __name__ == '__main__':
    unittest.main()
