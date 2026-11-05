"""Phase 173: distinguish absent expected trading dates from observed zero coverage.

Constructed fixtures only. Expected dates must come from authenticated external calendar.
"""
from datetime import date
import unittest

def iso(s):
    if not isinstance(s, str):
        raise ValueError("date type")
    try: d = date.fromisoformat(s)
    except ValueError as e: raise ValueError("invalid date") from e
    if d.isoformat() != s: raise ValueError("noncanonical date")
    return d

def audit(expected_dates, rows, cutoff):
    expected = [iso(x) for x in expected_dates]
    cut = iso(cutoff)
    if not expected or expected != sorted(set(expected)):
        raise ValueError("expected calendar must be nonempty, unique, sorted")
    universe = set(expected)
    observed = {}
    for row in rows:
        d = iso(row["date"])
        if d not in universe or d in observed:
            raise ValueError("unexpected or duplicate date")
        values = [row[k] for k in ("roster", "complete", "partial", "absent")]
        n, complete, partial, absent = values
        if any(type(x) is not int for x in values) or n <= 0 or min(complete, partial, absent) < 0 or complete + partial + absent != n:
            raise ValueError("invalid counts")
        observed[d] = (complete, n)
    result = {}
    for name, dates in (("pre", [d for d in expected if d < cut]), ("post", [d for d in expected if d >= cut])):
        if not dates: raise ValueError("cutoff must split calendar")
        missing = [d.isoformat() for d in dates if d not in observed]
        run = longest = 0
        for d in dates:
            run = run + 1 if d not in observed else 0
            longest = max(longest, run)
        present = [observed[d] for d in dates if d in observed]
        result[name] = dict(expected_dates=len(dates), observed_dates=len(present),
            missing_dates=missing, longest_missing_expected_date_run=longest,
            observed_only_pooled_coverage=(sum(k for k,n in present)/sum(n for k,n in present)) if present else None,
            calendar_complete=not missing)
    result["calendar_complete"] = result["pre"]["calendar_complete"] and result["post"]["calendar_complete"]
    return result

class Tests(unittest.TestCase):
    def setUp(self):
        self.days = ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-06"]
        self.rows = [dict(date=d, roster=2, complete=2, partial=0, absent=0) for d in self.days]
    def check(self, days=None, rows=None, cutoff="2025-10-03"):
        return audit(self.days if days is None else days, self.rows if rows is None else rows, cutoff)
    def test_missing_date(self):
        r = self.check(rows=self.rows[:2]+self.rows[3:])
        self.assertEqual(r["post"]["missing_dates"], ["2025-10-03"])
        self.assertEqual(r["post"]["observed_only_pooled_coverage"], 1)
        self.assertFalse(r["calendar_complete"])
    def test_consecutive_absences(self):
        r = self.check(rows=self.rows[:2])
        self.assertEqual(r["post"]["longest_missing_expected_date_run"], 2)
        self.assertIsNone(r["post"]["observed_only_pooled_coverage"])
    def test_complete(self): self.assertTrue(self.check()["calendar_complete"])
    def test_observed_zero_not_absent(self):
        rows = [dict(self.rows[0], complete=0, absent=2)]+self.rows[1:]
        r = self.check(rows=rows)
        self.assertTrue(r["calendar_complete"])
        self.assertEqual(r["pre"]["observed_only_pooled_coverage"], .5)
    def test_duplicate_expected(self):
        with self.assertRaises(ValueError): self.check(days=self.days+[self.days[0]])
    def test_unsorted_expected(self):
        with self.assertRaises(ValueError): self.check(days=list(reversed(self.days)))
    def test_duplicate_observed(self):
        with self.assertRaises(ValueError): self.check(rows=self.rows+[self.rows[0]])
    def test_unexpected_observed(self):
        with self.assertRaises(ValueError): self.check(rows=self.rows+[dict(self.rows[0],date="2025-10-07")])
    def test_noncanonical(self):
        with self.assertRaises(ValueError): self.check(cutoff="2025-10-3")
    def test_invalid_counts(self):
        with self.assertRaises(ValueError): self.check(rows=[dict(self.rows[0],complete=3)]+self.rows[1:])
    def test_boolean_counts(self):
        with self.assertRaises(ValueError): self.check(rows=[dict(self.rows[0],complete=True)]+self.rows[1:])
    def test_empty_period(self):
        with self.assertRaises(ValueError): self.check(cutoff="2025-10-01")

if __name__ == "__main__":
    unittest.main()
