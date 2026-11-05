"""Phase 175: fixed-roster weighted coverage sensitivity; synthetic fixtures only."""
from math import isfinite
import unittest

def coverage_bounds(rows, weights):
    """Rows: date -> group -> 0/1/None (missing); fixed positive group weights."""
    if not rows or not weights:
        raise ValueError("nonempty expected dates and roster required")
    if any(not isinstance(w, (int, float)) or isinstance(w, bool) or not isfinite(w) or w <= 0 for w in weights.values()):
        raise ValueError("weights must be finite and positive")
    total = lower = upper = 0.0
    for date, observed in rows.items():
        if not isinstance(date, str) or not date or not isinstance(observed, dict):
            raise ValueError("invalid date/row")
        if set(observed) - set(weights):
            raise ValueError("unexpected group")
        for group, weight in weights.items():
            value = observed.get(group)
            if value not in (None, 0, 1) or isinstance(value, bool):
                raise ValueError("coverage must be 0, 1, or missing")
            total += weight
            if value == 1:
                lower += weight
                upper += weight
            elif value is None:
                upper += weight
    return lower / total, upper / total

def change_bounds(pre, post, weights):
    pre_lo, pre_hi = coverage_bounds(pre, weights)
    post_lo, post_hi = coverage_bounds(post, weights)
    return post_lo - pre_hi, post_hi - pre_lo

class TestWeightedCoverage(unittest.TestCase):
    def test_complete(self):
        self.assertEqual(coverage_bounds({"d": {"a": 1, "b": 1}}, {"a": 1, "b": 2}), (1, 1))
    def test_missing_cell(self):
        self.assertEqual(coverage_bounds({"d": {"a": 1}}, {"a": 1, "b": 3}), (.25, 1))
    def test_observed_zero_not_missing(self):
        self.assertEqual(coverage_bounds({"d": {"a": 0}}, {"a": 1}), (0, 0))
    def test_missing_date(self):
        self.assertEqual(coverage_bounds({"d": {}}, {"a": 1}), (0, 1))
    def test_weight_sensitivity(self):
        rows = {"d": {"a": 1, "b": 0}}
        self.assertEqual(coverage_bounds(rows, {"a": 1, "b": 1}), (.5, .5))
        self.assertEqual(coverage_bounds(rows, {"a": 1, "b": 9}), (.1, .1))
    def test_change_bounds(self):
        self.assertEqual(change_bounds({"d1": {"a": 1, "b": 1}}, {"d2": {"a": 1}}, {"a": 1, "b": 1}), (-.5, 0))
    def test_reject_bad_weights(self):
        for weight in (0, -1, float("nan"), float("inf"), True):
            with self.subTest(weight=weight):
                with self.assertRaises(ValueError):
                    coverage_bounds({"d": {}}, {"a": weight})
    def test_reject_unexpected_group(self):
        with self.assertRaises(ValueError):
            coverage_bounds({"d": {"b": 1}}, {"a": 1})
    def test_reject_bad_cell(self):
        for value in (-1, 2, .5, True, "1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    coverage_bounds({"d": {"a": value}}, {"a": 1})
    def test_no_dates(self):
        with self.assertRaises(ValueError):
            coverage_bounds({}, {"a": 1})

if __name__ == "__main__":
    unittest.main()
