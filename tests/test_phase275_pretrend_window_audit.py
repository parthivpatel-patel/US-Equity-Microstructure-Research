import unittest
from scripts.phase275_pretrend_window_audit import audit_windows

C = ['2025-09-02','2025-09-03','2025-09-04','2025-09-05','2025-09-08','2025-09-09']
E = ('2025-09-02','2025-09-04')
L = ('2025-09-05','2025-09-09')
class WindowAuditTests(unittest.TestCase):
    def test_partition(self):
        self.assertEqual(audit_windows(C,E,L,require_contiguous_partition=True)['gap_sessions'],0)
    def test_gap_reported(self):
        self.assertEqual(audit_windows(C,('2025-09-02','2025-09-03'),('2025-09-08','2025-09-09'))['gap_sessions'],2)
    def test_gap_rejected_when_partition_required(self):
        with self.assertRaises(ValueError): audit_windows(C,('2025-09-02','2025-09-03'),('2025-09-08','2025-09-09'),require_contiguous_partition=True)
    def test_weekend_endpoint_rejected(self):
        with self.assertRaises(ValueError): audit_windows(C,E,('2025-09-06','2025-09-09'))
    def test_outside_calendar_rejected(self):
        with self.assertRaises(ValueError): audit_windows(C,('2025-09-01','2025-09-04'),L)
    def test_bad_calendar_order(self):
        with self.assertRaises(ValueError): audit_windows(C[::-1],E,L)
    def test_duplicate_calendar(self):
        with self.assertRaises(ValueError): audit_windows(C[:2]+C[1:],E,L)
    def test_overlap(self):
        with self.assertRaises(ValueError): audit_windows(C,E,('2025-09-04','2025-09-09'))
    def test_noncanonical_date(self):
        with self.assertRaises(ValueError): audit_windows(C,('20250902','2025-09-04'),L)
    def test_excluded_sessions(self):
        r=audit_windows(C,('2025-09-03','2025-09-04'),('2025-09-05','2025-09-08'))
        self.assertEqual((r['excluded_before'],r['excluded_after']), (1,1))
    def test_reject_single_session(self):
        with self.assertRaises(ValueError): audit_windows(C,('2025-09-02','2025-09-02'),L)
    def test_no_authentication_claim(self):
        r=audit_windows(C,E,L)
        self.assertFalse(r['calendar_authenticated'])
        self.assertFalse(r['historical_inference_authorized'])
if __name__ == '__main__': unittest.main()
