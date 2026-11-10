import unittest
from phase282_calendar_admission import admit_exchange_panel
S=["2025-09-02","2025-09-03"]
C={"X":2,"Y":1}
R=[{"date":s,"exchange":e,"contrast":v} for s in S for e,v in [("X",1),("Y",-1)]]
class TestAdmission(unittest.TestCase):
    def reject(self, rows=R, sessions=S, counts=C):
        with self.assertRaises(ValueError): admit_exchange_panel(rows,sessions,counts)
    def test_valid(self):
        a=admit_exchange_panel(R,S,C)
        self.assertEqual(len(a["dates"]),2)
        self.assertFalse(a["source_authenticated"])
    def test_missing(self): self.reject(R[:-1])
    def test_duplicate(self): self.reject(R+[R[0]])
    def test_extra(self): self.reject(R+[{"date":"2025-09-04","exchange":"X","contrast":1}])
    def test_reverse(self): self.reject(R,S[::-1])
    def test_duplicate_session(self): self.reject(R,S+[S[0]])
    def test_nan(self): self.reject(R[:-1]+[{**R[-1],"contrast":float("nan")}])
    def test_bool(self): self.reject(R[:-1]+[{**R[-1],"contrast":True}])
    def test_bad_count(self): self.reject(R,S,{"X":True,"Y":1})
    def test_schema(self): self.reject(R[:-1]+[{**R[-1],"secret":0}])
    def test_row_order(self):
        self.assertEqual(admit_exchange_panel(R[::-1],S,C),admit_exchange_panel(R,S,C))
if __name__=="__main__": unittest.main()
