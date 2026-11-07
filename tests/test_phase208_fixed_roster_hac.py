"""Deterministic synthetic fixtures; NOT historical SEC estimates."""
import unittest
from datetime import date, timedelta
from scripts.phase208_fixed_roster_hac import analyze

DATES = []
d = date(2025,9,2)
while len(DATES) < 20:
    if d.weekday() < 5:
        DATES.append(d.isoformat())
    d += timedelta(days=1)

def panel():
    return [{"date":day,"security":s,"exchange":"X","group":"G","treatment":t,
             "outcome":"count","value":i+1 if t else 0}
            for i,day in enumerate(DATES) for s,t in (("A",1),("B",0))]

class Phase208Tests(unittest.TestCase):
    def test_complete(self):
        result = analyze(panel(),DATES,"count")
        self.assertEqual(result["n_dates"],20)
        self.assertFalse(result["causal_effect_established"])
    def test_missing(self):
        with self.assertRaises(ValueError): analyze(panel()[:-1],DATES,"count")
    def test_duplicate(self):
        rows=panel(); rows.append(rows[0])
        with self.assertRaises(ValueError): analyze(rows,DATES,"count")
    def test_assignment_switch(self):
        rows=panel(); rows[0]["treatment"]=0
        with self.assertRaises(ValueError): analyze(rows,DATES,"count")
    def test_wrong_outcome(self):
        with self.assertRaises(ValueError): analyze(panel(),DATES,"volume")
    def test_short_window(self):
        with self.assertRaises(ValueError): analyze(panel()[:4],DATES[:2],"count")
    def test_bad_lag(self):
        with self.assertRaises(ValueError): analyze(panel(),DATES,"count",lags=(20,))
    def test_unordered_dates(self):
        with self.assertRaises(ValueError): analyze(panel(),list(reversed(DATES)),"count")
    def test_multiple_hac_lags(self):
        self.assertEqual(len(analyze(panel(),DATES,"count",lags=(0,1,3))["hac_sensitivity"]),3)
    def test_constructed_mean(self):
        self.assertAlmostEqual(analyze(panel(),DATES,"count")["hac_sensitivity"][0]["mean"],10.5)

if __name__ == "__main__":
    unittest.main()
