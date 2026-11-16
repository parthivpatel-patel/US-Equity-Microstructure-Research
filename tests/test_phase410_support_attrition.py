import unittest
from phase410_support_attrition import audit

def r(d,s,e,t,g='g'):
    return dict(date=d,security=s,exchange=e,treated=str(t),match_group=g)

class TestAudit(unittest.TestCase):
    def test_full(self):
        x=audit([r('2025-10-01','T','X',1),r('2025-10-01','C','X',0)])
        self.assertEqual((x['common_date_group_dates'],x['same_exchange_group_dates']),(1,1))
    def test_exchange(self):
        x=audit([r('2025-10-01','T','X',1),r('2025-10-01','C','Y',0)])
        self.assertEqual(x['monthly']['2025-10']['lost_no_same_exchange'],1)
    def test_date(self):
        x=audit([r('2025-10-01','T','X',1),r('2025-10-02','C','X',0)])
        self.assertEqual(x['monthly']['2025-10']['lost_no_common_date'],2)
    def test_duplicate(self):
        a=r('2025-10-01','T','X',1)
        self.assertEqual(audit([a,a])['status'],'BLOCKED')
    def test_empty(self):
        self.assertEqual(audit([])['status'],'BLOCKED')
    def test_roster_not_gate(self):
        x=audit([r('2025-10-01','T','X',1),r('2025-10-01','C','X',0)])
        self.assertEqual(x['status'],'STRUCTURE_ONLY_NOT_AUTHENTICATED')
        self.assertEqual(x['assumed_1_to_3_roster_violations'],['g'])
    def test_month(self):
        x=audit([r('2025-10-01','T','X',1),r('2025-10-01','C','X',0),r('2025-11-04','T','X',1)])
        self.assertEqual(x['monthly']['2025-11']['lost_no_common_date'],1)
if __name__=='__main__': unittest.main()
