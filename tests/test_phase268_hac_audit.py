import math
import unittest
from scripts.phase268_hac_audit import hac_mean_se, period_difference_hac

class TestHAC(unittest.TestCase):
    def test_constant(self):
        self.assertEqual(hac_mean_se([4]*6,2),0)
    def test_lag_zero(self):
        x=[1,2,3,4]
        self.assertAlmostEqual(hac_mean_se(x,0),math.sqrt(1.25/4))
    def test_lag_one_manual(self):
        x=[1,2,3,4]
        # gamma0=1.25; gamma1=(.75-.25+.75)/4=.3125
        self.assertAlmostEqual(hac_mean_se(x,1),math.sqrt((1.25+.3125)/4))
    def test_bad_lag(self):
        for lag in [-1,4,True,1.2]:
            with self.assertRaises(ValueError): hac_mean_se([1,2,3,4],lag)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): hac_mean_se([1,2,float('nan')],0)
    def test_short(self):
        with self.assertRaises(ValueError): hac_mean_se([1,2],0)
    def test_difference(self):
        daily={str(i):float(i) for i in range(6)}
        r=period_difference_hac(daily,['0','1','2'],['3','4','5'],1)
        self.assertEqual(r['estimate'],3)
        self.assertFalse(r['historical_inference_authorized'])
    def test_missing_date(self):
        with self.assertRaises(ValueError): period_difference_hac({'a':1,'b':2,'c':3},['a'],['b'],0)
    def test_overlap(self):
        with self.assertRaises(ValueError): period_difference_hac({'a':1,'b':2},['a'],['a','b'],0)

if __name__ == '__main__': unittest.main()
