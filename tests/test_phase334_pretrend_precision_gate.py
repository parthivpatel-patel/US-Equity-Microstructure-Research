import unittest
from phase334_pretrend_precision_gate import audit

def fixture():
    return [dict(outcome=o,period=p,hac_lag=str(l),slope_pp_per_trading_day="0.1",
                 two_way_se="0.02",two_way_ci_low="0.06",two_way_ci_high="0.14")
            for o in ("count","volume") for p in ("Jul-Sep","Jul-Oct") for l in (0,3,5,10,15)]

class TestAudit(unittest.TestCase):
    def test_valid_grid(self): self.assertEqual(len(audit(fixture())),4)
    def test_duplicate_lag(self):
        r=fixture(); r.append(r[0].copy())
        with self.assertRaises(ValueError): audit(r)
    def test_missing_lag(self):
        with self.assertRaises(ValueError): audit(fixture()[:-1])
    def test_invalid_interval(self):
        r=fixture(); r[0]["two_way_ci_low"]="0.11"
        with self.assertRaises(ValueError): audit(r)
    def test_inconsistent_slope(self):
        r=fixture(); r[0]["slope_pp_per_trading_day"]="0.2"
        with self.assertRaises(ValueError): audit(r)
    def test_zero_crossing(self):
        r=fixture(); r[0]["two_way_ci_low"]="-0.01"
        x=audit(r)
        self.assertFalse(next(y for y in x if y["outcome"]=="count" and y["period"]=="Jul-Sep")["zero_excluded_all_lags"])

if __name__ == "__main__": unittest.main()
