import unittest
from datetime import date, timedelta
from scripts.phase211_preperiod_diagnostics import diagnose

BASE=date(2025,9,1)
def sample(vals):
    return [{"date":(BASE+timedelta(days=i)).isoformat(),"contrast":v} for i,v in enumerate(vals)]
def run(vals,a=(0,5),b=(6,11),**kw):
    d=sample(vals)
    return diagnose(d,(d[a[0]]["date"],d[a[1]]["date"]),(d[b[0]]["date"],d[b[1]]["date"]),**kw)
class Tests(unittest.TestCase):
    def test_linear(self):
        r=run(list(range(12)))
        self.assertEqual(r["placebo_mean_shift"],6)
        self.assertEqual(r["early"]["slope_per_observed_session"],1)
    def test_constant(self):
        self.assertEqual(run([4]*12)["placebo_mean_shift"],0)
    def test_negative_trend(self):
        self.assertEqual(run(list(range(12,0,-1)))["early"]["slope_per_observed_session"],-1)
    def test_overlap(self):
        with self.assertRaises(ValueError):run(list(range(12)),b=(5,11))
    def test_reverse(self):
        with self.assertRaises(ValueError):run(list(range(12)),a=(6,11),b=(0,5))
    def test_short(self):
        with self.assertRaises(ValueError):run(list(range(12)),a=(0,1))
    def test_duplicate(self):
        d=sample(range(12));d[1]["date"]=d[0]["date"]
        with self.assertRaises(ValueError):diagnose(d,(d[0]["date"],d[5]["date"]),(d[6]["date"],d[11]["date"]))
    def test_unsorted(self):
        d=sample(range(12));d[0],d[1]=d[1],d[0]
        with self.assertRaises(ValueError):diagnose(d,(d[0]["date"],d[5]["date"]),(d[6]["date"],d[11]["date"]))
    def test_nonfinite(self):
        with self.assertRaises(ValueError):run([float("nan")]+list(range(11)))
    def test_reform_intrusion(self):
        d=sample(range(12));d[-1]["date"]="2025-11-03"
        with self.assertRaises(ValueError):diagnose(d,(d[0]["date"],d[5]["date"]),(d[6]["date"],d[11]["date"]))
    def test_missing_boundary(self):
        d=sample(range(12))
        with self.assertRaises(ValueError):diagnose(d,("2025-08-31",d[5]["date"]),(d[6]["date"],d[11]["date"]))
    def test_invalid_min(self):
        with self.assertRaises(ValueError):run(list(range(12)),min_dates=2)
if __name__=="__main__":unittest.main()
