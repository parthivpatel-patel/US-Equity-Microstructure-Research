"""Deterministic fixture checks for the published Phase 488 auditor."""
import csv,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase488_period_composition import audit

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.e=Path(self.tmp.name)/'e.csv';self.o=Path(self.tmp.name)/'o.csv'
        self.er=[('A','X','2025-10-01'),('A','X','2025-10-02'),('B','Y','2025-10-02'),('C','X','2025-10-01')]
        self.orows=[('A','X','2025-10-01','0'),('A','X','2025-10-02','1')]
        self.write()
    def write(self):
        for p,h,rows in [(self.e,['security','exchange','date'],self.er),
                         (self.o,['security','exchange','date','outcome'],self.orows)]:
            with p.open('w',newline='') as f:
                w=csv.writer(f);w.writerow(h);w.writerows(rows)
    def runaudit(self,cutoff='2025-10-02'):return audit(self.e,self.o,cutoff)
    def test_missing_and_zero(self):
        r=self.runaudit();self.assertEqual(r['pre']['observed_zero_cells'],1)
        self.assertEqual(r['post']['missing_eligible_cells'],1)
    def test_eligible_composition(self):
        self.assertEqual(self.runaudit()['eligible_unit_composition'],{'both':1,'pre_only':1,'post_only':1})
    def test_observed_composition(self):
        self.assertEqual(self.runaudit()['observed_unit_composition'],{'both':1,'pre_only':0,'post_only':0})
    def test_exchange(self):
        self.assertEqual(self.runaudit()['post']['by_exchange']['Y']['missing'],1)
    def test_outside(self):
        self.orows.append(('D','X','2025-10-02','1'));self.write()
        with self.assertRaises(ValueError):self.runaudit()
    def test_duplicate(self):
        self.er.append(self.er[0]);self.write()
        with self.assertRaises(ValueError):self.runaudit()
    def test_nonfinite(self):
        self.orows[0]=('A','X','2025-10-01','nan');self.write()
        with self.assertRaises(ValueError):self.runaudit()
    def test_cutoff_boundary(self):
        for c in ('2025-10-01','2025-10-03'):
            with self.assertRaises(ValueError):self.runaudit(c)
    def test_fingerprint(self):
        old=self.runaudit()['sha256']['panel']
        self.orows[1]=('A','X','2025-10-02','2');self.write()
        self.assertNotEqual(old,self.runaudit()['sha256']['panel'])
if __name__=='__main__':unittest.main()
