import unittest
from phase263_roster_gate import audit

DATES = ["2025-10-06", "2025-10-07"]
def rows(pairs=("A","B"), dates=DATES):
    return [dict(date=d,pair_id=p,treated=1.0,control=0.0) for d in dates for p in pairs]
def run(r, dates=DATES, pairs=("A","B")):
    return audit(r,dates,pairs,"2025-10-07")

class GateTests(unittest.TestCase):
    def test_complete(self):
        x=run(rows()); self.assertTrue(x["structurally_complete"]); self.assertEqual(x["n_expected_cells"],4)
        self.assertFalse(x["historical_inference_authorized"])
    def test_entirely_missing_pair(self):
        self.assertEqual(len(run(rows(("A",)))["missing_cells"]),2)
    def test_missing_date(self):
        self.assertEqual(len(run(rows(dates=["2025-10-06"]))["missing_cells"]),2)
    def test_extra_pair(self):
        self.assertEqual(len(run(rows(("A","B","C")))["extra_cells"]),2)
    def test_duplicate(self):
        with self.assertRaises(ValueError): run(rows()+rows()[:1])
    def test_bool_rejected(self):
        r=rows();r[0]["treated"]=True
        with self.assertRaises(ValueError):run(r)
    def test_nan_rejected(self):
        r=rows();r[0]["control"]=float("nan")
        with self.assertRaises(ValueError):run(r)
    def test_duplicate_roster(self):
        with self.assertRaises(ValueError):run(rows(),pairs=("A","A"))
    def test_calendar_unsorted(self):
        with self.assertRaises(ValueError):run(rows(),dates=DATES[::-1])
    def test_cutoff_not_straddled(self):
        with self.assertRaises(ValueError):audit(rows(),DATES,["A","B"],"2025-10-09")
    def test_extra_session(self):
        self.assertEqual(len(run(rows(dates=DATES+["2025-10-08"]))["extra_cells"]),2)
    def test_empty_roster(self):
        with self.assertRaises(ValueError):run(rows(),pairs=())

if __name__=="__main__":unittest.main()
