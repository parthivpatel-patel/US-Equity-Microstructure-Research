import unittest
from scripts.phase339_correlation_tipping import audit
def fixture():
    rows=[]
    for outcome in ('count','volume'):
        for period in ('Jul-Sep','Jul-Oct'):
            for lag in (0,3,5,10,15):
                rows.append(dict(outcome=outcome,period=period,hac_lag=str(lag),dates='64' if period=='Jul-Sep' else '87',groups='68',slope_pp_per_trading_day='0.04' if period=='Jul-Sep' else '-0.01',two_way_se='0.01'))
    return rows
class Tests(unittest.TestCase):
    def test_grid(self): self.assertEqual(len(audit(fixture())),10)
    def test_duplicate(self):
        rows=fixture();rows.append(rows[0]);self.assertRaises(ValueError,audit,rows)
    def test_missing(self): self.assertRaises(ValueError,audit,fixture()[:-1])
    def test_invalid(self):
        rows=fixture();rows[0]['two_way_se']='NaN';self.assertRaises(ValueError,audit,rows)
    def test_tipping(self): self.assertTrue(all(x['classification']=='all admissible correlations' for x in audit(fixture())))
    def test_lag_invariance(self):
        rows=fixture();rows[1]['slope_pp_per_trading_day']='0.03';self.assertRaises(ValueError,audit,rows)
if __name__=='__main__':unittest.main()
