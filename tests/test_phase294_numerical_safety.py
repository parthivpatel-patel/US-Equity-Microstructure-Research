import unittest
from scripts.phase289_common_date_block_bootstrap import bootstrap_common_dates, _safe_mean, _safe_weighted_mean

def panel(a, b, x=3, y=1):
    return {"source_authenticated": False,
            "pair_counts_by_exchange": {"X": x, "Y": y},
            "dates": [{"date": f"2025-09-{i+1:02d}", "by_exchange": {"X": v, "Y": w}}
                      for i, (v, w) in enumerate(zip(a, b))]}

class Phase294NumericalSafety(unittest.TestCase):
    def test_large_same_sign(self):
        out = bootstrap_common_dates(panel([1e308]*5, [1e308]*5), repetitions=99)
        self.assertEqual(out["mean"], 1e308)
        self.assertEqual(out["interval_95_percentile"], [1e308, 1e308])

    def test_large_opposite_sign(self):
        p = panel([1e308]*5, [-1e308]*5)
        self.assertEqual(bootstrap_common_dates(p, weighting="exchange", repetitions=99)["mean"], 0)

    def test_large_weight_roster(self):
        p = panel([2.0]*5, [2.0]*5, 10**300, 10**300)
        self.assertEqual(bootstrap_common_dates(p, repetitions=99)["mean"], 2.0)

    def test_mean_stable(self):
        self.assertEqual(_safe_mean([1e308, 1e308]), 1e308)

    def test_weighted_stable(self):
        self.assertEqual(_safe_weighted_mean([1e308, 1e308], [3, 1]), 1e308)

    def test_existing_small_values(self):
        self.assertEqual(bootstrap_common_dates(panel([2]*5, [-2]*5), repetitions=99)["mean"], 1)

if __name__ == "__main__":
    unittest.main()
