"""Deterministic synthetic checks for Phase 238 HAC bandwidth sweep."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from phase238_hac_bandwidth_sensitivity import bandwidth_sensitivity

class BandwidthSensitivityTests(unittest.TestCase):
    def setUp(self):
        self.early = ["2025-09-02", "2025-09-03", "2025-09-04"]
        self.late = ["2025-09-05", "2025-09-08", "2025-09-09"]
        self.daily = [
            {"date": d, "equal_cell_contrast": v, "pooled_count_contrast": v}
            for d, v in zip(self.early + self.late, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
        ]

    def test_point_estimate_invariant_to_bandwidth(self):
        result = bandwidth_sensitivity(self.daily, self.early, self.late, [0, 1, 2])
        values = [x["equal_cell_contrast"]["difference"] for x in result["results"]]
        self.assertTrue(all(abs(x - 0.3) < 1e-12 for x in values))
        self.assertEqual(len(result["results"]), 3)
        self.assertFalse(result["causal_effect_established"])

    def test_standard_errors_are_finite_and_nonnegative(self):
        result = bandwidth_sensitivity(self.daily, self.early, self.late, [0, 1, 2])
        for row in result["results"]:
            self.assertGreaterEqual(row["equal_cell_contrast"]["hac_se"], 0)
            self.assertLess(row["equal_cell_contrast"]["hac_se"], 1)

    def test_rejects_duplicate_bandwidths(self):
        with self.assertRaises(ValueError):
            bandwidth_sensitivity(self.daily, self.early, self.late, [0, 0])

    def test_rejects_unsorted_bandwidths(self):
        with self.assertRaises(ValueError):
            bandwidth_sensitivity(self.daily, self.early, self.late, [2, 1])

    def test_rejects_invalid_bandwidth(self):
        for values in ([], [-1], [True], [6]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                bandwidth_sensitivity(self.daily, self.early, self.late, values)

    def test_rejects_incomplete_daily_panel(self):
        with self.assertRaises(ValueError):
            bandwidth_sensitivity(self.daily[:-1], self.early, self.late, [0])

if __name__ == "__main__":
    unittest.main()
