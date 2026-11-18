"""Synthetic-data checks only. No historical SEC data used."""
import unittest
from datetime import date, timedelta
from scripts.phase451_block_bootstrap import analyze

def panel(n=12):
    out=[]
    for offset in range(n):
        for d in (date(2025,10,1)+timedelta(days=offset),date(2025,11,3)+timedelta(days=offset)):
            for s,t,y in [("T",True,5+int(d.month==11)*3),("C",False,2)]:
                out.append(dict(security=s,exchange="X",matched_group="G",date=d.isoformat(),treated=t,outcome=y))
    return out

class Tests(unittest.TestCase):
    def test_estimate(self): self.assertEqual(analyze(panel(),block_length=3,reps=100)["estimate"],3)
    def test_interval(self): self.assertEqual(analyze(panel(),block_length=3,reps=100)["percentile_95"],[3,3])
    def test_reproducible(self): self.assertEqual(analyze(panel(),block_length=3,reps=40,seed=8),analyze(panel()[::-1],block_length=3,reps=40,seed=8))
    def test_short(self):
        with self.assertRaisesRegex(ValueError,"insufficient"): analyze(panel(4),block_length=3)
    def test_duplicate(self):
        p=panel()
        with self.assertRaisesRegex(ValueError,"duplicate"): analyze(p+[p[0]],block_length=3)
    def test_global_treatment(self):
        p=panel(); p.append(dict(security="T",exchange="Y",matched_group="H",date="2025-10-20",treated=False,outcome=1))
        with self.assertRaisesRegex(ValueError,"global treatment"): analyze(p,block_length=3)
    def test_unstable(self):
        p=panel(); p.append(dict(security="T",exchange="X",matched_group="H",date="2025-10-20",treated=True,outcome=1))
        with self.assertRaisesRegex(ValueError,"unstable"): analyze(p,block_length=3)
    def test_invalid(self):
        p=panel(); p[0]["outcome"]=float("nan")
        with self.assertRaisesRegex(ValueError,"outcome"): analyze(p,block_length=3)
    def test_missing_date(self):
        p=[r for r in panel() if not (r["security"]=="T" and r["date"]=="2025-10-01")]
        self.assertEqual(analyze(p,block_length=3,reps=20)["excluded_unbalanced_calendar_dates"],1)
    def test_block_validation(self):
        with self.assertRaisesRegex(ValueError,"block_length"): analyze(panel(),block_length=0)
if __name__=="__main__": unittest.main()
