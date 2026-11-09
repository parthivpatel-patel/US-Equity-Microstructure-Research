import unittest
from phase258_trend_sensitivity import rotation_diagnostic, first_difference

class TrendSensitivityTests(unittest.TestCase):
    def test_linear_trend_not_reform(self):
        r = rotation_diagnostic(tuple(range(12)), 6)
        self.assertEqual(r['observed'], 6)
        self.assertEqual(r['tail_fraction'], 2/12)
    def test_flat(self):
        self.assertEqual(rotation_diagnostic([2]*12, 6)['tail_fraction'], 1)
    def test_step(self):
        self.assertEqual(rotation_diagnostic([0]*6+[4]*6, 6)['observed'], 4)
    def test_difference_trend(self):
        self.assertEqual(first_difference(tuple(range(12))), tuple([1]*11))
    def test_bad_bool(self):
        with self.assertRaises(ValueError): rotation_diagnostic([0,1,2,3], True)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): rotation_diagnostic([0,1,float('nan'),3], 2)
    def test_bad_series(self):
        with self.assertRaises(ValueError): first_difference([1,float('inf')])

if __name__ == '__main__':
    unittest.main()
