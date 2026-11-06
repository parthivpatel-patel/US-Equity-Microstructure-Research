import unittest
from scripts.phase200_common_date import common_date_contrasts as f
def r(d,g,t,v,o="count"): return dict(date=d,group=g,treatment=t,value=v,outcome=o)
class TestCommonDate(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError): f([])
    def test_balanced(self):
        self.assertEqual(f([r("d","a",1,5),r("d","a",0,2),r("d","b",1,8),r("d","b",0,4)])["date_contrasts"][0]["contrast"],3.5)
    def test_missing_arm(self):
        self.assertEqual(len(f([r("d","a",1,5),r("d","a",0,2),r("d","b",1,8)])["rejected_dates"]),1)
    def test_equal_group_weight(self):
        self.assertEqual(f([r("d","a",1,10),r("d","a",1,10),r("d","a",0,0),r("d","b",1,2),r("d","b",0,0)])["date_contrasts"][0]["contrast"],6)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): f([r("d","a",1,float("nan"))])
    def test_bool(self):
        with self.assertRaises(ValueError): f([r("d","a",True,1)])
    def test_outcomes(self):
        x=[r("d","a",1,3),r("d","a",0,1),r("d","a",1,8,"volume"),r("d","a",0,2,"volume")]
        self.assertEqual([z["contrast"] for z in f(x)["date_contrasts"]],[2,6])
    def test_roster_drift(self):
        x=[r("d1","a",1,3),r("d1","a",0,1),r("d2","b",1,3),r("d2","b",0,1)]
        self.assertEqual(len(f(x)["date_contrasts"]),0)
if __name__=="__main__": unittest.main()
