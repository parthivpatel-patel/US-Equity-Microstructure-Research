import unittest
from phase296_weighted_contract import safe_weighted_mean as mean

class ContractTests(unittest.TestCase):
    def test_large_values(self): self.assertEqual(mean([1e308, 1e308], [1,1]), 1e308)
    def test_ordinary(self): self.assertAlmostEqual(mean([2,4], [1,3]), 3.5)
    def test_zero_values(self): self.assertEqual(mean([0,0], [1,2]), 0)
    def test_empty(self):
        with self.assertRaises(ValueError): mean([], [])
    def test_unequal(self):
        with self.assertRaises(ValueError): mean([1,2], [1])
    def test_zero_weight(self):
        with self.assertRaises(ValueError): mean([1], [0])
    def test_negative_weight(self):
        with self.assertRaises(ValueError): mean([1], [-1])
    def test_nonfinite_value(self):
        with self.assertRaises(ValueError): mean([float('inf')], [1])
    def test_nonfinite_weight(self):
        with self.assertRaises(ValueError): mean([1], [float('nan')])
    def test_boolean_weight(self):
        with self.assertRaises(ValueError): mean([1], [True])
    def test_boolean_value(self):
        with self.assertRaises(ValueError): mean([True], [1])
    def test_cancellation(self): self.assertEqual(mean([1e308,-1e308], [1,1]), 0)

if __name__ == '__main__': unittest.main()
