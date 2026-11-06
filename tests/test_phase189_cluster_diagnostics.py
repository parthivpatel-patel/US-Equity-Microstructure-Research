import unittest
from scripts.phase189_cluster_diagnostics import components

class Diagnostics(unittest.TestCase):
    def test_constant(self):
        r=components([[3,3,3],[3,3,3]])
        self.assertEqual(r['variance'],0)
    def test_additive(self):
        r=components([[1,2,3],[4,5,6],[7,8,9]])
        self.assertGreater(r['variance'],0)
    def test_interaction_dominant_negative(self):
        r=components([[1,-1],[-1,1]])
        self.assertLess(r['variance'],0)
        self.assertIsNone(r['se'])
    def test_transpose(self):
        a=[[1,2,3],[4,8,6]]
        b=[list(row) for row in zip(*a)]
        self.assertAlmostEqual(components(a)['variance'],components(b)['variance'])
    def test_reject_unbalanced(self):
        with self.assertRaises(ValueError): components([[1,2],[3]])

if __name__=='__main__': unittest.main()
