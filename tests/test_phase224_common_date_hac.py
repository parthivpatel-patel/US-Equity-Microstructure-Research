import unittest
from scripts.phase224_common_date_hac import common_date_hac

D = ['2025-10-01','2025-10-02','2025-10-03','2025-10-06','2025-10-07','2025-10-08']

def rows(v):
    return [dict(date=d,equal_cell_contrast=x,pooled_count_contrast=2*x) for d,x in zip(D,v)]

class CommonDateHACTests(unittest.TestCase):
    def calc(self,v,lag=0):
        return common_date_hac(rows(v),D[:3],D[3:],lag)
    def test_exact_mean_difference(self):
        x=self.calc([1,2,3,4,5,6])
        self.assertAlmostEqual(x['equal_cell_contrast']['difference'],3)
        self.assertAlmostEqual(x['pooled_count_contrast']['difference'],6)
    def test_lag_zero_independent_reference(self):
        x=self.calc([1,2,3,4,5,6])['equal_cell_contrast']
        self.assertAlmostEqual(x['hac_variance'],4/9)
    def test_full_series_cross_window_covariance(self):
        x=self.calc([1,2,3,4,5,6],1)['equal_cell_contrast']
        self.assertAlmostEqual(x['hac_variance'],5/9)
    def test_constant_windows(self):
        x=self.calc([1,1,1,4,4,4],2)['equal_cell_contrast']
        self.assertEqual(x['hac_se'],0)
    def test_reject_missing_common_date(self):
        with self.assertRaises(ValueError):
            common_date_hac(rows([1,2,3,4,5,6])[:-1],D[:3],D[3:],0)
    def test_reject_overlap(self):
        with self.assertRaises(ValueError):
            common_date_hac(rows([1,2,3,4,5,6]),D[:3],D[2:],0)
    def test_reject_invalid_bandwidth(self):
        with self.assertRaises(ValueError):
            self.calc([1,2,3,4,5,6],6)
    def test_no_authentication(self):
        self.assertFalse(self.calc([1,2,3,4,5,6])['source_authenticated'])

if __name__=='__main__':
    unittest.main()
