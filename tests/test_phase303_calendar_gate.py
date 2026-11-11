import unittest
from scripts.phase303_calendar_gate import audit_calendar

class CalendarGateTests(unittest.TestCase):
    def test_matching(self):
        r=audit_calendar([{'date':'2025-09-02'}], ['2025-09-02'])
        self.assertTrue(r['calendar_consistent'])
        self.assertFalse(r['source_authenticated'])
    def test_missing_and_extra(self):
        r=audit_calendar([{'date':'2025-09-03'}], ['2025-09-02'])
        self.assertEqual(r['missing_dates'], ['2025-09-02'])
        self.assertEqual(r['extra_dates'], ['2025-09-03'])
    def test_duplicate(self):
        with self.assertRaises(ValueError):
            audit_calendar([{'date':'2025-09-02'}]*2,['2025-09-02'])
    def test_weekend(self):
        with self.assertRaises(ValueError):
            audit_calendar([],['2025-09-06'])
    def test_noncanonical(self):
        with self.assertRaises(ValueError):
            audit_calendar([{'date':'2025-9-2'}],['2025-09-02'])
    def test_unsorted_expected(self):
        with self.assertRaises(ValueError):
            audit_calendar([],['2025-09-03','2025-09-02'])
    def test_holiday_not_inferred(self):
        r=audit_calendar([{'date':'2025-09-01'}], ['2025-09-01'])
        self.assertTrue(r['calendar_consistent'])
        self.assertFalse(r['calendar_authenticated'])

if __name__=='__main__': unittest.main()
