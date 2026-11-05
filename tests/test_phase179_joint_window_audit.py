"""Regression tests for the Phase 179 descriptive audit."""
import csv
import tempfile
import unittest
from pathlib import Path
from scripts.phase179_joint_window_audit import audit

FIELDS = ["outcome", "window_days", "nov_minus_oct_pp", "pre_placebo_count", "pre_placebo_at_least_as_extreme_abs"]

class TestJointWindowAudit(unittest.TestCase):
    def rows(self):
        return [dict(zip(FIELDS, row)) for row in [
            ("count", 3, -0.5, 10, 2), ("volume", 3, 0.2, 10, 8),
            ("count", 5, 0.3, 8, 3), ("volume", 5, 0.4, 8, 7)]]

    def evaluate(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            return audit(path)

    def test_signs(self):
        result = self.evaluate(self.rows())
        self.assertEqual((result["opposite_sign_windows"], result["count_sign_changes"], result["volume_sign_changes"]), (1, 1, 0))

    def test_gap(self):
        self.assertAlmostEqual(self.evaluate(self.rows())["windows"][0]["volume_minus_count_pp"], 0.7)

    def test_duplicate(self):
        rows = self.rows()
        rows.append(rows[0])
        with self.assertRaises(ValueError):
            self.evaluate(rows)

    def test_missing_outcome(self):
        with self.assertRaises(ValueError):
            self.evaluate(self.rows()[:-1])

    def test_bad_placebo_count(self):
        rows = self.rows()
        rows[0]["pre_placebo_at_least_as_extreme_abs"] = 11
        with self.assertRaises(ValueError):
            self.evaluate(rows)

    def test_nonfinite(self):
        rows = self.rows()
        rows[0]["nov_minus_oct_pp"] = "nan"
        with self.assertRaises(ValueError):
            self.evaluate(rows)

    def test_unknown_outcome(self):
        rows = self.rows()
        rows[0]["outcome"] = "unknown"
        with self.assertRaises(ValueError):
            self.evaluate(rows)

if __name__ == "__main__":
    unittest.main()
