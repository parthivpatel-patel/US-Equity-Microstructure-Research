import math
import unittest
from phase267_date_cluster import analyze

DATES = ["2025-10-20","2025-10-21","2025-10-22","2025-10-23","2025-10-24","2025-10-27"]
def panel(a=(0,0,0,2,2,2)):
    return [(d,p,v) for d,v in zip(DATES,a) for p in ("a","b")]

class Tests(unittest.TestCase):
    def test_step(self):
        r=analyze(panel(),"2025-10-23",0)
        self.assertEqual(r["estimate"],2)
        self.assertEqual(r["hac_se"],0)
    def test_no_change(self):
        self.assertEqual(analyze(panel((1,1,1,1,1,1)),"2025-10-23")["estimate"],0)
    def test_pair_offset(self):
        rows=[(d,p,v+(5 if p=="a" else -5)) for d,p,v in panel()]
        self.assertEqual(analyze(rows,"2025-10-23")["estimate"],2)
    def test_missing(self):
        with self.assertRaises(ValueError): analyze(panel()[:-1],"2025-10-23")
    def test_duplicate(self):
        rows=panel()
        with self.assertRaises(ValueError): analyze(rows+[rows[0]],"2025-10-23")
    def test_invalid(self):
        rows=panel(); rows[0]=(rows[0][0],rows[0][1],float("nan"))
        with self.assertRaises(ValueError): analyze(rows,"2025-10-23")
    def test_small_side(self):
        with self.assertRaises(ValueError): analyze(panel(),"2025-10-24")
    def test_bad_lag(self):
        with self.assertRaises(ValueError): analyze(panel(),"2025-10-23",6)
    def test_positive_se(self):
        r=analyze(panel((0,1,0,3,2,4)),"2025-10-23",1)
        self.assertTrue(math.isfinite(r["hac_se"]) and r["hac_se"]>=0)

if __name__=="__main__": unittest.main()
