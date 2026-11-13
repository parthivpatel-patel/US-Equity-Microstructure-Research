import csv
import io
import unittest
from phase336_threshold_margin import audit

HEADER='outcome,period,hac_lag,slope_pp_per_trading_day,two_way_se,dates,groups\n'
def rows():
    return list(csv.DictReader(io.StringIO(HEADER+''.join(
        f'{o},{p},{lag},0.03,0.01,64,68\n' for o in ('count','volume') for p in ('Jul-Sep','Jul-Oct') for lag in (0,3,5,10,15)))))
class AuditTests(unittest.TestCase):
    def test_grid(self): self.assertEqual(len(audit(rows())),4)
    def test_duplicate(self):
        r=rows();r.append(r[0].copy())
        with self.assertRaises(ValueError): audit(r)
    def test_missing(self):
        with self.assertRaises(ValueError): audit(rows()[:-1])
    def test_zero_se(self):
        r=rows();r[0]['two_way_se']='0'
        with self.assertRaises(ValueError): audit(r)
    def test_nonfinite(self):
        r=rows();r[0]['slope_pp_per_trading_day']='nan'
        with self.assertRaises(ValueError): audit(r)
    def test_cluster_mismatch(self):
        r=rows();r[0]['dates']='63'
        with self.assertRaises(ValueError): audit(r)
    def test_threshold(self):
        r=rows();r[0]['two_way_se']='0.015'
        self.assertFalse(audit(r)[1]['all_lags_exceed']['2.0'])
if __name__=='__main__': unittest.main()
