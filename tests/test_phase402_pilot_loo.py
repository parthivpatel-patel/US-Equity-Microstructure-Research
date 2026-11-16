import unittest
import pandas as pd
from phase402_pilot_loo import analyze
class AuditTests(unittest.TestCase):
    def setUp(self):
        dates=[20251001,20251002,20251016,20251017,20251103,20251104]
        self.d=pd.DataFrame([{'Date':date,'lot':lot,'Hidden':20+lot/10,'TradesForHidden':100,"HiddenVol('000)":10+lot/10,"TradeVolForHidden('000)":100} for date in dates for lot in [10,40,100]])
    def test_four_contrasts(self):self.assertEqual(len(analyze(self.d)),4)
    def test_order_invariance(self):self.assertEqual(analyze(self.d),analyze(self.d.sample(frac=1,random_state=3)))
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):analyze(pd.concat([self.d,self.d.iloc[:1]]))
    def test_missing_tier_rejected(self):
        with self.assertRaises(ValueError):analyze(self.d.iloc[1:])
    def test_bad_numerator_rejected(self):
        d=self.d.copy();d.loc[0,'Hidden']=101
        with self.assertRaises(ValueError):analyze(d)
    def test_date_unassigned_rejected(self):
        d=self.d.copy();d.loc[0,'Date']=20250930
        with self.assertRaises(ValueError):analyze(d)
if __name__=='__main__':unittest.main()
