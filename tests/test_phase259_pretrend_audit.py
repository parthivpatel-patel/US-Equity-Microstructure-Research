import unittest
from scripts.phase259_pretrend_audit import audit

DATES=['2025-09-22','2025-09-23','2025-09-24','2025-09-25','2025-09-26','2025-09-29']
def rows(values, pairs=('a','b')):
    return [dict(date=d,pair_id=p,treated=v,control=0) for d,v in zip(DATES,values) for p in pairs]
class TestAudit(unittest.TestCase):
    def test_linear_trend(self):
        r=audit(rows([0,1,2,3,4,5]),'2025-09-26')
        self.assertEqual(r['pre_slope_per_observed_session'],1)
        self.assertEqual(r['pre_late_minus_early'],2)
        self.assertEqual(r['post_minus_pre'],3.0)
    def test_flat(self):
        self.assertEqual(audit(rows([2]*6),'2025-09-26')['pre_slope_per_observed_session'],0)
    def test_duplicate(self):
        a=rows([0]*6)
        with self.assertRaises(ValueError): audit(a+[a[0]],'2025-09-26')
    def test_changing_roster(self):
        a=rows([0]*6)
        a.pop()
        with self.assertRaises(ValueError): audit(a,'2025-09-26')
    def test_nonfinite(self):
        a=rows([0]*6);a[0]['treated']=float('nan')
        with self.assertRaises(ValueError): audit(a,'2025-09-26')
    def test_bool(self):
        a=rows([0]*6);a[0]['control']=False
        with self.assertRaises(ValueError): audit(a,'2025-09-26')
    def test_no_post(self):
        with self.assertRaises(ValueError): audit(rows([0]*6),'2025-10-01')
    def test_short_pre(self):
        with self.assertRaises(ValueError): audit(rows([0]*6),'2025-09-25')
    def test_empty(self):
        with self.assertRaises(ValueError): audit([],'2025-09-26')
if __name__=='__main__':unittest.main()
