"""Constructed-data tests only; no historical SEC data."""
import unittest
from scripts.phase450_paired_estimator import estimate
def r(s,d,t,y,e="X",g="G"):
    return dict(security=s,date=d,treated=t,outcome=y,exchange=e,matched_group=g)
class Tests(unittest.TestCase):
    def setUp(self):
        self.rows=[r("T","2025-10-31",True,4),r("C","2025-10-31",False,2),r("T","2025-11-03",True,8),r("C","2025-11-03",False,3)]
    def test_did(self): self.assertEqual(estimate(self.rows)["estimate"],3)
    def test_order(self): self.assertEqual(estimate(self.rows[::-1])["estimate"],3)
    def test_unpaired(self): self.assertEqual(estimate(self.rows+[r("T","2025-11-04",True,99)])["estimate"],3)
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,"duplicate"): estimate(self.rows+self.rows[:1])
    def test_nan(self):
        with self.assertRaisesRegex(ValueError,"finite"): estimate(self.rows[:-1]+[r("C","2025-11-03",False,float("nan"))])
    def test_unstable(self):
        with self.assertRaisesRegex(ValueError,"unstable"): estimate(self.rows+[r("T","2025-11-04",False,2)])
    def test_no_support(self):
        with self.assertRaisesRegex(ValueError,"no stratum"): estimate(self.rows[:2])
    def test_bootstrap(self):
        a=estimate(self.rows,bootstrap_reps=120,seed=7)
        self.assertEqual(a,estimate(self.rows,bootstrap_reps=120,seed=7))
        self.assertEqual(a["bootstrap_percentile_95"],[3,3])
    def test_equal_strata(self):
        extra=[r("U","2025-10-31",True,10,"Y"),r("V","2025-10-31",False,0,"Y"),r("U","2025-11-03",True,10,"Y"),r("V","2025-11-03",False,0,"Y")]
        self.assertEqual(estimate(self.rows+extra)["estimate"],1.5)
    def test_bool_outcome(self):
        with self.assertRaisesRegex(ValueError,"finite"): estimate(self.rows[:-1]+[r("C","2025-11-03",False,True)])
if __name__=="__main__": unittest.main()
