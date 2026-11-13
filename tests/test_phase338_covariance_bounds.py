import csv
import io
import unittest
from phase338_covariance_bounds import audit

HEADER='outcome,period,dates,groups,hac_lag,slope_pp_per_trading_day,two_way_se\n'
def fixture():
    rows=[]
    for outcome in ('count','volume'):
        for period in ('Jul-Sep','Jul-Oct'):
            for lag in (0,3,5,10,15):
                slope = '.03' if period == 'Jul-Sep' else '-.01'
                rows.append(f'{outcome},{period},64,68,{lag},{slope},.01')
    return list(csv.DictReader(io.StringIO(HEADER+'\n'.join(rows))))

class Tests(unittest.TestCase):
    def test_bounds(self):
        x=audit(fixture())
        self.assertEqual(len(x),10)
        self.assertEqual(x[0]['se_lower_bound'],'0.00')
        self.assertEqual(x[0]['se_upper_bound'],'0.02')
        self.assertEqual(x[0]['minimum_abs_slope_change_over_se'],'2.000000')
        self.assertTrue(x[0]['guaranteed_above_illustrative_1_96'])
    def test_missing(self):
        with self.assertRaises(ValueError): audit(fixture()[:-1])
    def test_duplicate(self):
        r=fixture();r.append(r[0])
        with self.assertRaises(ValueError): audit(r)
    def test_zero_se(self):
        r=fixture();r[0]['two_way_se']='0'
        with self.assertRaises(ValueError): audit(r)
    def test_nonfinite(self):
        r=fixture();r[0]['two_way_se']='NaN'
        with self.assertRaises(ValueError): audit(r)
    def test_lag_slope_drift(self):
        r=fixture();r[1]['slope_pp_per_trading_day']='.02'
        with self.assertRaises(ValueError): audit(r)
    def test_sample_count_drift(self):
        r=fixture();r[1]['dates']='65'
        with self.assertRaises(ValueError): audit(r)

if __name__=='__main__': unittest.main()
