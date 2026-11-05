"""Phase 172: fixed-calendar pooled and daily coverage gate.

Deterministic constructed-data diagnostics only; not SEC estimates.
"""
from datetime import date
import math
import unittest


def audit(rows, cutoff, pooled_minimum=0.9, daily_minimum=0.5):
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

    for t in (pooled_minimum, daily_minimum):
        if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or not 0 <= t <= 1:
            raise ValueError("invalid threshold")
    c = canonical(cutoff)
    seen = set()
    periods = {"pre": [], "post": []}
    for r in rows:
        d = canonical(r["date"])
        if d in seen:
            raise ValueError("duplicate date")
        seen.add(d)
        n = r["roster"]
        counts = [r[k] for k in ("complete", "partial", "absent")]
        if type(n) is not int or n <= 0 or any(type(v) is not int or v < 0 for v in counts) or sum(counts) != n:
            raise ValueError("invalid counts")
        f = counts[0] / n
        reported = r["coverage"]
        if isinstance(reported, bool) or not isinstance(reported, (int, float)) or not math.isfinite(reported) or not math.isclose(f, reported, rel_tol=0, abs_tol=1e-12):
            raise ValueError("inconsistent coverage")
        periods["pre" if d < c else "post"].append((d, counts[0], n))
    if not all(periods.values()):
        raise ValueError("both periods required")
    result = {}
    for period, obs in periods.items():
        obs.sort()
        fractions = [k/n for _, k, n in obs]
        run = longest = 0
        for f in fractions:
            run = run + 1 if f == 0 else 0
            longest = max(longest, run)
        pooled = sum(k for _, k, _ in obs) / sum(n for _, _, n in obs)
        result[period] = {
            "dates": len(obs),
            "pooled_coverage": pooled,
            "worst_daily_coverage": min(fractions),
            "below_daily_floor_dates": [d.isoformat() for (d, _, _), f in zip(obs, fractions) if f < daily_minimum],
            "longest_zero_coverage_run_observed_dates": longest,
            "passes": pooled >= pooled_minimum and all(f >= daily_minimum for f in fractions),
        }
    result["admitted"] = result["pre"]["passes"] and result["post"]["passes"]
    return result


class Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            dict(date=f"2025-10-{d:02d}", complete=k, partial=0, absent=10-k, roster=10, coverage=k/10)
            for d, k in [(1,10),(2,10),(3,10),(6,10),(7,10),(8,10),(9,10),(10,10),(13,10),(14,0),(15,10)]
        ]

    def test_pooled_pass_daily_fail(self):
        r = audit(self.rows, "2025-10-08", .8, .5)
        self.assertAlmostEqual(r["post"]["pooled_coverage"], 5/6)
        self.assertEqual(r["post"]["below_daily_floor_dates"], ["2025-10-14"])
        self.assertFalse(r["admitted"])

    def test_zero_run(self):
        rows = [dict(r, complete=0, absent=10, coverage=0) if r["date"] == "2025-10-15" else r for r in self.rows]
        self.assertEqual(audit(rows, "2025-10-08", 0, 0)["post"]["longest_zero_coverage_run_observed_dates"], 2)

    def test_order_independent(self):
        self.assertEqual(audit(self.rows, "2025-10-08"), audit(list(reversed(self.rows)), "2025-10-08"))

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            audit(self.rows + [self.rows[0]], "2025-10-08")

    def test_invalid_count(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["partial"] = 1
        with self.assertRaises(ValueError):
            audit(rows, "2025-10-08")

    def test_noncanonical_date(self):
        with self.assertRaises(ValueError):
            audit(self.rows, "2025-10-8")

    def test_empty_period(self):
        with self.assertRaises(ValueError):
            audit(self.rows, "2025-10-01")

    def test_invalid_thresholds(self):
        for t in (True, float("nan"), -0.1, 1.1):
            with self.subTest(t=t), self.assertRaises(ValueError):
                audit(self.rows, "2025-10-08", daily_minimum=t)

    def test_bad_fraction(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["coverage"] = 0.9
        with self.assertRaises(ValueError):
            audit(rows, "2025-10-08")

    def test_daily_floor_zero_is_permissive(self):
        self.assertTrue(audit(self.rows, "2025-10-08", 0, 0)["admitted"])


if __name__ == "__main__":
    unittest.main()
