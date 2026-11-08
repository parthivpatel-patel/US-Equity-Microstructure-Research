"""Numerical oracle for Phase 238 using synthetic observations only.

Run: python -m unittest discover -s tests -p 'test_phase241_numeric_oracle.py' -v
"""
import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from phase238_hac_bandwidth_sensitivity import bandwidth_sensitivity

class NumericOracle(unittest.TestCase):
    def test_independent_bartlett_oracle_and_both_estimands(self):
        dates = ["2025-09-02", "2025-09-03", "2025-09-04",
                 "2025-09-05", "2025-09-08", "2025-09-09"]
        equal = [.1, .2, .3, .4, .5, .6]
        pooled = [2., 1., 4., 5., 2., 8.]
        daily = [dict(date=d, equal_cell_contrast=e, pooled_count_contrast=p)
                 for d, e, p in zip(dates, equal, pooled)]
        rows = bandwidth_sensitivity(daily, dates[:3], dates[3:], [0, 1, 2, 3, 4, 5])["results"]
        for key, values in [("equal_cell_contrast", equal), ("pooled_count_contrast", pooled)]:
            a = sum(values[:3]) / 3
            b = sum(values[3:]) / 3
            score = [-(x-a)/3 for x in values[:3]] + [(x-b)/3 for x in values[3:]]
            for bw, row in enumerate(rows):
                expected = sum(s*s for s in score)
                for lag in range(1, bw+1):
                    expected += 2*(1-lag/(bw+1))*sum(score[t]*score[t-lag] for t in range(lag, 6))
                self.assertAlmostEqual(row[key]["difference"], b-a, places=12)
                self.assertAlmostEqual(row[key]["hac_variance"], max(0, expected), places=12)
                self.assertAlmostEqual(row[key]["hac_se"], math.sqrt(max(0, expected)), places=12)

    def test_incomplete_panel_rejected(self):
        dates = ["2025-09-02", "2025-09-03"]
        with self.assertRaises(ValueError):
            bandwidth_sensitivity(
                [dict(date=dates[0], equal_cell_contrast=1., pooled_count_contrast=1.)],
                dates[:1], dates[1:], [0])

if __name__ == "__main__":
    unittest.main()
