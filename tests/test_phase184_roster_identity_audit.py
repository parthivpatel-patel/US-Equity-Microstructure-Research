"""Deterministic synthetic validation; not historical SEC observations."""
import unittest
from scripts.phase184_roster_identity_audit import audit, WINDOWS

def fixture():
    return [dict(window_days=str(w), placebo_date=d, outcome=o,
                 matched_group_id=g, contrast_pp=str(v))
            for w in WINDOWS for d in ("2025-09-02", "2025-09-03")
            for o, v in (("count", 1), ("volume", 3)) for g in ("A", "B")]

class AuditTests(unittest.TestCase):
    def test_balanced(self):
        r = audit(fixture())
        self.assertEqual(r["balanced_equal_group_date_means_pp"]["5"], {"count": 1, "volume": 3})
    def test_identity_mismatch_same_group_count(self):
        x = fixture()
        next(z for z in x if z["window_days"] == "5" and z["outcome"] == "volume")["matched_group_id"] = "C"
        with self.assertRaises(ValueError): audit(x)
    def test_cross_window_drift(self):
        x = fixture()
        for z in x:
            if z["window_days"] == "10": z["matched_group_id"] += "_new"
        with self.assertRaises(ValueError): audit(x)
    def test_duplicate(self):
        x = fixture(); x.append(dict(x[0]))
        with self.assertRaises(ValueError): audit(x)
    def test_nonfinite(self):
        x = fixture(); x[0]["contrast_pp"] = "nan"
        with self.assertRaises(ValueError): audit(x)
    def test_missing_outcome_date(self):
        x = [z for z in fixture() if not (z["window_days"] == "3" and z["outcome"] == "volume" and z["placebo_date"] == "2025-09-02")]
        with self.assertRaises(ValueError): audit(x)
    def test_invalid_date(self):
        x = fixture(); x[0]["placebo_date"] = "2025-09-31"
        with self.assertRaises(ValueError): audit(x)
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])

if __name__ == "__main__":
    unittest.main()
