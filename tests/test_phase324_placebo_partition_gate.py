"""Deterministic tests for Phase 324 necessary-condition audit."""
import unittest
from scripts.phase324_placebo_partition_gate import check


def row(d, n, L, A, lo, hi):
    return dict(nov_minus_oct_pp=str(d), pre_placebo_n=str(n),
                pre_placebo_at_least_as_negative=str(L),
                pre_placebo_at_least_as_extreme_absolute=str(A),
                pre_placebo_min_pp=str(lo), pre_placebo_max_pp=str(hi))


class PartitionGateTests(unittest.TestCase):
    def test_published_count_fails(self):
        r = row("-0.7346606598677254", 78, 2, 2,
                "-1.4475738789418606", "1.0538523294152946")
        self.assertEqual(check(r)["minimum_absolute_extremes"], 3)
        self.assertFalse(check(r)["consistent_with_necessary_conditions"])

    def test_published_volume_not_disproved(self):
        r = row("0.626597999820323", 78, 48, 76,
                "-1.8665501312689659", "1.4840122108986915")
        self.assertEqual(check(r)["minimum_absolute_extremes"], 31)
        self.assertTrue(check(r)["consistent_with_necessary_conditions"])

    def test_negative_no_positive_extreme(self):
        self.assertEqual(check(row(-2, 3, 1, 1, -3, 1))["minimum_absolute_extremes"], 1)

    def test_positive_no_negative_extreme(self):
        self.assertEqual(check(row(2, 3, 2, 1, -1, 3))["minimum_absolute_extremes"], 1)

    def test_invalid_minimum_count(self):
        with self.assertRaises(ValueError):
            check(row(2, 3, 0, 1, -1, 3))

    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            check(row("NaN", 3, 1, 1, -2, 3))


if __name__ == "__main__":
    unittest.main()
