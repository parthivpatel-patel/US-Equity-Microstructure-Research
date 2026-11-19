import math
import unittest
from phase470_joint_ar1 import weights, covariance, correlation


class JointAR1Tests(unittest.TestCase):
    def test_weights_sum_to_zero(self):
        for k in (1, 10, 20, 30, 39):
            self.assertAlmostEqual(sum(weights(40, k)), 0)

    def test_invalid_inputs(self):
        for args in ((0, 0), (40, 40), (40, -1)):
            with self.assertRaises(ValueError): weights(*args)
        with self.assertRaises(ValueError): covariance(rho=1)
        with self.assertRaises(ValueError): covariance(splits=(10, 10))

    def test_iid_variance(self):
        m = covariance(rho=0)
        for i, k in enumerate((10, 20, 30)):
            self.assertAlmostEqual(m[i][i], 1/k + 1/(40-k))

    def test_phase469_compatibility(self):
        self.assertAlmostEqual(covariance(rho=0.5)[1][1], 0.2700000381469636, places=12)

    def test_symmetry(self):
        m = covariance(rho=0.8)
        for i in range(3):
            for j in range(3): self.assertAlmostEqual(m[i][j], m[j][i])

    def test_overlap_without_serial_correlation(self):
        c = correlation(covariance(rho=0))
        self.assertAlmostEqual(c[0][1], 1/math.sqrt(3))
        self.assertAlmostEqual(c[0][2], 1/3)

    def test_serial_case(self):
        c = correlation(covariance(rho=0.8))
        self.assertAlmostEqual(c[0][1], 0.7106695991321678, places=10)
        self.assertAlmostEqual(c[0][2], 0.41531653319199446, places=10)


if __name__ == '__main__': unittest.main()
