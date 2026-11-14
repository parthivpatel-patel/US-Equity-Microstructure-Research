import unittest
from fractions import Fraction
from phase368_serial_overlap import covariance, correlation, report

class SerialOverlapTests(unittest.TestCase):
    def test_white_noise_matches_existing_phase(self):
        for h in (1, 2, 5, 9):
            for lag in range(2*h + 3):
                expected = Fraction(sum(
                    (-1 if i < h else 1) * (-1 if i-lag < h else 1)
                    for i in range(lag, 2*h)), 2*h)
                self.assertEqual(correlation(lag, h), expected)
    def test_normalization(self):
        for rho in (Fraction(-1,2), Fraction(0), Fraction(1,2)):
            self.assertEqual(correlation(0, 5, rho), 1)
            self.assertGreater(covariance(0, 5, rho), 0)
    def test_nonzero_tail_with_serial_dependence(self):
        self.assertEqual(correlation(10, 5, 0), 0)
        self.assertNotEqual(correlation(10, 5, Fraction(1,2)), 0)
    def test_invalid(self):
        for lag,h,r in ((-1,5,0),(True,5,0),(0,0,0),(0,True,0),(0,5,1),(0,5,-1),(0,5,.5)):
            with self.assertRaises(ValueError): covariance(lag,h,r)
    def test_report(self):
        self.assertEqual(report()['0']['1'], '7/10')

if __name__ == '__main__':
    unittest.main()
