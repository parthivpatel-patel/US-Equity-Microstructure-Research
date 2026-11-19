import unittest
from scripts.phase473_covariance_bounds import variance,sensitivity

class TestVariance(unittest.TestCase):
    def test_iid(self):
        for k in (1,10,20,30,39):
            self.assertAlmostEqual(variance(40,k,0),1/k+1/(40-k))
    def test_symmetry(self):
        for rho in (-.5,0,.5,.8):
            self.assertAlmostEqual(variance(40,10,rho),variance(40,30,rho))
    def test_positive(self):
        for row in sensitivity():
            self.assertGreater(row["variance"],0)
    def test_reject(self):
        for args in ((2,1,.5),(40,0,.5),(40,40,.5),(40,20,1),(40,20,-1)):
            with self.assertRaises(ValueError):
                variance(*args)

if __name__=="__main__":
    unittest.main()
