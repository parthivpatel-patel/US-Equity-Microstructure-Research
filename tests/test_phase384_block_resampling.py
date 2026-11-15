"""Deterministic tests for exact circular-block resampling (constructed data only)."""
import unittest
from fractions import Fraction
from scripts.phase384_block_resampling import enumerate_circular_block_means as run, exact_quantile


class BlockTests(unittest.TestCase):
    def test_constant(self):
        r = run([Fraction(1, 3)] * 3, 2)
        self.assertEqual(r['distribution'], ((Fraction(1, 3), 9),))

    def test_one_block_is_circular_shift(self):
        r = run([0, 1, 2], 3)
        self.assertEqual(r['distribution'], ((Fraction(1), 3),))

    def test_independent_date_draws(self):
        r = run([0, 2], 1)
        self.assertEqual(r['distribution'], ((Fraction(0), 1), (Fraction(1), 2), (Fraction(2), 1)))

    def test_block_two(self):
        r = run([0, 0, 3], 2)
        self.assertEqual(r['draws'], 9)
        self.assertEqual(sum(c for _, c in r['distribution']), 9)

    def test_exact_quantile(self):
        d = run([0, 2], 1)['distribution']
        self.assertEqual(exact_quantile(d, 1, 4), 0)
        self.assertEqual(exact_quantile(d, 3, 4), 1)

    def test_budget(self):
        with self.assertRaises(ValueError):
            run(range(10), 1)

    def test_reject_bool_and_float(self):
        for values in ([True, 1], [0.1, 1]):
            with self.assertRaises(ValueError):
                run(values, 1)

    def test_reject_bad_block(self):
        for length in (0, 4, True):
            with self.assertRaises(ValueError):
                run([1, 2, 3], length)

    def test_reject_bad_quantile(self):
        with self.assertRaises(ValueError):
            exact_quantile(((0, 1),), 0, 1)


if __name__ == '__main__':
    unittest.main()
