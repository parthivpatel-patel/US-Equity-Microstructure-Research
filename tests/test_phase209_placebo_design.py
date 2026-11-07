"""Synthetic tests only: no SEC observations."""
import unittest
from datetime import date, timedelta
from scripts.phase209_placebo_design import admit_windows

def weekdays(start, n):
    result = []
    d = date.fromisoformat(start)
    while len(result) < n:
        if d.weekday() < 5:
            result.append(d.isoformat())
        d += timedelta(days=1)
    return result

PRE = weekdays("2025-09-02", 20)
POST = weekdays("2025-10-01", 20)
ALL = PRE + POST

class TestAdmission(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(admit_windows(ALL, PRE, POST)["pre_n"], 20)
    def test_empty(self):
        with self.assertRaises(ValueError): admit_windows([], PRE, POST)
    def test_duplicate(self):
        with self.assertRaises(ValueError): admit_windows(ALL + [ALL[-1]], PRE, POST)
    def test_missing_observed_date(self):
        with self.assertRaises(ValueError): admit_windows(ALL[:-1], PRE, POST)
    def test_overlap(self):
        with self.assertRaises(ValueError): admit_windows(ALL, PRE, PRE)
    def test_interleave(self):
        with self.assertRaises(ValueError): admit_windows(ALL, PRE, POST[:10] + PRE[-1:])
    def test_post_reform(self):
        after = weekdays("2025-11-03", 20)
        with self.assertRaises(ValueError): admit_windows(ALL + after, PRE, after)
    def test_short(self):
        with self.assertRaises(ValueError): admit_windows(ALL, PRE[:2], POST)
    def test_noncanonical(self):
        with self.assertRaises(ValueError): admit_windows(ALL, PRE[:-1] + ["2025-9-29"], POST)
    def test_unsorted(self):
        with self.assertRaises(ValueError): admit_windows(ALL, list(reversed(PRE)), POST)
    def test_flag(self):
        self.assertFalse(admit_windows(ALL, PRE, POST)["causal_effect_established"])
