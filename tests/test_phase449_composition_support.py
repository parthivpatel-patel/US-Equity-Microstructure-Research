import unittest
from phase449_composition_support import audit

def row(d, s, t, e="X", g="G"):
    return {"date": d, "security": s, "treated": t, "exchange": e, "matched_group": g}

class CompositionTests(unittest.TestCase):
    def test_stable(self):
        dates = ["2025-10-30", "2025-11-04"]
        result = audit([row(d, s, t) for d in dates for s, t in [("A", True), ("B", False)]])
        self.assertTrue(result["strata"][0]["stable_arms_across_both_periods"])
    def test_churn_without_stable_names(self):
        result = audit([row("2025-10-30", "A", True), row("2025-10-30", "B", False),
                        row("2025-11-04", "C", True), row("2025-11-04", "D", False)])
        self.assertFalse(result["strata"][0]["stable_arms_across_both_periods"])
    def test_no_common_date(self):
        result = audit([row("2025-10-30", "A", True), row("2025-11-04", "B", False)])
        self.assertEqual(result["strata"][0]["common_dates"], 0)
    def test_duplicate(self):
        r = row("2025-10-30", "A", True)
        with self.assertRaises(ValueError): audit([r, r])
    def test_assignment_change(self):
        with self.assertRaises(ValueError):
            audit([row("2025-10-30", "A", True), row("2025-11-04", "A", False)])
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])
    def test_invalid_indicator(self):
        with self.assertRaises(ValueError): audit([row("2025-10-30", "A", 1)])
    def test_exchange_separate(self):
        result = audit([row("2025-10-30", "A", True, "X"),
                        row("2025-10-30", "B", False, "X"),
                        row("2025-10-30", "A", True, "Y"),
                        row("2025-10-30", "C", False, "Y")])
        self.assertEqual(len(result["strata"]), 2)

if __name__ == "__main__":
    unittest.main()
