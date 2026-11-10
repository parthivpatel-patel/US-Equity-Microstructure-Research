import unittest
from scripts.phase283_common_date_hac import common_date_hac

def panel(a,b):
    return {"source_authenticated":False,"pair_counts_by_exchange":{"X":2,"Y":1},
            "dates":[{"date":f"2025-09-{i+1:02d}","by_exchange":{"X":x,"Y":y}} for i,(x,y) in enumerate(zip(a,b))]}

class Tests(unittest.TestCase):
    def test_pair(self):
        self.assertAlmostEqual(common_date_hac(panel([1,3],[4,6]))["mean"],3)
    def test_exchange(self):
        self.assertAlmostEqual(common_date_hac(panel([1,3],[4,6]),weighting="exchange")["mean"],3.5)
    def test_lag_zero(self):
        self.assertAlmostEqual(common_date_hac(panel([1,3],[4,6]))["hac_standard_error"],1/2**.5)
    def test_lag_one(self):
        r=common_date_hac(panel([1,3,5],[1,3,5]),lag=1)
        self.assertAlmostEqual(r["hac_standard_error"]**2,(8/3)/3)
    def test_bad_lag(self):
        with self.assertRaises(ValueError): common_date_hac(panel([1],[1]),lag=1)
    def test_missing_exchange(self):
        p=panel([1],[2]);del p["dates"][0]["by_exchange"]["Y"]
        with self.assertRaises(ValueError):common_date_hac(p)
    def test_duplicate_date(self):
        p=panel([1,2],[2,3]);p["dates"][1]["date"]=p["dates"][0]["date"]
        with self.assertRaises(ValueError):common_date_hac(p)
    def test_nonfinite(self):
        p=panel([float("nan")],[2])
        with self.assertRaises(ValueError):common_date_hac(p)
    def test_authentication(self):
        p=panel([1],[2]);p["source_authenticated"]=True
        with self.assertRaises(ValueError):common_date_hac(p)

if __name__=="__main__":unittest.main()
