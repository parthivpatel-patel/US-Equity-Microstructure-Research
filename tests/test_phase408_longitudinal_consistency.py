import unittest
from phase408_longitudinal_consistency import audit

def rows():
    return [dict(date=d, security=s, exchange='XNAS', treated=str(t), match_group='G')
            for d in ('2025-09-30', '2025-10-15', '2025-11-03')
            for s, t in (('A', 1), ('B', 0))]

class AuditTests(unittest.TestCase):
    def test_valid(self):
        r = audit(rows())
        self.assertEqual(r['status'], 'LONGITUDINAL_STRUCTURE_PASS_NOT_AUTHENTICATED')
        self.assertEqual(r['paired_group_dates'], 3)
    def test_treatment_flip(self):
        a = rows(); a[-2]['treated'] = '0'
        self.assertEqual(audit(a)['status'], 'BLOCKED')
    def test_group_flip(self):
        a = rows(); a[-1]['match_group'] = 'H'
        self.assertEqual(audit(a)['status'], 'BLOCKED')
    def test_missing_daily_pair(self):
        a = rows(); a.pop()
        self.assertEqual(audit(a)['unpaired_group_dates'], 1)
    def test_duplicate_key(self):
        a = rows(); a.append(a[0].copy())
        self.assertTrue(any('duplicate' in x for x in audit(a)['errors']))
    def test_empty(self):
        self.assertEqual(audit([])['status'], 'BLOCKED')

if __name__ == '__main__':
    unittest.main()
