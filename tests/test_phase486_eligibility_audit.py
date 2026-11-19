import csv,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase486_eligibility_audit import audit

class EligibilityTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup)
        self.e=Path(t.name)/'e.csv';self.p=Path(t.name)/'p.csv'
        self.write(self.e,['security','exchange','date'],[['A','X','2025-10-01'],['A','X','2025-10-02'],['B','Y','2025-10-02']])
        self.write(self.p,['security','exchange','date','outcome'],[['A','X','2025-10-01','0'],['B','Y','2025-10-02','2']])
    def write(self,p,h,rows):
        with p.open('w',newline='') as f:
            w=csv.writer(f);w.writerow(h);w.writerows(rows)
    def test_fixture(self):
        r=audit(self.e,self.p)
        self.assertEqual([r[x] for x in ('eligible','observed','missing','observed_zero','complete_eligible_units')],[3,2,1,1,1])
    def test_daily(self):
        self.assertEqual([r['missing'] for r in audit(self.e,self.p)['daily']],[0,1])
    def test_outside(self):
        with self.p.open('a') as f:f.write('Z,X,2025-10-02,3\n')
        with self.assertRaises(ValueError):audit(self.e,self.p)
    def test_duplicate_eligibility(self):
        with self.e.open('a') as f:f.write('A,X,2025-10-01\n')
        with self.assertRaises(ValueError):audit(self.e,self.p)
    def test_duplicate_observation(self):
        with self.p.open('a') as f:f.write('A,X,2025-10-01,0\n')
        with self.assertRaises(ValueError):audit(self.e,self.p)
    def test_nonfinite(self):
        with self.p.open('a') as f:f.write('A,X,2025-10-02,nan\n')
        with self.assertRaises(ValueError):audit(self.e,self.p)
    def test_bad_date(self):
        with self.e.open('a') as f:f.write('C,X,2025-02-30\n')
        with self.assertRaises(ValueError):audit(self.e,self.p)
    def test_hash(self):
        h=audit(self.e,self.p)['sha256']['panel']
        with self.p.open('a') as f:f.write('A,X,2025-10-02,1\n')
        self.assertNotEqual(h,audit(self.e,self.p)['sha256']['panel'])
if __name__=='__main__':unittest.main()
