import unittest
from phase242_placebo_scan import placebo_scan

class ScanTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{'date':f'2025-10-{d:02d}', 'equal_cell_contrast':float(d), 'pooled_count_contrast':float(2*d)} for d in range(1,9)]
    def test_known_linear_fixture(self):
        result=placebo_scan(self.rows,[2,3,6],2,0)
        self.assertEqual([r['cut_date'] for r in result['results']], ['2025-10-03','2025-10-04','2025-10-07'])
        self.assertTrue(all(abs(r['equal_cell_difference']-2)<1e-12 for r in result['results']))
        self.assertTrue(all(abs(r['pooled_count_difference']-4)<1e-12 for r in result['results']))
        self.assertFalse(result['source_authenticated'])
    def test_duplicate_cuts_rejected(self):
        with self.assertRaises(ValueError): placebo_scan(self.rows,[2,2],2,0)
    def test_out_of_bounds_rejected(self):
        with self.assertRaises(ValueError): placebo_scan(self.rows,[7],2,0)
    def test_invalid_bandwidth_rejected(self):
        with self.assertRaises(ValueError): placebo_scan(self.rows,[2],2,4)
    def test_unsorted_dates_rejected(self):
        with self.assertRaises(ValueError): placebo_scan(self.rows[::-1],[2],2,0)
    def test_nonfinite_contrast_rejected(self):
        self.rows[0]['equal_cell_contrast']=float('nan')
        with self.assertRaises(ValueError): placebo_scan(self.rows,[2],2,0)
if __name__=='__main__': unittest.main()
