"""Deterministic fixture tests for Phase 178 published-table auditor."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from phase178_window_audit import audit

HEADER=["outcome","window_days","november_pp","october6_pp","pre_placebo_count","pre_placebo_at_least_as_negative","pre_placebo_at_least_as_extreme_abs","nov_minus_oct_pp"]
BASE=["count","5","-1.335781","-0.601120","78","2","2","-0.734661"]

class AuditTests(unittest.TestCase):
    def check(self,rows,fails=False):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"input.csv"
            with p.open("w",newline="") as f:
                writer=csv.writer(f);writer.writerow(HEADER);writer.writerows(rows)
            if fails:
                with self.assertRaises(ValueError):audit(p)
            else:return audit(p)
    def test_valid(self):
        result=self.check([BASE])
        self.assertEqual(result["count"]["negative_windows"],1)
        self.assertAlmostEqual(result["count"]["windows"][0]["absolute_placebo_fraction"],2/78)
    def test_duplicate(self):self.check([BASE,BASE],True)
    def test_empty(self):self.check([],True)
    def test_bad_count(self):
        x=BASE.copy();x[6]="79";self.check([x],True)
    def test_bad_delta(self):
        x=BASE.copy();x[7]="0.1";self.check([x],True)
    def test_bad_window(self):
        x=BASE.copy();x[1]="0";self.check([x],True)
    def test_nonfinite(self):
        x=BASE.copy();x[2]="nan";self.check([x],True)
    def test_two_windows(self):
        x=BASE.copy();x[1]="10";x[2]="-1.0";x[3]="-1.2";x[7]="0.2"
        result=self.check([x,BASE])
        self.assertEqual(result["count"]["positive_windows"],1)

if __name__=="__main__":unittest.main()
