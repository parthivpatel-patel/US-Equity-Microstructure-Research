import unittest
from scripts.phase458_placebo_pretrend import diagnostics

def fixture():
    rows=[]
    for d,y in zip(["2025-09-02","2025-09-03","2025-10-01","2025-10-02","2025-11-04"],[1,3,6,8,999]):
        rows.extend([dict(security="T",exchange="X",matched_group="G",date=d,treated=True,outcome=y),dict(security="C",exchange="X",matched_group="G",date=d,treated=False,outcome=0)])
    return rows

class TestPlacebo(unittest.TestCase):
    def test_placebo(self): self.assertEqual(diagnostics(fixture())["equal_group_placebo_mean"],5)
    def test_slope(self): self.assertEqual(diagnostics(fixture())["groups"][0]["pretrend_slope_per_day"],2)
    def test_post_ignored(self): self.assertEqual(diagnostics(fixture()[:-2])["equal_group_placebo_mean"],diagnostics(fixture())["equal_group_placebo_mean"])
    def test_duplicate(self):
        with self.assertRaises(ValueError): diagnostics(fixture()+fixture()[:1])
    def test_conflict(self):
        x=fixture(); x[0]["treated"]=False
        with self.assertRaises(ValueError): diagnostics(x)
    def test_support(self): self.assertEqual(diagnostics(fixture(),min_dates=3)["eligible_groups"],0)
    def test_nonfinite(self):
        x=fixture(); x[0]["outcome"]=float("nan")
        with self.assertRaises(ValueError): diagnostics(x)
    def test_cutoff(self):
        with self.assertRaises(ValueError): diagnostics(fixture(),placebo="2025-12-01")
    def test_no_pairs(self): self.assertEqual(diagnostics(fixture()[::2])["eligible_groups"],0)
