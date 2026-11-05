"""Phase 170: fixed-calendar completeness audit. Constructed-data tests only."""
from datetime import date
import math
import unittest

def audit(rows, dates, groups):
    def parse(s):
        if not isinstance(s, str): raise ValueError("date type")
        try: d = date.fromisoformat(s)
        except ValueError as e: raise ValueError("invalid date") from e
        if d.isoformat() != s: raise ValueError("noncanonical date")
        return d
    ds = [parse(d) for d in dates]
    gs = list(groups)
    if not ds or len(set(ds)) != len(ds): raise ValueError("date roster")
    if not gs or len(set(gs)) != len(gs) or any(not isinstance(g,str) or not g.strip() for g in gs): raise ValueError("group roster")
    cells = set()
    for day,g,arm,value in rows:
        d = parse(day)
        if d not in ds or g not in gs: raise ValueError("outside roster")
        if type(arm) is not int or arm not in (0,1): raise ValueError("arm")
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value): raise ValueError("outcome")
        key = (d,g,arm)
        if key in cells: raise ValueError("duplicate cell")
        cells.add(key)
    out = []
    for d in sorted(ds):
        counts = [int((d,g,0) in cells) + int((d,g,1) in cells) for g in gs]
        c,p,a = (counts.count(n) for n in (2,1,0))
        out.append(dict(date=d.isoformat(), complete=c,partial=p,absent=a,roster=len(gs),coverage=c/len(gs)))
    return out

class Tests(unittest.TestCase):
    def setUp(self):
        self.ds = ["2025-10-01","2025-10-02","2025-10-03"]
        self.gs = ["A","B"]
        self.rows = [("2025-10-01","A",0,1),("2025-10-01","A",1,2),("2025-10-02","B",0,3)]
    def test_missing_entire_date(self):
        x = audit(self.rows,self.ds,self.gs)
        self.assertEqual([r["coverage"] for r in x],[.5,0,0])
        self.assertEqual(x[-1]["absent"],2)
    def test_partial(self):
        x = audit(self.rows,self.ds,self.gs)
        self.assertEqual((x[1]["partial"],x[1]["absent"]),(1,1))
    def test_complete(self):
        rows = [(d,g,a,1) for d in self.ds for g in self.gs for a in (0,1)]
        self.assertTrue(all(x["coverage"]==1 for x in audit(rows,self.ds,self.gs)))
    def test_duplicate_cell(self):
        with self.assertRaises(ValueError): audit(self.rows+[self.rows[0]],self.ds,self.gs)
    def test_duplicate_date(self):
        with self.assertRaises(ValueError): audit([],self.ds+[self.ds[0]],self.gs)
    def test_outside_roster(self):
        with self.assertRaises(ValueError): audit([("2025-10-04","A",0,1)],self.ds,self.gs)
    def test_bad_date(self):
        with self.assertRaises(ValueError): audit([],["2025-10-1"],self.gs)
    def test_bad_arm_and_value(self):
        for arm,value in ((True,1),(2,1),(0,float("nan"))):
            with self.subTest(arm=arm,value=value),self.assertRaises(ValueError):
                audit([("2025-10-01","A",arm,value)],self.ds,self.gs)
    def test_empty_rows(self):
        self.assertEqual([x["absent"] for x in audit([],self.ds,self.gs)],[2,2,2])
    def test_bad_groups(self):
        for gs in ([],["A","A"],[""]):
            with self.subTest(gs=gs),self.assertRaises(ValueError): audit([],self.ds,gs)

if __name__ == "__main__": unittest.main()
