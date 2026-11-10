"""Synthetic regression tests; not historical SEC evidence."""
import datetime as dt
import unittest
from scripts.phase277_exchange_balance import audit_panel

D=(dt.date(2025,9,2),dt.date(2025,9,3))
P=(("a","X"),("b","X"),("c","Y"))
def sample():
    return [dict(date=d.isoformat(),pair=p,exchange=e,treated=t,control=0)
            for d in D for p,e,t in [("a","X",1),("b","X",3),("c","Y",9)]]

class AuditTests(unittest.TestCase):
    def test_weighting(self):
        x=audit_panel(sample(),D,P)["dates"][0]
        self.assertAlmostEqual(x["pair_weighted"],13/3)
        self.assertAlmostEqual(x["exchange_equal"],5.5)
    def test_count(self):
        self.assertEqual(audit_panel(sample(),D,P)["expected_observations"],6)
    def test_fail_closed(self):
        self.assertFalse(audit_panel(sample(),D,P)["historical_inference_authorized"])
    def test_missing(self):
        with self.assertRaises(ValueError): audit_panel(sample()[:-1],D,P)
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit_panel(sample()+sample()[:1],D,P)
    def test_wrong_exchange(self):
        r=sample();r[0]["exchange"]="Y"
        with self.assertRaises(ValueError): audit_panel(r,D,P)
    def test_unexpected_date(self):
        r=sample();r[0]["date"]="2025-09-04"
        with self.assertRaises(ValueError): audit_panel(r,D,P)
    def test_nonfinite(self):
        r=sample();r[0]["treated"]="nan"
        with self.assertRaises(ValueError): audit_panel(r,D,P)
    def test_duplicate_roster(self):
        with self.assertRaises(ValueError): audit_panel(sample(),D,P+P[:1])
    def test_reassigned_pair(self):
        with self.assertRaises(ValueError): audit_panel(sample(),D,(("a","X"),("a","Y")))
    def test_unsorted_dates(self):
        with self.assertRaises(ValueError): audit_panel(sample(),D[::-1],P)
    def test_empty(self):
        with self.assertRaises(ValueError): audit_panel([],D,())

if __name__=="__main__": unittest.main()
