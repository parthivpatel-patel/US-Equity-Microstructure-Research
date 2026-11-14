"""Deterministic constructed-data checks; not SEC empirical estimates."""
import unittest
from scripts.phase352_calendar_serial import calendar_serial_components as calc
S=["2025-10-01","2025-10-02","2025-10-03","2025-10-06"]
R=[("a",S[0],2.),("a",S[2],4.),("b",S[0],6.),("b",S[2],8.)]
class TestCalendarSerial(unittest.TestCase):
    def test_gap_lag_one(self):
        r=calc(R,S,1)
        self.assertEqual(r["lag_products"][1],0.)
        self.assertEqual(r["missing_sessions"],[S[1],S[3]])
    def test_true_lag_two(self): self.assertNotEqual(calc(R,S,2)["lag_products"][2],0.)
    def test_mean(self): self.assertAlmostEqual(calc(R,S)["mean_pp"],5.)
    def test_order(self): self.assertEqual(calc(R,S)["lag_products"],calc(list(reversed(R)),S)["lag_products"])
    def test_duplicate(self):
        with self.assertRaises(ValueError): calc(R+[R[0]],S)
    def test_off_calendar(self):
        with self.assertRaises(ValueError): calc(R+[("c","2025-10-04",1.)],S)
    def test_calendar_order(self):
        with self.assertRaises(ValueError): calc(R,list(reversed(S)))
    def test_bool(self):
        with self.assertRaises(ValueError): calc([("a",S[0],True)]+R[1:],S)
    def test_lag_bool(self):
        with self.assertRaises(ValueError): calc(R,S,True)
    def test_one_group(self):
        with self.assertRaises(ValueError): calc(R[:2],S)
if __name__=="__main__": unittest.main()
