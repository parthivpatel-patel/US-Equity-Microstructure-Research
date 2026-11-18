import unittest
from scripts.phase452_calendar_gap_audit import audit

class CalendarGapTests(unittest.TestCase):
    def test_consecutive(self):
        self.assertTrue(audit(['2025-10-30','2025-10-31','2025-11-03','2025-11-04'])['passes_gap_screen'])
    def test_gap(self):
        r=audit(['2025-10-01','2025-10-15','2025-11-03','2025-11-04'])
        self.assertFalse(r['passes_gap_screen'])
        self.assertEqual(r['pre']['large_gaps'][0][2],14)
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'): audit(['2025-11-03']*2)
    def test_missing_period(self): self.assertFalse(audit(['2025-10-30'])['passes_gap_screen'])
    def test_invalid_gap(self):
        with self.assertRaisesRegex(ValueError,'max_calendar_gap'): audit([],max_calendar_gap=True)
    def test_order_invariance(self):
        d=['2025-10-31','2025-11-03','2025-11-04']
        self.assertEqual(audit(d),audit(d[::-1]))
if __name__=='__main__': unittest.main()
