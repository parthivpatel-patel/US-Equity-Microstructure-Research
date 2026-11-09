import unittest
from scripts.phase265_weight_bounds import bounds

class TestBounds(unittest.TestCase):
    def test_equal_only(self):
        x=bounds([1,3,5],1/3,1/3)
        self.assertAlmostEqual(x["minimum"],3)
        self.assertAlmostEqual(x["maximum"],3)
    def test_unrestricted(self):
        x=bounds([-2,1,4])
        self.assertEqual(x["minimum"],-2)
        self.assertEqual(x["maximum"],4)
    def test_capped(self):
        x=bounds([-2,1,4],0.2,0.5)
        self.assertAlmostEqual(x["minimum"],0.1)
        self.assertAlmostEqual(x["maximum"],1.9)
    def test_constant(self):
        x=bounds([7,7],0,1)
        self.assertEqual((x["minimum"],x["maximum"]),(7,7))
    def test_infeasible(self):
        with self.assertRaises(ValueError): bounds([1,2,3],0,0.2)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): bounds([1,float("nan")])
    def test_empty(self):
        with self.assertRaises(ValueError): bounds([])
    def test_weight_sums(self):
        x=bounds([-3,0,2,9],0.1,0.4)
        for key in ("minimum_weights","maximum_weights"):
            self.assertAlmostEqual(sum(x[key]),1)
            self.assertTrue(all(0.1<=w<=0.4 for w in x[key]))

if __name__=="__main__": unittest.main()
