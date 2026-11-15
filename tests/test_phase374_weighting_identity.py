import unittest
from decimal import Decimal
from phase374_weighting_identity import summarize

class TestWeights(unittest.TestCase):
    def test_pooled_vs_equal(self):
        r = summarize([(1, 1, 1, 1), (0, 9, 0, 9)])
        self.assertEqual(r['pooled_count'], Decimal('0.1'))
        self.assertEqual(r['equal_row_count'], Decimal('0.5'))
    def test_large_integers_exact(self):
        x = 2**60
        r = summarize([(x-1, x, x-1, x)])
        self.assertLess(r['pooled_count'], 1)
    def test_no_empty(self):
        with self.assertRaises(ValueError): summarize([])
    def test_no_zero_denominator(self):
        with self.assertRaises(ValueError): summarize([(0, 0, 0, 1)])
    def test_no_excess_hidden(self):
        with self.assertRaises(ValueError): summarize([(2, 1, 0, 1)])
    def test_no_fractional(self):
        with self.assertRaises(ValueError): summarize([(0.5, 1, 0, 1)])
    def test_no_nan(self):
        with self.assertRaises(ValueError): summarize([('NaN', 1, 0, 1)])

if __name__ == '__main__': unittest.main()
