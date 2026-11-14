import unittest
from datetime import date, timedelta, datetime
from phase369_placebo_calendar import audit_calendar

class CalendarAuditTests(unittest.TestCase):
    def setUp(self):
        self.days = [date(2025, 9, 1) + timedelta(days=i) for i in range(30)]

    def test_overlap_and_boundary(self):
        out = audit_calendar(self.days, [self.days[5], self.days[6], self.days[16]])
        self.assertEqual(out['overlapping_pairs'], 1)
        self.assertEqual(out['pairs'][0]['shared_sessions'], 9)
        self.assertEqual(out['windows'][self.days[5].isoformat()]['pre'][0], self.days[0].isoformat())

    def test_nonoverlap(self):
        self.assertEqual(audit_calendar(self.days, [self.days[5], self.days[16]])['overlapping_pairs'], 0)

    def test_reject_missing_calendar_session(self):
        with self.assertRaises(ValueError):
            audit_calendar(self.days, [date(2026, 1, 1)])

    def test_reject_incomplete_window(self):
        with self.assertRaises(ValueError):
            audit_calendar(self.days, [self.days[4]])

    def test_reject_duplicate_sessions_and_events(self):
        with self.assertRaises(ValueError):
            audit_calendar(self.days + [self.days[-1]], [])
        with self.assertRaises(ValueError):
            audit_calendar(self.days, [self.days[5]] * 2)

    def test_reject_datetime_and_boolean_window(self):
        with self.assertRaises(ValueError):
            audit_calendar(self.days, [datetime(2025, 9, 6)])
        with self.assertRaises(ValueError):
            audit_calendar(self.days, [], True)

if __name__ == '__main__':
    unittest.main()
