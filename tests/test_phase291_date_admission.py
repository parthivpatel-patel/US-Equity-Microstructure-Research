"""Synthetic calendar-admission regression tests; no historical SEC observations."""
import unittest
from datetime import date

def strict_iso_day(value):
    if type(value) is not str or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError("date must be canonical YYYY-MM-DD")
    digits = value[:4] + value[5:7] + value[8:]
    if not digits.isascii() or not digits.isdigit():
        raise ValueError("non-ASCII date digits")
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("noncanonical date")
    return parsed

def validate_session_dates(rows, expected_sessions):
    expected = [strict_iso_day(x) for x in expected_sessions]
    observed = [strict_iso_day(r["date"]) for r in rows]
    if len(set(expected)) != len(expected) or expected != sorted(expected):
        raise ValueError("invalid expected calendar")
    if observed != expected:
        raise ValueError("observed sessions differ from supplied calendar")
    return len(observed)

class AdmissionTests(unittest.TestCase):
    def test_valid(self): self.assertEqual(strict_iso_day("2025-11-03").isoformat(), "2025-11-03")
    def test_invalid_february(self):
        with self.assertRaises(ValueError): strict_iso_day("2025-02-29")
    def test_invalid_month(self):
        with self.assertRaises(ValueError): strict_iso_day("2025-13-01")
    def test_noncanonical(self):
        with self.assertRaises(ValueError): strict_iso_day("2025-1-03")
    def test_unicode_digits(self):
        with self.assertRaises(ValueError): strict_iso_day("２０２５-11-03")
    def test_missing_session(self):
        with self.assertRaises(ValueError): validate_session_dates([{"date":"2025-11-03"}], ["2025-11-03","2025-11-04"])
    def test_extra_session(self):
        with self.assertRaises(ValueError): validate_session_dates([{"date":"2025-11-03"},{"date":"2025-11-04"}], ["2025-11-03"])
    def test_duplicate_calendar(self):
        with self.assertRaises(ValueError): validate_session_dates([], ["2025-11-03","2025-11-03"])
    def test_complete(self):
        self.assertEqual(validate_session_dates([{"date":"2025-11-03"},{"date":"2025-11-04"}], ["2025-11-03","2025-11-04"]), 2)

if __name__ == "__main__": unittest.main()
