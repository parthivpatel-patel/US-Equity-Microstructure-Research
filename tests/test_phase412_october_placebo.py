import unittest
from scripts.phase412_october_placebo import audit

def r(day,security,treated,hidden=1,total=10,exchange='X'):
    return dict(date=day,security=security,treated=str(treated),hidden_trades=str(hidden),
        total_trades=str(total),match_group='G',exchange=exchange)

class TestPlacebo(unittest.TestCase):
    def test_known_change(self):
        rows=[r('2025-10-01','T',1,8),r('2025-10-01','C',0,2),
              r('2025-10-20','T',1,3),r('2025-10-20','C',0,2)]
        self.assertAlmostEqual(audit(rows)['placebo_change_pp'],-50)
    def test_duplicate(self):
        self.assertEqual(audit([r('2025-10-01','T',1)]*2)['status'],'BLOCKED')
    def test_exchange_mismatch(self):
        rows=[r('2025-10-01','T',1),r('2025-10-01','C',0,exchange='Y'),
              r('2025-10-20','T',1),r('2025-10-20','C',0)]
        self.assertEqual(audit(rows)['status'],'BLOCKED')
    def test_invalid_counts(self):
        self.assertEqual(audit([r('2025-10-01','T',1,1,0)])['status'],'BLOCKED')
    def test_empty(self):
        self.assertEqual(audit([])['status'],'BLOCKED')
    def test_cutoff(self):
        self.assertEqual(audit([],'2025-11-03')['status'],'BLOCKED')
if __name__=='__main__':unittest.main()
