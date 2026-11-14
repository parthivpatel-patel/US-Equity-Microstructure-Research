import unittest
from fractions import Fraction
from phase366_window_overlap import correlation, report, weights

class TestOverlap(unittest.TestCase):
    def test_exact_lags(self):
        expected=[Fraction(x,10) for x in (10,7,4,1,-2,-5,-4,-3,-2,-1,0)]
        self.assertEqual([correlation(k) for k in range(11)],expected)
    def test_symmetry_beyond_support(self):
        self.assertEqual(correlation(11),0)
        self.assertEqual(correlation(100),0)
    def test_small_window(self):
        self.assertEqual([correlation(k,1) for k in range(3)],[1,Fraction(-1,2),0])
    def test_invalid(self):
        for bad in [0,-1,True,1.2]:
            with self.assertRaises(ValueError): weights(bad)
        for bad in [-1,True,1.2]:
            with self.assertRaises(ValueError): correlation(bad)
    def test_report(self):
        self.assertEqual(report()['1'],'7/10')
        self.assertEqual(report()['5'],'-1/2')

if __name__=='__main__': unittest.main()
