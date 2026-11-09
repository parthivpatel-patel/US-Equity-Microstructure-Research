"""Synthetic structural tests; no historical SEC observations."""
import datetime as dt
import unittest
from scripts.phase270_temporal_gate import validate_temporal_series as check

D = [dt.date(2025, 10, 27) + dt.timedelta(days=i) for i in range(5)]
C = D[2]
S = list(zip(D, [1., 2., 3., 4., 5.]))

class TemporalGateTests(unittest.TestCase):
    def test_complete(self):
        r = check(S, D, C)
        self.assertEqual((r["pre_dates"], r["post_dates"]), (2, 3))
        self.assertFalse(r["historical_inference_authorized"])
    def test_missing_middle(self):
        with self.assertRaisesRegex(ValueError, "calendar mismatch"):
            check(S[:2] + S[3:], D, C)
    def test_extra_session(self):
        with self.assertRaisesRegex(ValueError, "calendar mismatch"):
            check(S + [(D[-1] + dt.timedelta(days=1), 6)], D, C)
    def test_reordered(self):
        with self.assertRaisesRegex(ValueError, "unique and increasing"):
            check(S[::-1], D, C)
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, "unique and increasing"):
            check(S + [S[-1]], D, C)
    def test_bad_expected(self):
        with self.assertRaisesRegex(ValueError, "unique and increasing"):
            check(S, D[::-1], C)
    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            check(S[:-1] + [(D[-1], float("nan"))], D, C)
    def test_period_short(self):
        with self.assertRaisesRegex(ValueError, "two dates"):
            check(S, D, D[1])
    def test_wrong_date_type(self):
        with self.assertRaisesRegex(ValueError, "invalid observation dates"):
            check([("2025-10-27", 1)] + S[1:], D, C)
    def test_empty(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            check([], D, C)

if __name__ == "__main__":
    unittest.main()
