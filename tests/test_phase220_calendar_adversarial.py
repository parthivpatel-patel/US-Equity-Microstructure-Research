"""Adversarial calendar-consistency tests; synthetic, not historical inference."""
import unittest
from datetime import date, timedelta

REFORM = date(2025, 11, 3)

def weekday_sessions(start, count):
    d = date.fromisoformat(start)
    out = []
    while len(out) < count:
        if d >= REFORM:
            raise ValueError('reform boundary')
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += timedelta(days=1)
    return out

def strict_admission(rows, sessions):
    if not sessions or sessions != sorted(set(sessions)):
        raise ValueError('invalid calendar')
    if [r['date'] for r in rows] != sessions:
        raise ValueError('missing observations')
    return len(sessions)

class CalendarAdversarialTests(unittest.TestCase):
    def test_weekday_filter_includes_labor_day(self):
        sessions = weekday_sessions('2025-08-29', 4)
        self.assertIn('2025-09-01', sessions)
    def test_self_consistent_false_calendar_passes_consistency(self):
        sessions = weekday_sessions('2025-08-29', 4)
        rows = [{'date': x, 'contrast': 0.0} for x in sessions]
        self.assertEqual(strict_admission(rows, sessions), 4)
    def test_omission_from_both_rows_and_calendar_is_invisible(self):
        sessions = weekday_sessions('2025-09-02', 8)
        omitted = sessions[:3] + sessions[4:]
        rows = [{'date': x, 'contrast': 0.0} for x in omitted]
        self.assertEqual(strict_admission(rows, omitted), 7)
    def test_omission_from_rows_only_rejected(self):
        sessions = weekday_sessions('2025-09-02', 8)
        rows = [{'date': x, 'contrast': 0.0} for x in sessions[1:]]
        with self.assertRaises(ValueError):
            strict_admission(rows, sessions)
    def test_reform_boundary_rejected(self):
        with self.assertRaises(ValueError):
            weekday_sessions('2025-10-31', 3)

if __name__ == '__main__':
    unittest.main()
