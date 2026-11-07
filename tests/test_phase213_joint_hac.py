import unittest
from datetime import date, timedelta
from scripts.phase213_joint_hac import joint_window_hac

class JointHacTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{'date': (date(2025,9,1)+timedelta(days=i)).isoformat(), 'contrast': float(i%4 + (5 if i>=12 else 0))} for i in range(24)]
        self.early = ('2025-09-01','2025-09-10')
        self.late = ('2025-09-13','2025-09-24')
    def run_est(self, **kwargs):
        return joint_window_hac(self.rows,self.early,self.late,**kwargs)
    def test_finite(self):
        r=self.run_est(); self.assertTrue(all(v>=0 for v in r['hac_standard_errors'].values()))
    def test_mean(self):
        r=self.run_est(); self.assertAlmostEqual(r['late_minus_early'],r['late_mean']-r['early_mean'])
    def test_zero_lag(self):
        r=self.run_est(lags=(0,)); self.assertIn(0,r['hac_standard_errors'])
    def test_overlap(self):
        with self.assertRaises(ValueError): joint_window_hac(self.rows,self.early,('2025-09-10','2025-09-24'))
    def test_duplicate(self):
        with self.assertRaises(ValueError): joint_window_hac(self.rows+[self.rows[-1]],self.early,self.late)
    def test_nan(self):
        self.rows[0]['contrast']=float('nan')
        with self.assertRaises(ValueError): self.run_est()
    def test_reform(self):
        self.rows[-1]['date']='2025-11-03'
        with self.assertRaises(ValueError): self.run_est()
    def test_lag(self):
        with self.assertRaises(ValueError): self.run_est(lags=(24,))
    def test_small(self):
        with self.assertRaises(ValueError): self.run_est(min_per_window=13)
    def test_flags(self):
        self.assertFalse(self.run_est()['causal_effect_established'])

if __name__ == '__main__': unittest.main()
