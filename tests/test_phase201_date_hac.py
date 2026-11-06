import unittest
from phase201_date_hac import date_hac

class TestDateHAC(unittest.TestCase):
    def setUp(self):
        self.rows = [{"date": f"2025-10-{d:02d}", "contrast": x} for d, x in [(1,1),(2,2),(3,3),(6,4)]]
    def test_mean(self):
        self.assertEqual(date_hac(self.rows,0)["mean"],2.5)
    def test_lag_zero(self):
        self.assertAlmostEqual(date_hac(self.rows,0)["hac_se"],(1.25/4)**.5)
    def test_lag_one(self):
        self.assertAlmostEqual(date_hac(self.rows,1)["hac_se"],(1.5625/4)**.5)
    def test_bad_lag(self):
        for lag in [-1,4,1.0,True]:
            with self.subTest(lag=lag), self.assertRaises(ValueError): date_hac(self.rows,lag)
    def test_duplicate_date(self):
        with self.assertRaises(ValueError): date_hac([self.rows[0],self.rows[0]],0)
    def test_unsorted(self):
        with self.assertRaises(ValueError): date_hac(list(reversed(self.rows)),0)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): date_hac([self.rows[0],{"date":"2025-10-02","contrast":float("nan")}],0)
    def test_too_few(self):
        with self.assertRaises(ValueError): date_hac(self.rows[:1],0)

if __name__ == "__main__": unittest.main()
