"""Phase 298 regression contract for extreme integer weights (repaired in Phase 300)."""
import unittest
from scripts.phase296_weighted_contract import safe_weighted_mean

class Phase298ExtremeIntegerContract(unittest.TestCase):
    def test_normal_inputs(self):
        self.assertEqual(safe_weighted_mean([2, 4], [1, 1]), 3)

    def test_subnormal_positive_weights(self):
        self.assertEqual(safe_weighted_mean([2, 4], [5e-324, 5e-324]), 3)

    def test_extreme_integer_weight_must_fail_closed_with_value_error(self):
        # Phase 300 integrates finite_float; the regression is no longer expected to fail.
        with self.assertRaises(ValueError):
            safe_weighted_mean([1], [10**1000])

if __name__ == "__main__":
    unittest.main()
