"""Synthetic characterization only; not historical market data."""
import unittest
from scripts.phase262_calendar_gate import validate
S=["2025-10-06","2025-10-07","2025-10-08","2025-10-09","2025-10-10"]
def rows(ds=S):
    return [{"date":d,"pair_id":p,"treated":1.0,"control":0.0} for d in ds for p in ("A","B")]
class TestCalendarGate(unittest.TestCase):
    def test_complete(self):
        x=validate(rows(),S,"2025-10-09")
        self.assertTrue(x["admitted"])
        self.assertFalse(x["calendar_authenticated"])
    def test_missing(self):
        x=validate(rows(S[:2]+S[3:]),S,"2025-10-09")
        self.assertEqual(x["missing_sessions"],["2025-10-08"])
        self.assertFalse(x["admitted"])
    def test_extra(self):
        self.assertEqual(validate(rows(S+["2025-10-13"]),S,"2025-10-09")["extra_sessions"],["2025-10-13"])
    def test_partial(self):
        self.assertEqual(validate(rows()[:-1],S,"2025-10-09")["partial_sessions"],{"2025-10-10":["B"]})
    def test_duplicate(self):
        with self.assertRaises(ValueError):validate(rows()+rows()[:1],S,"2025-10-09")
    def test_unsorted(self):
        with self.assertRaises(ValueError):validate(rows(),S[::-1],"2025-10-09")
    def test_duplicate_calendar(self):
        with self.assertRaises(ValueError):validate(rows(),S+[S[-1]],"2025-10-09")
    def test_nonfinite(self):
        r=rows();r[0]["treated"]=float("nan")
        with self.assertRaises(ValueError):validate(r,S,"2025-10-09")
    def test_empty(self):
        self.assertFalse(validate([],S,"2025-10-09")["admitted"])
    def test_boolean(self):
        r=rows();r[0]["control"]=True
        with self.assertRaises(ValueError):validate(r,S,"2025-10-09")
if __name__=="__main__":unittest.main()
