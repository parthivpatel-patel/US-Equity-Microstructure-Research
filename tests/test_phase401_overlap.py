import unittest
import pandas as pd
from phase401_overlap import audit

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.df=pd.DataFrame({'Ticker':['A','B','C','D','E','F','G','H'],'treated':[1,1,0,0,0,0,0,0],'r_pre':[.7,.8,.1,.2,.3,.4,.5,.6],'v_pre':[.7,.8,.1,.2,.3,.4,.5,.6],'trades_pre':[100,200,1,2,3,4,5,6],'dr':[0]*8,'dv':[0]*8})
    def test_quartile_empty(self):
        rows=audit(self.df)
        self.assertTrue(any(r[0]=='quartile_0' and r[2]==0 and r[4] is None for r in rows))
    def test_duplicate(self):
        d=self.df.copy();d.loc[1,'Ticker']='A'
        with self.assertRaises(ValueError):audit(d)
    def test_bad_group(self):
        d=self.df.copy();d.loc[1,'treated']=2
        with self.assertRaises(ValueError):audit(d)
    def test_bad_rate(self):
        d=self.df.copy();d.loc[1,'r_pre']=1.5
        with self.assertRaises(ValueError):audit(d)
    def test_nonfinite(self):
        d=self.df.copy();d.loc[1,'dr']=float('nan')
        with self.assertRaises(ValueError):audit(d)
if __name__=='__main__':unittest.main()
