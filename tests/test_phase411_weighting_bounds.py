import unittest
from phase411_weighting_bounds import audit
def r(d,t,s,h,n,e='X'):
    return dict(date=d,match_group='a',exchange=e,treated=str(t),security=s,hidden_trades=str(h),total_trades=str(n))
class Test(unittest.TestCase):
    def test_reversal(self):
        x=audit([r('2025-10-01',1,'A',9,10),r('2025-10-01',0,'B',5,10),r('2025-10-02',1,'A',0,1000),r('2025-10-02',0,'B',1,10)])
        self.assertGreater(x['equal_cell_gap_pp'],0);self.assertLess(x['pooled_denominator_gap_pp'],0)
    def test_unpaired(self):
        self.assertEqual(audit([r('2025-10-01',1,'A',1,2),r('2025-10-01',0,'B',0,2),r('2025-10-02',1,'A',1,2)])['paired_cells'],1)
    def test_duplicate(self):
        x=r('2025-10-01',1,'A',1,2);self.assertEqual(audit([x,x])['status'],'BLOCKED')
    def test_invalid(self):
        self.assertEqual(audit([r('2025-10-01',1,'A',3,2)])['status'],'BLOCKED')
    def test_no_pair(self):
        self.assertEqual(audit([r('2025-10-01',1,'A',1,2)])['status'],'BLOCKED')
    def test_empty(self):
        self.assertEqual(audit([])['status'],'BLOCKED')
if __name__=='__main__':unittest.main()
