"""Deterministic algebra and validation checks; no SEC panel data."""
import csv
import tempfile
import unittest
from pathlib import Path
from scripts.phase428_covariance_bounds import bounds

BASE = [
    ("dr", "unadjusted", "-0.0346292858694782", "0.0044178773396563"),
    ("dr", "baseline_adjusted", "-0.010814785925263", "0.005040681518764"),
    ("dv", "unadjusted", "-0.0257205290109133", "0.0042131965708826"),
    ("dv", "baseline_adjusted", "0.0147891302272283", "0.0055690271663983"),
]

class TestBounds(unittest.TestCase):
    def run_rows(self, rows):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "input.csv"
            with path.open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["outcome","specification","effect","se_HC3","n_securities","n_treated"])
                for row in rows:
                    w.writerow([*row,"2262","68"])
            return bounds(path)

    def test_numeric_bounds(self):
        a, b = self.run_rows(BASE)
        self.assertAlmostEqual(a["delta"], 0.0238144999442152)
        self.assertAlmostEqual(a["min_abs_z"], 2.5177725592958384)
        self.assertAlmostEqual(b["delta"], 0.0405096592381416)
        self.assertAlmostEqual(b["min_abs_z"], 4.141150348438238)
    def test_missing_arm(self):
        with self.assertRaises(ValueError):
            self.run_rows(BASE[:-1])
    def test_duplicate_arm(self):
        with self.assertRaises(ValueError):
            self.run_rows(BASE + [BASE[0]])
    def test_negative_se(self):
        bad = BASE.copy()
        bad[0] = (*bad[0][:3], "-1")
        with self.assertRaises(ValueError):
            self.run_rows(bad)
    def test_nonfinite(self):
        bad = BASE.copy()
        bad[0] = (*bad[0][:2], "nan", bad[0][3])
        with self.assertRaises(ValueError):
            self.run_rows(bad)

if __name__ == "__main__":
    unittest.main()
