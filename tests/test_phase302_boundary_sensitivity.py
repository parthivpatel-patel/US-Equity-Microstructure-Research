import unittest
from scripts.phase302_boundary_sensitivity import exact_block_means, exact_summary

class BoundaryAudit(unittest.TestCase):
    def test_all_constant(self):
        for circular in (False, True):
            self.assertEqual(set(exact_block_means([4,4,4,4],2,circular)), {4.0})
    def test_exact_draw_counts(self):
        self.assertEqual(len(exact_block_means([0,0,0,12],2,False)),9)
        self.assertEqual(len(exact_block_means([0,0,0,12],2,True)),16)
    def test_boundary_example(self):
        r=exact_summary([0,0,0,12],2)
        self.assertEqual(r['noncircular']['mean'],2)
        self.assertEqual(r['circular']['mean'],3)
        self.assertEqual(r['noncircular']['p975'],3)
        self.assertEqual(r['circular']['p975'],6)
    def test_invalid_length(self):
        for length in (0,5):
            with self.assertRaises(ValueError):
                exact_block_means([1,2,3,4],length,True)
if __name__=='__main__': unittest.main()
