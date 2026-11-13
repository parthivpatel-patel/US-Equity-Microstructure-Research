import csv
import io
import unittest
from phase337_covariance_comparison import audit

HEADER='outcome,period,hac_lag,slope_pp_per_trading_day,date_hac_se,two_way_se,dates,groups\n'
def rows():
    return list(csv.DictReader(io.StringIO(HEADER+''.join(
        f'{o},{p},{lag},0.03,0.01,0.02,64,68\n' for o in ('count','volume') for p in ('Jul-Sep','Jul-Oct') for lag in (0,3,5,10,15)))))
class AuditTests(unittest.TestCase):
    def test_complete_grid(self): self.assertEqual(len(audit(rows())),4)
    def test_ratio_and_disagreement(self):
        result=audit(rows())[0]
        self.assertEqual(result['min_two_way_over_date_hac_se'],'2.000000')
        self.assertEqual(result['lags_disagreeing_at_illustrative_1_96'],[0,3,5,10,15])
    def test_missing(self):
        with self.assertRaises(ValueError): audit(rows()[:-1])
    def test_duplicate(self):
        r=rows();r.append(r[0].copy())
        with self.assertRaises(ValueError): audit(r)
    def test_zero_se(self):
        r=rows();r[0]['date_hac_se']='0'
        with self.assertRaises(ValueError): audit(r)
    def test_nan(self):
        r=rows();r[0]['two_way_se']='NaN'
        with self.assertRaises(ValueError): audit(r)
    def test_slope_mismatch(self):
        r=rows();r[0]['slope_pp_per_trading_day']='0.04'
        with self.assertRaises(ValueError): audit(r)
    def test_count_mismatch(self):
        r=rows();r[0]['dates']='63'
        with self.assertRaises(ValueError): audit(r)
    def test_smaller_two_way(self):
        r=rows();r[0]['two_way_se']='0.005'
        self.assertEqual(audit(r)[0]['lags_two_way_se_smaller_than_date_hac'],[0])
if __name__=='__main__': unittest.main()
