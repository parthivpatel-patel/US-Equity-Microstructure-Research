"""Phase 160: fail-closed security-panel admission and group weight ESS.

Synthetic fixtures only. Run: python -m unittest -v tests/test_phase160_panel_admission.py
"""
import math
import unittest

def validate_panel(rows):
    if not rows:
        raise ValueError("empty panel")
    seen, counts, weights = set(), {0: 0, 1: 0}, {0: [], 1: []}
    for row in rows:
        ticker = row["Ticker"]
        if not isinstance(ticker, str) or not ticker or ticker != ticker.strip():
            raise ValueError("invalid ticker")
        if ticker in seen:
            raise ValueError("duplicate ticker")
        seen.add(ticker)
        treated = row["treated"]
        if type(treated) is not int or treated not in (0, 1):
            raise ValueError("treatment must be binary integer")
        for name in ("r_pre", "r_post", "v_pre", "v_post"):
            value = row[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError("invalid outcome rate: " + name)
        for name in ("trades_pre", "trades_post"):
            value = row[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                raise ValueError("invalid trade count: " + name)
        for delta, pre, post in (("dr", "r_pre", "r_post"), ("dv", "v_pre", "v_post")):
            if not math.isfinite(row[delta]) or not math.isclose(row[delta], row[post] - row[pre], abs_tol=1e-10, rel_tol=0):
                raise ValueError("inconsistent change: " + delta)
        counts[treated] += 1
        weights[treated].append(min(row["trades_pre"], row["trades_post"]))
    if not all(counts.values()):
        raise ValueError("both groups required")
    return {"counts": counts, "weighted_ess": {
        g: sum(w)**2 / sum(v*v for v in w) for g, w in weights.items()}}

def fixture(ticker="A", treated=1, **overrides):
    row = dict(Ticker=ticker, treated=treated, r_pre=.3, r_post=.4, v_pre=.2,
               v_post=.25, dr=.1, dv=.05, trades_pre=100, trades_post=80)
    row.update(overrides)
    return row

class PanelAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.rows = [fixture(), fixture("B", 0)]

    def test_valid_panel_and_ess(self):
        result = validate_panel(self.rows)
        self.assertEqual(result["counts"], {0: 1, 1: 1})
        self.assertEqual(result["weighted_ess"], {0: 1.0, 1: 1.0})

    def test_duplicate_ticker(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_panel([self.rows[0], fixture("A", 0)])

    def test_treatment_values_fail_closed(self):
        for value in (-1, 2, .5, True, "1"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "treatment"):
                validate_panel([fixture(treated=value), self.rows[1]])

    def test_invalid_rate(self):
        for value in (-.1, 1.1, float("nan"), float("inf"), True):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "rate"):
                validate_panel([fixture(r_pre=value), self.rows[1]])

    def test_invalid_trade_count(self):
        for value in (0, -1, float("nan"), True):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "trade count"):
                validate_panel([fixture(trades_pre=value), self.rows[1]])

    def test_inconsistent_change(self):
        with self.assertRaisesRegex(ValueError, "inconsistent change"):
            validate_panel([fixture(dr=.2), self.rows[1]])

    def test_missing_comparison_group(self):
        with self.assertRaisesRegex(ValueError, "both groups"):
            validate_panel([fixture()])

    def test_weight_concentration(self):
        rows = [fixture("A", 1, trades_pre=100, trades_post=100),
                fixture("C", 1, trades_pre=1, trades_post=1), fixture("B", 0)]
        ess = validate_panel(rows)["weighted_ess"][1]
        self.assertAlmostEqual(ess, 101**2 / (100**2 + 1))
        self.assertLess(ess, 1.03)

if __name__ == "__main__":
    unittest.main()
