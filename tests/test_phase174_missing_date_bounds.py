"""Phase 174: fixed-roster bounds for missing expected trading dates.
Constructed fixtures only; not an estimator of reform effects.
"""
from datetime import date
import unittest

def canonical(s):
    if not isinstance(s, str):
        raise ValueError("date must be string")
    try:
        d = date.fromisoformat(s)
    except ValueError as exc:
        raise ValueError("invalid date") from exc
    if d.isoformat() != s:
        raise ValueError("noncanonical date")
    return d

def coverage_bounds(expected_dates, daily_rows, cutoff, roster_size):
    expected = [canonical(s) for s in expected_dates]
    cut = canonical(cutoff)
    if not expected or expected != sorted(set(expected)):
        raise ValueError("expected calendar must be sorted, unique, nonempty")
    if type(roster_size) is not int or roster_size <= 0:
        raise ValueError("invalid fixed roster")
    observed = {}
    universe = set(expected)
    for row in daily_rows:
        d = canonical(row["date"])
        if d not in universe or d in observed:
            raise ValueError("unexpected or duplicate date")
        vals = [row[k] for k in ("complete", "partial", "absent")]
        if any(type(v) is not int or v < 0 for v in vals) or sum(vals) != roster_size:
            raise ValueError("counts must partition roster")
        observed[d] = vals[0]
    result = {}
    for name, days in (("pre", [d for d in expected if d < cut]),
                       ("post", [d for d in expected if d >= cut])):
        if not days:
            raise ValueError("cutoff must split calendar")
        missing = sum(d not in observed for d in days)
        complete = sum(observed.get(d, 0) for d in days)
        denom = len(days) * roster_size
        result[name] = {
            "expected_dates": len(days),
            "missing_dates": missing,
            "observed_complete_pairs": complete,
            "coverage_lower": complete / denom,
            "coverage_upper": (complete + missing * roster_size) / denom,
            "observed_only_coverage": complete / ((len(days) - missing) * roster_size)
                if len(days) > missing else None,
        }
    result["change_bounds"] = [
        result["post"]["coverage_lower"] - result["pre"]["coverage_upper"],
        result["post"]["coverage_upper"] - result["pre"]["coverage_lower"],
    ]
    return result

class Tests(unittest.TestCase):
    def setUp(self):
        self.days = ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-06"]
        self.rows = [dict(date=d, complete=2, partial=0, absent=0) for d in self.days]
    def check(self, rows=None, days=None, cutoff="2025-10-03", roster=2):
        return coverage_bounds(self.days if days is None else days,
                               self.rows if rows is None else rows, cutoff, roster)
    def test_complete(self):
        self.assertEqual(self.check()["change_bounds"], [0, 0])
    def test_missing_post(self):
        r = self.check(rows=self.rows[:2] + self.rows[3:])
        self.assertEqual(r["post"]["observed_only_coverage"], 1)
        self.assertEqual(r["post"]["coverage_lower"], .5)
        self.assertEqual(r["change_bounds"], [-.5, 0])
    def test_missing_entire_post(self):
        r = self.check(rows=self.rows[:2])
        self.assertIsNone(r["post"]["observed_only_coverage"])
        self.assertEqual(r["change_bounds"], [-1, 0])
    def test_observed_zero(self):
        rows = self.rows[:2] + [dict(self.rows[2], complete=0, absent=2)] + self.rows[3:]
        self.assertEqual(self.check(rows=rows)["post"]["coverage_upper"], .5)
    def test_partial(self):
        rows = [dict(self.rows[0], complete=1, partial=1)] + self.rows[1:]
        self.assertEqual(self.check(rows=rows)["pre"]["coverage_lower"], .75)
    def test_duplicate(self):
        with self.assertRaises(ValueError): self.check(rows=self.rows + self.rows[:1])
    def test_unexpected(self):
        with self.assertRaises(ValueError): self.check(rows=[dict(self.rows[0], date="2025-10-07")])
    def test_partition(self):
        with self.assertRaises(ValueError): self.check(rows=[dict(self.rows[0], complete=1)] + self.rows[1:])
    def test_boolean(self):
        with self.assertRaises(ValueError): self.check(rows=[dict(self.rows[0], complete=True)] + self.rows[1:])
    def test_noncanonical(self):
        with self.assertRaises(ValueError): self.check(cutoff="2025-10-3")
    def test_duplicate_calendar(self):
        with self.assertRaises(ValueError): self.check(days=self.days + [self.days[-1]])
    def test_empty_period(self):
        with self.assertRaises(ValueError): self.check(cutoff=self.days[0])
    def test_roster(self):
        with self.assertRaises(ValueError): self.check(roster=True)

if __name__ == "__main__":
    unittest.main()
