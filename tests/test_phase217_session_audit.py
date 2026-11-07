"""Deterministic calendar-screening tests; no SEC data or authenticated calendar."""
import unittest
from scripts.phase217_session_audit import audit_candidate_sessions

class SessionAuditTests(unittest.TestCase):
    def test_weekday_sequence(self):
        r = audit_candidate_sessions(['2025-10-09','2025-10-10','2025-10-13'])
        self.assertEqual(r['n_sessions'], 3)
        self.assertFalse(r['exchange_calendar_authenticated'])
    def test_weekend_rejected(self):
        with self.assertRaises(ValueError):
            audit_candidate_sessions(['2025-10-10','2025-10-11','2025-10-13'])
    def test_unexplained_weekday_rejected(self):
        with self.assertRaises(ValueError):
            audit_candidate_sessions(['2025-10-09','2025-10-13'])
    def test_declared_closure_allows_gap_but_not_authentication(self):
        r = audit_candidate_sessions(['2025-10-09','2025-10-13'], ['2025-10-10'])
        self.assertFalse(r['exchange_calendar_authenticated'])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            audit_candidate_sessions(['2025-10-09','2025-10-09'])
    def test_reform_rejected(self):
        with self.assertRaises(ValueError):
            audit_candidate_sessions(['2025-11-03'])
    def test_closure_session_conflict(self):
        with self.assertRaises(ValueError):
            audit_candidate_sessions(['2025-10-09'], ['2025-10-09'])
    def test_noncanonical_date(self):
        with self.assertRaises(ValueError):
            audit_candidate_sessions(['20251009'])
    def test_invalid_closure(self):
        with self.assertRaises(ValueError):
            audit_candidate_sessions(['2025-10-09'], ['2025-10-11'])

if __name__ == '__main__': unittest.main()
