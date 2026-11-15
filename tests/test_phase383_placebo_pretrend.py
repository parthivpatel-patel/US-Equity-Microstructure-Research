import unittest
from fractions import Fraction
from phase383_placebo_pretrend import audit_matched_pretrend as audit

P=['p']
D=['2025-09-01','2025-09-02','2025-09-03']
W=[('sep', D[:2], D[2:])]
def rows(t=(1,2,3), c=(0,0,0), den=10):
    return [('p',s,d,v,den) for s,vs in [('T',t),('C',c)] for d,v in zip(D,vs)]
class TestPretrend(unittest.TestCase):
    def test_exact(self):
        r=audit(rows(),P,W)['windows'][0]
        self.assertEqual(r['contrast'],Fraction(3,20))
        self.assertEqual(r['pretrend_slope_per_calendar_day'],Fraction(1,10))
    def test_common_shock_cancels(self):
        self.assertEqual(audit(rows((2,3,4),(1,1,1)),P,W)['windows'][0]['contrast'],Fraction(3,20))
    def test_missing(self):
        with self.assertRaises(ValueError): audit(rows()[:-1],P,W)
    def test_duplicate(self):
        r=rows()
        with self.assertRaises(ValueError): audit(r+r[:1],P,W)
    def test_invalid_counts(self):
        with self.assertRaises(ValueError): audit(rows((11,2,3)),P,W)
    def test_overlapping_windows(self):
        with self.assertRaises(ValueError): audit(rows(),P,[('bad',D[:2],D[1:])])
    def test_short_pre(self):
        with self.assertRaises(ValueError): audit(rows(),P,[('bad',D[:1],D[1:])])
    def test_no_data(self):
        with self.assertRaises(ValueError): audit([],P,W)
    def test_multi_pair_equal_weight(self):
        r=rows()+[('q',s,d,v,10) for s,vs in [('T',(0,0,0)),('C',(0,0,0))] for d,v in zip(D,vs)]
        self.assertEqual(audit(r,['p','q'],W)['windows'][0]['contrast'],Fraction(3,40))
if __name__=='__main__': unittest.main()
