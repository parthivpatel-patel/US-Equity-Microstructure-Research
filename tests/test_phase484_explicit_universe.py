"""Constructed CSV fixtures only; no historical SEC observations."""
import tempfile, unittest
from pathlib import Path
from scripts.phase484_explicit_universe import audit

class CoverageTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup)
        root=Path(t.name)
        self.p=root/"panel.csv";self.c=root/"calendar.csv";self.u=root/"universe.csv"
        self.c.write_text("date\n2025-10-01\n2025-10-02\n")
        self.u.write_text("security,exchange\nA,X\nB,Y\n")
        self.p.write_text("security,date,exchange,value\nA,2025-10-01,X,0\nA,2025-10-02,X,1\nB,2025-10-01,Y,2\n")
    def run_audit(self):return audit(self.p,self.c,self.u)
    def test_coverage(self):
        r=self.run_audit()
        self.assertEqual((r["expected_cells"],r["missing_cells"],r["observed_zero_cells"],r["complete_units"]),(4,1,1,1))
        self.assertEqual(r["daily_observed_cells"]["2025-10-02"],1)
    def test_hash_changes(self):
        h=self.run_audit()["sha256"]["panel"]
        self.p.write_text(self.p.read_text().replace(",Y,2",",Y,3"))
        self.assertNotEqual(h,self.run_audit()["sha256"]["panel"])
    def test_duplicate_panel(self):
        self.p.write_text(self.p.read_text()+"A,2025-10-01,X,0\n")
        with self.assertRaises(ValueError):self.run_audit()
    def test_duplicate_universe(self):
        self.u.write_text(self.u.read_text()+"A,X\n")
        with self.assertRaises(ValueError):self.run_audit()
    def test_nonfinite(self):
        self.p.write_text(self.p.read_text().replace(",X,1",",X,nan"))
        with self.assertRaises(ValueError):self.run_audit()
    def test_outside_universe(self):
        self.p.write_text(self.p.read_text().replace("B,2025-10-01,Y","C,2025-10-01,Y"))
        with self.assertRaises(ValueError):self.run_audit()
    def test_ragged(self):
        self.p.write_text(self.p.read_text()+"A,2025-10-02,X\n")
        with self.assertRaises(ValueError):self.run_audit()

if __name__=="__main__":unittest.main()
