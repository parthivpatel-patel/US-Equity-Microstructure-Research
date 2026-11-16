import csv
import os
import sys
import tempfile
import unittest
sys.path.insert(0,os.path.dirname(__file__))
from phase404_october_trend import analyze

class TrendTests(unittest.TestCase):
    def make(self, corrupt=None):
        f=tempfile.NamedTemporaryFile(mode='w',suffix='.csv',delete=False,newline='')
        cols=['Date','lot','Hidden','TradesForHidden',"HiddenVol('000)","TradeVolForHidden('000)"]
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
        for i in range(9):
            for lot in (10,40,100):
                row=dict(Date=f'202510{i+1:02d}',lot=lot,Hidden=20 if lot==100 else 50,TradesForHidden=100,**{"HiddenVol('000)":20 if lot==100 else 50,"TradeVolForHidden('000)":100})
                if corrupt and i==0 and lot==10:corrupt(row)
                w.writerow(row)
        f.close();self.addCleanup(lambda:os.unlink(f.name));return f.name
    def test_constant_difference(self):
        r=analyze(self.make());self.assertAlmostEqual(r['trade']['slope_pp_per_session'],0,places=10);self.assertEqual(r['trade']['n_dates'],9)
    def test_invalid_numerator(self):
        with self.assertRaises(ValueError):analyze(self.make(lambda r:r.update(Hidden=101)))
    def test_duplicate(self):
        p=self.make()
        with open(p) as f: lines=f.readlines()
        with open(p,'a') as f: f.write(lines[1])
        with self.assertRaises(ValueError):analyze(p)
if __name__=='__main__':unittest.main()
