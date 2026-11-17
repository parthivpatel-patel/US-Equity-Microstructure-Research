import unittest
from phase433_calendar_support import audit

def r(d,s,a,g='G',e='X'):
    return {'date':d,'security':s,'treated':str(a),'match_group':g,'exchange':e}

class Tests(unittest.TestCase):
    def test_common_date(self):
        x=[r(d,s,a,g) for g,dates in [('G1',['2025-10-30','2025-10-31']),('G2',['2025-10-31'])] for d in dates for s,a in [('T'+g,1),('C'+g,0)]]
        self.assertEqual(audit(x)['cross_unit'][0]['common_date_values'],['2025-10-31'])
    def test_disjoint_date(self):
        x=[r(d,s,a,g) for g,d in [('G1','2025-10-30'),('G2','2025-10-31')] for s,a in [('T'+g,1),('C'+g,0)]]
        self.assertEqual(audit(x)['cross_unit'][0]['common_paired_dates'],0)
    def test_missing_arm(self):
        x=[r('2025-10-30','T',1),r('2025-10-31','T',1),r('2025-10-31','C',0)]
        self.assertEqual(audit(x)['by_unit'][0]['unpaired_dates'],1)
    def test_exchange_specific_identity(self):
        x=[r('2025-10-31','T',1,'G1','X'),r('2025-10-31','T',0,'G2','Y')]
        self.assertEqual(audit(x)['unstable_security_exchange_assignments'],[])
    def test_unstable(self):
        x=[r('2025-10-30','T',1),r('2025-10-31','T',0)]
        self.assertEqual(audit(x)['unstable_security_exchange_assignments'],['T@X'])
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):audit([r('2025-10-31','T',1)]*2)
    def test_weekend(self):
        with self.assertRaisesRegex(ValueError,'weekend'):audit([r('2025-11-01','T',1)])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'):audit([])
    def test_bad_arm(self):
        with self.assertRaisesRegex(ValueError,'treatment'):audit([r('2025-10-31','T',2)])
    def test_missing(self):
        with self.assertRaisesRegex(ValueError,'missing'):audit([{'date':'2025-10-31'}])
    def test_post(self):
        x=[r('2025-11-03','T',1),r('2025-11-03','C',0)]
        self.assertEqual(audit(x)['cross_unit'][1]['common_paired_dates'],1)

if __name__=='__main__':unittest.main()
