"""Phase 171: pre/post coverage admission on fixed-calendar Phase 170 output.

Constructed-data verification only; no SEC observations.
"""
import math
import unittest
from datetime import date

def coverage_gate(rows, cutoff, minimum=0.9):
    def parse(s):
        if not isinstance(s, str):
            raise ValueError("date type")
        try:
            d = date.fromisoformat(s)
        except ValueError as e:
            raise ValueError("invalid date") from e
        if d.isoformat() != s:
            raise ValueError("noncanonical date")
        return d
    c = parse(cutoff)
    if isinstance(minimum, bool) or not isinstance(minimum, (int,float)) or not math.isfinite(minimum) or not 0 <= minimum <= 1:
        raise ValueError("threshold")
    seen = set()
    groups = {"pre": [], "post": []}
    for row in rows:
        d = parse(row["date"])
        if d in seen:
            raise ValueError("duplicate date")
        seen.add(d)
        roster = row["roster"]
        counts = [row[k] for k in ("complete","partial","absent")]
        if type(roster) is not int or roster <= 0 or any(type(v) is not int or v < 0 for v in counts) or sum(counts) != roster:
            raise ValueError("invalid counts")
        if not math.isclose(row["coverage"], counts[0]/roster, rel_tol=0, abs_tol=1e-12):
            raise ValueError("inconsistent coverage")
        groups["pre" if d < c else "post"].append((counts[0], roster))
    if not all(groups.values()):
        raise ValueError("both periods required")
    out = {}
    for name, values in groups.items():
        complete = sum(x for x,_ in values)
        possible = sum(n for _,n in values)
        fraction = complete / possible
        out[name] = dict(dates=len(values),complete=complete,possible=possible,coverage=fraction,passes=fraction >= minimum,worst_date_coverage=min(x/n for x,n in values))
    out["admitted"] = out["pre"]["passes"] and out["post"]["passes"]
    out["coverage_gap_post_minus_pre"] = out["post"]["coverage"] - out["pre"]["coverage"]
    return out

class Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            dict(date="2025-10-01",complete=2,partial=0,absent=0,roster=2,coverage=1),
            dict(date="2025-10-02",complete=1,partial=1,absent=0,roster=2,coverage=.5),
            dict(date="2025-10-03",complete=0,partial=0,absent=2,roster=2,coverage=0)]
    def test_missing_date(self):
        self.assertFalse(coverage_gate(self.rows,"2025-10-03",.5)["admitted"])
    def test_strict(self):
        self.assertFalse(coverage_gate(self.rows,"2025-10-02")["admitted"])
    def test_relaxed(self):
        self.assertTrue(coverage_gate(self.rows,"2025-10-03",0)["admitted"])
    def test_cutoff(self):
        with self.assertRaises(ValueError): coverage_gate(self.rows,"2025-10-3")
    def test_empty_period(self):
        with self.assertRaises(ValueError): coverage_gate(self.rows,"2025-10-01")
    def test_duplicate(self):
        with self.assertRaises(ValueError): coverage_gate(self.rows+self.rows[:1],"2025-10-02")
    def test_counts(self):
        r=[dict(x) for x in self.rows];r[0]["complete"]=3
        with self.assertRaises(ValueError): coverage_gate(r,"2025-10-02")
    def test_fraction(self):
        r=[dict(x) for x in self.rows];r[0]["coverage"]=.8
        with self.assertRaises(ValueError): coverage_gate(r,"2025-10-02")
    def test_threshold(self):
        for t in (-.1,1.1,float("nan"),True):
            with self.subTest(t=t),self.assertRaises(ValueError): coverage_gate(self.rows,"2025-10-02",t)
    def test_pooled(self):
        r=[dict(date="2025-10-01",complete=1,partial=0,absent=0,roster=1,coverage=1),dict(date="2025-10-02",complete=1,partial=0,absent=8,roster=9,coverage=1/9),dict(date="2025-10-03",complete=1,partial=0,absent=0,roster=1,coverage=1)]
        self.assertAlmostEqual(coverage_gate(r,"2025-10-03")["pre"]["coverage"],.2)

if __name__ == "__main__":
    unittest.main()
