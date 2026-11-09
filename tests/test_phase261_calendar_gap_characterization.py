"""Characterization tests: weekday checks do not authenticate session completeness."""
import unittest
from datetime import date

def weekday_only_admission(dates):
    return all(d.weekday() < 5 for d in dates)

def absent_sessions(observed, authenticated_calendar):
    return sorted(set(authenticated_calendar) - set(observed))

class CalendarGapTests(unittest.TestCase):
    def test_missing_weekday_passes_weekday_guard(self):
        observed = [date(2025,10,d) for d in (6,7,9,10)]
        expected = [date(2025,10,d) for d in (6,7,8,9,10)]
        self.assertTrue(weekday_only_admission(observed))
        self.assertEqual(absent_sessions(observed,expected),[date(2025,10,8)])
    def test_weekend_rejected(self):
        self.assertFalse(weekday_only_admission([date(2025,10,11)]))
    def test_complete_week(self):
        dates = [date(2025,10,d) for d in (6,7,8,9,10)]
        self.assertEqual(absent_sessions(dates,dates),[])
    def test_missing_weekday_is_not_holiday_proof(self):
        observed = [date(2025,11,3),date(2025,11,5)]
        expected = [date(2025,11,d) for d in (3,4,5)]
        self.assertTrue(weekday_only_admission(observed))
        self.assertEqual(absent_sessions(observed,expected),[date(2025,11,4)])

if __name__ == "__main__":
    unittest.main()
