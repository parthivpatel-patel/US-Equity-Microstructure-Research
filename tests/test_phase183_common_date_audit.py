"""Deterministic fixtures only, not historical SEC data."""
import unittest
from scripts.phase183_common_date_audit import audit, WINDOWS, OUTCOMES

def fixture():
    return [dict(window_days=str(w), placebo_date=d, outcome=o,
                 contrast_pp=str(w / 10 + (d.endswith("02"))), matched_groups="4")
            for w in WINDOWS for d in ("2025-09-01", "2025-09-02") for o in OUTCOMES]

class CommonDateTests(unittest.TestCase):
    def test_known_mean(self):
        result = audit(fixture())
        self.assertEqual(len(result["common_dates"]), 2)
        self.assertAlmostEqual(result["common_count_means_pp"]["5"], 1.0)
    def test_duplicate(self):
        rows = fixture(); rows.append(rows[0].copy())
        with self.assertRaises(ValueError): audit(rows)
    def test_nonfinite(self):
        rows = fixture(); rows[0]["contrast_pp"] = "nan"
        with self.assertRaises(ValueError): audit(rows)
    def test_non_iso_date(self):
        rows = fixture(); rows[0]["placebo_date"] = "20250901"
        with self.assertRaises(ValueError): audit(rows)
    def test_roster_count_mismatch(self):
        rows = fixture(); rows[0]["matched_groups"] = "3"
        with self.assertRaises(ValueError): audit(rows)
    def test_missing_outcome(self):
        with self.assertRaises(ValueError): audit(fixture()[1:])
    def test_empty_intersection(self):
        rows = fixture()
        for row in rows:
            if row["window_days"] == "15":
                row["placebo_date"] = "2025-09-03" if row["placebo_date"] == "2025-09-01" else "2025-09-04"
        with self.assertRaises(ValueError): audit(rows)

if __name__ == "__main__":
    unittest.main()
