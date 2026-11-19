import unittest
from phase469_serial_null import calibration

class TestExactNull(unittest.TestCase):
    def test_independent(self):
        v, iv, ratio, size = calibration(rho=0)
        self.assertAlmostEqual(v, 0.1)
        self.assertAlmostEqual(ratio, 1)
        self.assertAlmostEqual(size, 0.05, places=8)
    def test_positive_dependence(self):
        self.assertGreater(calibration(rho=0.8)[2], calibration(rho=0.5)[2])
    def test_negative_dependence(self):
        self.assertLess(calibration(rho=-0.5)[2], 1)
    def test_invalid(self):
        for args in ((1,1,0), (40,40,0), (40,20,1)):
            with self.assertRaises(ValueError): calibration(*args)

if __name__ == "__main__": unittest.main()
