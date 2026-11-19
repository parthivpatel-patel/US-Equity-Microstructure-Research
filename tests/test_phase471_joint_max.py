import unittest
import numpy as np
from phase471_joint_max import ar1_correlation, calibrate

class JointMaxTests(unittest.TestCase):
    def test_symmetry(self):
        r=ar1_correlation(); np.testing.assert_allclose(r,r.T,atol=1e-12)
    def test_diagonal(self):
        np.testing.assert_allclose(np.diag(ar1_correlation()),np.ones(3))
    def test_positive_definite(self):
        self.assertGreater(np.linalg.eigvalsh(ar1_correlation()).min(),0)
    def test_zero_rho(self):
        self.assertAlmostEqual(ar1_correlation(rho=0)[0,1],1/np.sqrt(3),places=12)
    def test_invalid(self):
        with self.assertRaises(ValueError): ar1_correlation(splits=(10,10))
    def test_reproducible(self):
        self.assertEqual(calibrate(draws=1000),calibrate(draws=1000))
    def test_bonferroni(self):
        self.assertLess(calibrate(draws=20000)["bonferroni_familywise"],.06)

if __name__=="__main__": unittest.main()
