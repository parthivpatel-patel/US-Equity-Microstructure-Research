import unittest
from phase256_date_signflip import exact_signflip

class TestExact(unittest.TestCase):
    def test_one(self):
        self.assertEqual(exact_signflip([3])['p_two_sided'], 1)
    def test_two(self):
        self.assertEqual(exact_signflip([1, 1])['p_two_sided'], .5)
    def test_three(self):
        self.assertEqual(exact_signflip([1, 1, 1])['p_two_sided'], .25)
    def test_zero(self):
        self.assertEqual(exact_signflip([0, 0])['p_two_sided'], 1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): exact_signflip([float('nan')])
    def test_bool(self):
        with self.assertRaises(ValueError): exact_signflip([True])
    def test_limit(self):
        with self.assertRaises(ValueError): exact_signflip([1]*19)
    def test_empty(self):
        with self.assertRaises(ValueError): exact_signflip([])

if __name__ == '__main__': unittest.main()
