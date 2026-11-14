"""Regression checks for mixed list/tuple inputs to the dated placebo calendar gate."""
import unittest
from datetime import date, datetime, timedelta
from scripts.phase369_placebo_calendar import audit_calendar

D = date(2025, 9, 1)
S = [D + timedelta(days=i) for i in range(30)]  # synthetic calendar, NOT exchange data

class MixedSequenceTests(unittest.TestCase):
    def test_tuple_sessions_list_events(self):
        self.assertEqual(audit_calendar(tuple(S), [S[10]])['events'], 1)

    def test_list_sessions_tuple_events(self):
        self.assertEqual(audit_calendar(S, (S[10],))['events'], 1)

    def test_tuple_tuple(self):
        self.assertEqual(audit_calendar(tuple(S), (S[10],))['events'], 1)

    def test_datetime_rejected(self):
        with self.assertRaises(ValueError):
            audit_calendar(tuple(S), [datetime(2025, 9, 11)])

    def test_overlap_invariant(self):
        result = audit_calendar(tuple(S), [S[10], S[11]])
        self.assertEqual(result['pairs'][0]['shared_sessions'], 9)

if __name__ == '__main__':
    unittest.main()
