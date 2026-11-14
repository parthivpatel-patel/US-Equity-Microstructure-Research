import unittest
from fractions import Fraction
from phase367_trend_contamination import contrast, linear_trend_bias, detrended_contrast

class TrendContaminationTests(unittest.TestCase):
    def test_linear_trends_all_windows(self):
        for h in (1,2,5,10,20):
            for slope in (Fraction(0), Fraction(1,7), Fraction(-3,11)):
                values = [Fraction(9,4)+slope*t for t in range(-h,h)]
                self.assertEqual(contrast(values,h),linear_trend_bias(slope,h))
                self.assertEqual(detrended_contrast(values,h,slope),0)
    def test_level_invariance(self):
        self.assertEqual(contrast([2,2,2,2],2),0)
    def test_step_not_erased(self):
        self.assertEqual(detrended_contrast([0,0,3,3],2,0),3)
    def test_negative_trend(self):
        self.assertEqual(linear_trend_bias('-0.02',5),Fraction(-1,10))
    def test_invalid_windows(self):
        for h in (0,-1,True,2.5):
            with self.assertRaises(ValueError): contrast([0,0],h)
    def test_invalid_length(self):
        with self.assertRaises(ValueError): contrast([1,2,3],2)
    def test_invalid_values(self):
        for v in (float('nan'),float('inf'),'bad'):
            with self.assertRaises(ValueError): contrast([0,v],1)

if __name__ == '__main__': unittest.main()
