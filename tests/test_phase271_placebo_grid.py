import datetime as dt
import unittest
from scripts.phase271_placebo_grid import placebo_grid

class PlaceboGridTests(unittest.TestCase):
    def setUp(self):
        self.series = [(dt.date(2025, 9, 1) + dt.timedelta(days=i), float(i % 4)) for i in range(20)]
        self.cutoffs = [self.series[8][0], self.series[12][0]]
    def test_grid_size(self):
        self.assertEqual(len(placebo_grid(self.series, self.cutoffs, [0, 2])), 4)
    def test_lag_zero_cross_covariance(self):
        self.assertEqual(placebo_grid(self.series, self.cutoffs, [0])[0]["cross_cutoff_component"], 0)
    def test_point_estimate_invariant_to_lag(self):
        out = placebo_grid(self.series, self.cutoffs, [0, 1, 2])
        self.assertEqual(len(set(x["difference"] for x in out[:3])), 1)
    def test_reject_duplicate_dates(self):
        with self.assertRaises(ValueError): placebo_grid(self.series + [self.series[-1]], self.cutoffs, [0])
    def test_reject_unsorted_dates(self):
        with self.assertRaises(ValueError): placebo_grid(list(reversed(self.series)), self.cutoffs, [0])
    def test_reject_invalid_cutoffs(self):
        with self.assertRaises(ValueError): placebo_grid(self.series, list(reversed(self.cutoffs)), [0])
    def test_reject_insufficient_period(self):
        with self.assertRaises(ValueError): placebo_grid(self.series, [self.series[2][0]], [0])
    def test_reject_duplicate_lags(self):
        with self.assertRaises(ValueError): placebo_grid(self.series, self.cutoffs, [1, 1])
    def test_reject_nonfinite(self):
        with self.assertRaises(ValueError): placebo_grid(self.series[:-1] + [(self.series[-1][0], float("nan"))], self.cutoffs, [0])
    def test_reject_boolean_lag(self):
        with self.assertRaises(ValueError): placebo_grid(self.series, self.cutoffs, [False])
if __name__ == "__main__": unittest.main()
