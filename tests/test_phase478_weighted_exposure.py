import unittest
from phase478_weighted_exposure import variance_components
class TestWeightedExposure(unittest.TestCase):
    def test_cancellation(self):
        x=variance_components([.5,-.5],[1,1]);self.assertAlmostEqual(x['se_inflation'],1)
    def test_permutation(self):
        a=variance_components([.5,-.5],[2,1]);b=variance_components([-.5,.5],[1,2]);self.assertAlmostEqual(a['factor_variance'],b['factor_variance'])
    def test_weight_scale(self):
        a=variance_components([.5,-.5],[2,1]);b=variance_components([.5,-.5],[20,10]);self.assertAlmostEqual(a['se_inflation'],b['se_inflation'])
    def test_common_rho_cancels_ratio(self):
        a=variance_components([.5,-.5],[2,1],.0,.0);b=variance_components([.5,-.5],[2,1],.8,.8);self.assertAlmostEqual(a['se_inflation'],b['se_inflation'])
    def test_invalid(self):
        with self.assertRaises(ValueError):variance_components([1,2],[0,0])
if __name__=='__main__':unittest.main()
