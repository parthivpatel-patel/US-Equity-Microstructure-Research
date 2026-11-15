import unittest
from fractions import Fraction
from phase387_date_hac import date_hac

D=['2025-09-02','2025-09-03','2025-09-04','2025-09-05']
def panel(values):
    return [(p,d,v) for p in ('a','b') for d,v in zip(D,values)]
class TestHAC(unittest.TestCase):
    def test_constant(self): self.assertEqual(date_hac(panel([3]*4),2)['variance_of_mean'],0)
    def test_lag_zero(self): self.assertEqual(date_hac(panel([0,2,0,2]),0)['variance_of_mean'],Fraction(1,4))
    def test_lag_one(self): self.assertEqual(date_hac(panel([0,2,0,2]),1)['variance_of_mean'],Fraction(1,16))
    def test_order(self): self.assertEqual(date_hac(list(reversed(panel([0,2,0,2]))),1),date_hac(panel([0,2,0,2]),1))
    def test_fraction(self): self.assertEqual(date_hac(panel([Fraction(1,2)]*4),1)['mean'],Fraction(1,2))
    def test_missing(self):
        with self.assertRaises(ValueError): date_hac(panel([1,2,3,4])[:-1],1)
    def test_duplicate(self):
        with self.assertRaises(ValueError): date_hac(panel([1,2,3,4])*2,1)
    def test_bandwidth(self):
        for x in [-1,4,1.0,True]:
            with self.subTest(x=x),self.assertRaises(ValueError): date_hac(panel([1,2,3,4]),x)
    def test_bad_date(self):
        with self.assertRaises(ValueError): date_hac([('a','bad',1),('b','bad',1)],0)
if __name__=='__main__': unittest.main()
