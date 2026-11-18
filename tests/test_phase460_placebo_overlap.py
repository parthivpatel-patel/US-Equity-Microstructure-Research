import unittest
from scripts.phase460_placebo_overlap import audit

class AuditTests(unittest.TestCase):
    def test_order_independent(self):
        self.assertEqual(audit(["2025-10-01","2025-09-01"]),audit(["2025-09-01","2025-10-01"]))
    def test_exact_overlap(self):
        x=audit(["2025-09-01","2025-10-01"])
        self.assertEqual(x["pairs"][0]["days_reassigned_from_post_to_pre"],30)
        self.assertEqual(x["pairs"][0]["shared_total_window_days"],125)
    def test_short_window_flag(self):
        self.assertFalse(audit(["2025-11-02"])["windows"][0]["passes_calendar_upper_bound"])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): audit(["2025-10-01"]*2)
    def test_reform_rejected(self):
        with self.assertRaises(ValueError): audit(["2025-11-03"])
    def test_bool_threshold_rejected(self):
        with self.assertRaises(ValueError): audit(["2025-10-01"],min_pre=True)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): audit([])

if __name__=="__main__": unittest.main()
