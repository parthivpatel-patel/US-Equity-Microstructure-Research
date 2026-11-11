"""Phase 300: integration regression tests (synthetic numerical inputs only)."""
import unittest
from scripts.phase296_weighted_contract import safe_weighted_mean

class NumericIntegration(unittest.TestCase):
    def test_extreme_integer_weight(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([1], [10**1000])
    def test_extreme_integer_value(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([10**1000], [1])
    def test_normal(self):
        self.assertEqual(safe_weighted_mean([2,4], [1,1]), 3)
    def test_subnormal(self):
        self.assertEqual(safe_weighted_mean([2,4], [5e-324,5e-324]), 3)
    def test_reject_bool(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([True], [1])
    def test_reject_nonfinite(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([1], [float('inf')])
    def test_reject_mismatched(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([1,2], [1])
    def test_reject_zero_weight(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([1], [0])

if __name__ == '__main__':
    unittest.main()
