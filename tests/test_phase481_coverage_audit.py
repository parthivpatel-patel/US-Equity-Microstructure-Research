import csv
import pathlib
import tempfile
import unittest
from scripts.phase481_coverage_audit import audit

class CoverageAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=pathlib.Path(self.tmp.name)/"panel.csv"
    def tearDown(self): self.tmp.cleanup()
    def write(self,rows):
        with self.path.open("w",newline="") as f:
            w=csv.writer(f);w.writerow(["security","date","exchange","value","source_id"]);w.writerows(rows)
    def test_missing_not_zero(self):
        self.write([["A","2025-10-01","X",0,"s"],["B","2025-10-01","X",2,"s"],["A","2025-10-02","X",3,"s"]])
        r=audit(self.path)
        self.assertEqual(r["observed_zero_rows"],1)
        self.assertEqual(r["complete_units_across_observed_dates"],1)
        self.assertEqual(r["daily"][1]["coverage_fraction_of_union"],.5)
    def test_duplicates_rejected(self):
        row=["A","2025-10-01","X",1,"s"];self.write([row,row])
        with self.assertRaisesRegex(ValueError,"duplicate"):audit(self.path)
    def test_nonfinite_rejected(self):
        self.write([["A","2025-10-01","X","nan","s"]])
        with self.assertRaisesRegex(ValueError,"nonfinite"):audit(self.path)
    def test_invalid_date_rejected(self):
        self.write([["A","2025-13-01","X",1,"s"]])
        with self.assertRaisesRegex(ValueError,"invalid date"):audit(self.path)
    def test_exchange_unit_separation(self):
        self.write([["A","2025-10-01","X",1,"s"],["A","2025-10-01","Y",1,"s"]])
        self.assertEqual(audit(self.path)["unique_security_exchange_units"],2)

if __name__=="__main__":unittest.main()
