import csv, importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('mod',Path(__file__).resolve().parents[1] / 'scripts' / 'phase2_influence.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.p=Path(self.t.name)/'a.csv'
  self.rows=[dict(Ticker=x,treated=g,dr=v,dv=v,trades_pre=w,r_pre=.2,v_pre=.3) for x,g,v,w in [('A',1,.2,1),('B',1,.4,3),('C',0,.1,2),('D',0,.1,4)]]
 def tearDown(self):self.t.cleanup()
 def write(self):
  with self.p.open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=self.rows[0]);w.writeheader();w.writerows(self.rows)
 def test_gap(self):
  self.write();r=m.compute(self.p);self.assertAlmostEqual(r['dr']['equal_security_gap_pp'],20)
 def test_weighted(self):
  self.write();r=m.compute(self.p);self.assertAlmostEqual(r['dr']['pretrade_weighted_gap_pp'],25)
 def test_loo(self):
  self.write();r=m.compute(self.p);self.assertEqual(len(r['dr']['top_5_treated_weight_influence']),2)
 def test_duplicate(self):
  self.rows[-1]['Ticker']='A';self.write()
  with self.assertRaises(ValueError):m.compute(self.p)
 def test_nonfinite(self):
  self.rows[0]['dr']='nan';self.write()
  with self.assertRaises(ValueError):m.compute(self.p)
 def test_bad_group(self):
  self.rows[0]['treated']='2';self.write()
  with self.assertRaises(ValueError):m.compute(self.p)
 def test_bad_weight(self):
  self.rows[0]['trades_pre']=0;self.write()
  with self.assertRaises(ValueError):m.compute(self.p)
 def test_concentration(self):
  self.write();r=m.compute(self.p);self.assertAlmostEqual(r['treated_pretrade_weight_concentration']['top1_share'],.75)
if __name__=='__main__':unittest.main()
