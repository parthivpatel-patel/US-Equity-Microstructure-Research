import unittest
from scripts.phase347_two_way_cluster_diagnostic import variance_components

class Tests(unittest.TestCase):
    def test_exact_balanced(self):
        x=variance_components([('A','d1',1.),('A','d2',3.),('B','d1',5.),('B','d2',7.)])
        self.assertEqual(x['mean_pp'],4.)
        self.assertAlmostEqual(x['group_component'],2.)
        self.assertAlmostEqual(x['date_component'],0.5)
        self.assertAlmostEqual(x['intersection_component'],1.25)
        self.assertAlmostEqual(x['two_way_raw_variance'],1.25)
    def test_duplicates_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):
            variance_components([('A','d1',1.),('A','d1',2.)])
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            variance_components([('A','d1',float('nan')),('B','d1',2.)])
    def test_single_rejected(self):
        with self.assertRaises(ValueError):
            variance_components([('A','d1',1.)])
if __name__=='__main__': unittest.main()
