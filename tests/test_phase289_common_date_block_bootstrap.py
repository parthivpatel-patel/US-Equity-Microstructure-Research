import unittest
from scripts.phase289_common_date_block_bootstrap import bootstrap_common_dates as boot

def panel(values):
    return {"source_authenticated":False,"pair_counts_by_exchange":{"X":3,"Y":1},
            "dates":[{"date":f"2025-09-{i+1:02d}","by_exchange":{"X":x,"Y":y}}
                     for i,(x,y) in enumerate(values)]}

class Tests(unittest.TestCase):
    def test_constant(self):
        self.assertEqual(boot(panel([(2,2)]*8),repetitions=99)["interval_95_percentile"],[2,2])
    def test_seed_deterministic(self):
        p=panel([(i,-i) for i in range(8)])
        self.assertEqual(boot(p,repetitions=101),boot(p,repetitions=101))
    def test_weighting(self):
        p=panel([(2,-2)]*8)
        self.assertEqual(boot(p)["mean"],1)
        self.assertEqual(boot(p,weighting="exchange")["mean"],0)
    def test_missing_exchange(self):
        p=panel([(1,2)]*3); del p["dates"][0]["by_exchange"]["Y"]
        with self.assertRaises(ValueError): boot(p)
    def test_duplicate_date(self):
        p=panel([(1,2)]*3); p["dates"][1]["date"]=p["dates"][0]["date"]
        with self.assertRaises(ValueError): boot(p)
    def test_nonfinite(self):
        p=panel([(1,2)]*3); p["dates"][0]["by_exchange"]["X"]=float("nan")
        with self.assertRaises(ValueError): boot(p)
    def test_invalid_provenance(self):
        p=panel([(1,2)]*3); p["source_authenticated"]=True
        with self.assertRaises(ValueError): boot(p)
    def test_block_too_long(self):
        with self.assertRaises(ValueError): boot(panel([(1,2)]*3),block_length=4)
    def test_bad_repetitions(self):
        with self.assertRaises(ValueError): boot(panel([(1,2)]*3),repetitions=1)
    def test_one_date(self):
        with self.assertRaises(ValueError): boot(panel([(1,2)]))
    def test_reject_bool_count(self):
        p=panel([(1,2)]*3); p["pair_counts_by_exchange"]["X"]=True
        with self.assertRaises(ValueError): boot(p)

if __name__=="__main__": unittest.main()
