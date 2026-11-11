"""Phase 301: numerical compatibility checks before bootstrap helper integration.

Synthetic software checks only; no historical market data are used.
Run: python -m unittest tests.test_phase301_weighted_compatibility -v
"""
import unittest
from scripts.phase296_weighted_contract import safe_weighted_mean
from scripts.phase289_common_date_block_bootstrap import _safe_weighted_mean

class WeightedCompatibility(unittest.TestCase):
    def test_floating_rounding_is_not_exact(self):
        result = safe_weighted_mean([2, -2], [3, 1])
        self.assertAlmostEqual(result, 1.0, places=14)
        self.assertNotEqual(result, 1.0)

    def test_existing_helper_exact_on_simple_inputs(self):
        self.assertEqual(_safe_weighted_mean([2, -2], [3, 1]), 1.0)

    def test_extreme_integer_rejected_by_new_helper(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([10**1000, 1], [1, 1])

    def test_mismatched_length_rejected_by_new_helper(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([1, 2], [1])

    def test_zero_weight_rejected_by_new_helper(self):
        with self.assertRaises(ValueError):
            safe_weighted_mean([1, 2], [1, 0])

    def test_large_finite_inputs(self):
        self.assertEqual(safe_weighted_mean([1e308, 1e308], [3, 1]), 1e308)
