import unittest
from datetime import date, timedelta
from scripts.phase453_session_preflight import preflight

def dates(start, n):
    d = date.fromisoformat(start)
    return [(d + timedelta(days=i)).isoformat() for i in range(n)]

class SessionPreflightTests(unittest.TestCase):
    def setUp(self):
        self.pre = dates('2025-10-20', 10)
        self.post = dates('2025-11-03', 10)
        self.calendar = self.pre + self.post

    def test_complete_authenticated(self):
        self.assertTrue(preflight(self.calendar, self.calendar, block_length=3,
                                  calendar_authenticated=True)['passes_authenticated_preflight'])

    def test_no_authentication_no_pass(self):
        r = preflight(self.calendar, self.calendar, block_length=3)
        self.assertTrue(r['passes_structural_screen'])
        self.assertFalse(r['passes_authenticated_preflight'])

    def test_missing_session_fails(self):
        observed = [d for d in self.calendar if d != self.pre[4]]
        r = preflight(observed, self.calendar, block_length=3, calendar_authenticated=True)
        self.assertEqual(r['pre']['missing_sessions'], [self.pre[4]])
        self.assertFalse(r['passes_authenticated_preflight'])

    def test_unknown_observation_fails(self):
        r = preflight(self.calendar + ['2025-11-20'], self.calendar, block_length=3)
        self.assertEqual(r['observations_outside_calendar'], ['2025-11-20'])
        self.assertFalse(r['passes_structural_screen'])

    def test_insufficient_block_support(self):
        r = preflight(self.calendar, self.calendar, block_length=6)
        self.assertFalse(r['passes_structural_screen'])

    def test_duplicate_observations_rejected(self):
        with self.assertRaises(ValueError): preflight(self.calendar + [self.pre[0]], self.calendar)

    def test_duplicate_calendar_rejected(self):
        with self.assertRaises(ValueError): preflight(self.calendar, self.calendar + [self.pre[0]])

    def test_empty_period_fails(self):
        self.assertFalse(preflight(self.pre, self.calendar, block_length=2)['passes_structural_screen'])

    def test_invalid_flag_rejected(self):
        with self.assertRaises(ValueError): preflight(self.calendar, self.calendar, calendar_authenticated=1)

    def test_non_session_weekend_detected(self):
        cal = [d for d in self.calendar if d != '2025-11-08']
        r = preflight(self.calendar, cal, block_length=3)
        self.assertIn('2025-11-08', r['observations_outside_calendar'])

if __name__ == '__main__': unittest.main()
