"""Fixture checks; these do not authenticate original SEC observations."""
import sys, tempfile, unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase398_panel_audit import audit
class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'panel.csv'
        self.d=pd.DataFrame({'Ticker':['A','B','C','D'],'treated':[1,1,0,0],
        'r_pre':[.2,.3,.4,.5],'r_post':[.3,.45,.4,.55],
        'v_pre':[.1,.2,.3,.4],'v_post':[.2,.35,.3,.45],
        'days_pre':[23]*4,'days_post':[19]*4,'trades_pre':[10,20,30,40],
        'trades_post':[10,20,30,40],'dr':[.1,.15,0,.05],'dv':[.1,.15,0,.05]})
    def check(self):
        self.d.to_csv(self.path,index=False);return audit(self.path)
    def test_valid(self): self.assertAlmostEqual(self.check()['dr']['difference'],.1)
    def test_duplicate(self):
        self.d.loc[1,'Ticker']='A'
        with self.assertRaises(ValueError):self.check()
    def test_bad_diff(self):
        self.d.loc[0,'dr']=.8
        with self.assertRaises(ValueError):self.check()
    def test_bad_rate(self):
        self.d.loc[0,'r_post']=1.1
        with self.assertRaises(ValueError):self.check()
    def test_nonfinite(self):
        self.d.loc[0,'dv']=float('nan')
        with self.assertRaises(ValueError):self.check()
    def test_missing_group(self):
        self.d['treated']=1
        with self.assertRaises(ValueError):self.check()
    def test_nonpositive_exposure(self):
        self.d.loc[0,'trades_pre']=0
        with self.assertRaises(ValueError):self.check()
if __name__=='__main__':unittest.main()
