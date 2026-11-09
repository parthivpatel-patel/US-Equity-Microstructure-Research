"""Deterministic tests for phase269; no historical observations."""
import datetime as dt
import math
import unittest
from scripts.phase269_full_series_hac import daily_contrasts, full_series_hac

class TestFullSeriesHAC(unittest.TestCase):
    def setUp(self):
        self.dates=[dt.date(2025,10,27)+dt.timedelta(days=i) for i in range(8)]
        vals=[0,2,0,2,4,6,4,6]
        self.rows=[dict(date=str(d),pair=p,treated=str(v+offset),control=str(offset))
                   for d,v in zip(self.dates,vals) for p,offset in (("A",3),("B",8))]
        self.series=daily_contrasts(self.rows)
    def test_difference(self):
        self.assertAlmostEqual(full_series_hac(self.series,self.dates[4],0)["difference"],4)
    def test_lag_zero_se(self):
        self.assertAlmostEqual(full_series_hac(self.series,self.dates[4],0)["hac_se"],math.sqrt(.5))
    def test_cross_cutoff_component(self):
        r=full_series_hac(self.series,self.dates[4],1)
        self.assertNotEqual(r["cross_cutoff_component"],0)
    def test_incomplete_pair(self):
        with self.assertRaises(ValueError): daily_contrasts(self.rows[:-1])
    def test_duplicate_pair(self):
        with self.assertRaises(ValueError): daily_contrasts(self.rows+[self.rows[0]])
    def test_nonfinite(self):
        rows=[dict(r) for r in self.rows]
        rows[0]["treated"]="nan"
        with self.assertRaises(ValueError): daily_contrasts(rows)
    def test_invalid_lag(self):
        with self.assertRaises(ValueError): full_series_hac(self.series,self.dates[4],8)
    def test_too_few_period_dates(self):
        with self.assertRaises(ValueError): full_series_hac(self.series,self.dates[1],1)

if __name__=="__main__":
    unittest.main()
