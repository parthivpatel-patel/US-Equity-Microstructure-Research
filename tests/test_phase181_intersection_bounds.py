import csv
import tempfile
import unittest
from pathlib import Path
from scripts.phase181_intersection_bounds import audit, bounds

class TestBounds(unittest.TestCase):
    def test_disjoint(self): self.assertEqual(bounds([2, 2], 4), {"lower": 0, "upper": 2})
    def test_forced(self): self.assertEqual(bounds([3, 3], 4), {"lower": 2, "upper": 3})
    def test_identical(self): self.assertEqual(bounds([4, 4], 4), {"lower": 4, "upper": 4})
    def test_five(self): self.assertEqual(bounds([82, 78, 74, 68, 58], 82), {"lower": 32, "upper": 58})
    def test_hundred(self): self.assertEqual(bounds([82, 78, 74, 68, 58], 100), {"lower": 0, "upper": 58})
    def test_bad_universe(self):
        with self.assertRaises(ValueError): bounds([82], 81)
    def test_bad_counts(self):
        with self.assertRaises(ValueError): bounds([2, -1], 3)
    def test_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"a.csv"
            with p.open("w", newline="") as f:
                w = csv.writer(f); w.writerow(["outcome","window_days","pre_placebo_count"])
                for o in ("count","volume"):
                    for window,n in [(3,82),(5,78),(7,74),(10,68),(15,58)]: w.writerow([o,window,n])
            self.assertEqual(audit(p)["sum_memberships"], 360)
    def test_mismatched_outcomes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a.csv";p.write_text("outcome,window_days,pre_placebo_count\ncount,3,82\nvolume,3,81\n")
            with self.assertRaises(ValueError): audit(p)

if __name__ == "__main__": unittest.main()
