import unittest
from scripts.phase348_weighted_cluster import weighted_components

class TestWeighted(unittest.TestCase):
    def test_unbalanced_weights(self):
        rows=[('A','2025-09-01',80),('A','2025-09-02',80),('B','2025-09-01',-80)]
        r=weighted_components(rows)
        self.assertAlmostEqual(r['equal_group_mean_pp'],0)
        self.assertEqual(r['cells'],3)
        self.assertAlmostEqual(r['group_component'],3200)
        self.assertAlmostEqual(r['date_component'],800)
        self.assertAlmostEqual(r['intersection_component'],2400)
        self.assertAlmostEqual(r['two_way_raw_variance'],1600)
    def test_balanced(self):
        r=weighted_components([('A','2025-09-01',1),('A','2025-09-02',3),('B','2025-09-01',5),('B','2025-09-02',7)])
        self.assertEqual(r['equal_group_mean_pp'],4)
        self.assertAlmostEqual(r['two_way_raw_variance'],1.25)
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):
            weighted_components([('A','2025-09-01',1),('A','2025-09-01',2)])
    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError,'invalid contrast'):
            weighted_components([('A','2025-09-01',float('nan'))])
    def test_bad_date(self):
        with self.assertRaises(ValueError):
            weighted_components([('A','2025-09-31',1)])
    def test_insufficient(self):
        with self.assertRaisesRegex(ValueError,'two groups'):
            weighted_components([('A','2025-09-01',1),('A','2025-09-02',2)])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'):
            weighted_components([])

if __name__=='__main__': unittest.main()
