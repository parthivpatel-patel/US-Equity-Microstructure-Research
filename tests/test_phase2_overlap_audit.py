import importlib.util
import tempfile
import unittest
from pathlib import Path
import pandas as pd

MODULE=Path(__file__).resolve().parents[1]/'scripts'/'phase2_overlap_audit.py'
spec=importlib.util.spec_from_file_location('overlap',MODULE)
overlap=importlib.util.module_from_spec(spec)
spec.loader.exec_module(overlap)

class OverlapAuditTests(unittest.TestCase):
    def setUp(self):
        self.dir=tempfile.TemporaryDirectory()
        self.path=Path(self.dir.name)/'panel.csv'
        self.data=pd.DataFrame([
            dict(Ticker='T1',treated=1,r_pre=.5,v_pre=.6,trades_pre=100,days_pre=23,days_post=19),
            dict(Ticker='T2',treated=1,r_pre=.6,v_pre=.7,trades_pre=200,days_pre=23,days_post=19),
            dict(Ticker='C1',treated=0,r_pre=.2,v_pre=.3,trades_pre=10,days_pre=22,days_post=19),
            dict(Ticker='C2',treated=0,r_pre=.3,v_pre=.4,trades_pre=20,days_pre=23,days_post=19)])
    def tearDown(self):self.dir.cleanup()
    def write(self):self.data.to_csv(self.path,index=False)
    def test_counts_and_support(self):
        self.write();r=overlap.audit(self.path)
        self.assertEqual((r['n_treated'],r['n_controls']),(2,2))
        self.assertEqual(r['covariates']['r_pre']['treated_outside_control_minmax'],2)
        self.assertEqual(r['full_23_pre_19_post_days'],{'treated':2,'controls':1})
    def test_duplicate_rejected(self):
        self.data.loc[1,'Ticker']='T1';self.write()
        with self.assertRaises(ValueError):overlap.audit(self.path)
    def test_nonfinite_rejected(self):
        self.data.loc[1,'r_pre']=float('nan');self.write()
        with self.assertRaises(ValueError):overlap.audit(self.path)
    def test_bad_rate_rejected(self):
        self.data.loc[1,'v_pre']=1.2;self.write()
        with self.assertRaises(ValueError):overlap.audit(self.path)
    def test_invalid_treatment_rejected(self):
        self.data.loc[1,'treated']=3;self.write()
        with self.assertRaises(ValueError):overlap.audit(self.path)
if __name__=='__main__':unittest.main()
