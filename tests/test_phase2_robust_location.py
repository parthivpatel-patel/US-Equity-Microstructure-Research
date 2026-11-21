import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

path=Path(__file__).resolve().parents[1]/'scripts'/'phase2_robust_location.py'
spec=importlib.util.spec_from_file_location('robust',path)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class RobustTest(unittest.TestCase):
    def test_trim(self):
        self.assertEqual(mod.trimmed_mean([1,2,3,4,100],.2),3)
    def test_untrimmed(self):
        self.assertAlmostEqual(mod.trimmed_mean([1,2,3],0),2)
    def test_invalid(self):
        with self.assertRaises(ValueError):mod.trimmed_mean([1,2],.5)
    def test_empty(self):
        with self.assertRaises(ValueError):mod.trimmed_mean([],0)
    def test_nonfinite(self):
        with self.assertRaises(ValueError):mod.trimmed_mean([1,float('nan')],0)
    def test_small_group(self):
        self.assertAlmostEqual(mod.trimmed_mean([1,2,3],.2),2)
    def test_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['Ticker','treated','dr','dv','r_pre','r_post','v_pre','v_post']);w.writeheader()
                for ticker,t,delta in [('A',1,.2),('B',0,.1)]:
                    w.writerow(dict(Ticker=ticker,treated=t,dr=delta,dv=delta,r_pre=.2,r_post=.2+delta,v_pre=.2,v_post=.2+delta))
            r=mod.analyze(p)
            self.assertEqual(r['n_treated'],1)
            self.assertAlmostEqual(r['location_sensitivity'][0]['treated_minus_control_pp'],10)
    def test_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['Ticker','treated','dr','dv','r_pre','r_post','v_pre','v_post']);w.writeheader()
                for t in [1,0]:w.writerow(dict(Ticker='A',treated=t,dr=.1,dv=.1,r_pre=.2,r_post=.3,v_pre=.2,v_post=.3))
            with self.assertRaisesRegex(ValueError,'duplicate'):mod.analyze(p)
if __name__=='__main__':unittest.main()
