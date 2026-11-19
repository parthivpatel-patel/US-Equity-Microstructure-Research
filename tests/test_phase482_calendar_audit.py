import csv, os, sys, tempfile, unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","scripts"))
from phase482_calendar_audit import audit
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory(); self.addCleanup(self.t.cleanup)
  self.c=self.write("cal.csv",["date"],[["2025-10-01"],["2025-10-02"],["2025-10-03"]])
  self.rows=[["A","2025-10-01","X","0"],["A","2025-10-02","X","1"],["A","2025-10-03","X","2"],["B","2025-10-01","X","3"]]
 def write(self,n,h,rows):
  p=os.path.join(self.t.name,n)
  with open(p,"w",newline="") as f:
   w=csv.writer(f);w.writerow(h);w.writerows(rows)
  return p
 def panel(self,rows=None): return self.write("panel.csv",["security","date","exchange","value"],self.rows if rows is None else rows)
 def test_counts(self):
  x=audit(self.panel(),self.c,"2025-10-02")
  self.assertEqual((x["observed_rows"],x["absent_union_grid_rows"],x["observed_zeros"]),(4,2,1))
  self.assertEqual(x["coverage_categories"]["complete_both"],1)
 def test_duplicate(self):
  with self.assertRaises(ValueError):audit(self.panel(self.rows+[self.rows[0]]),self.c,"2025-10-02")
 def test_nonfinite(self):
  with self.assertRaises(ValueError):audit(self.panel([["A","2025-10-01","X","nan"]]),self.c,"2025-10-02")
 def test_off_calendar(self):
  with self.assertRaises(ValueError):audit(self.panel([["A","2025-10-04","X","1"]]),self.c,"2025-10-02")
 def test_bad_calendar(self):
  c=self.write("bad.csv",["date"],[["2025-10-02"],["2025-10-01"]])
  with self.assertRaises(ValueError):audit(self.panel(),c,"2025-10-02")
 def test_bad_cutoff(self):
  with self.assertRaises(ValueError):audit(self.panel(),self.c,"2025-10-05")
if __name__=="__main__":unittest.main()
