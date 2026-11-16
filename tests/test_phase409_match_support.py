import unittest
from phase409_match_support import audit

def row(s, t, e='X', d='2025-10-01', g='A'):
    return dict(date=d, security=s, exchange=e, treated=str(t), match_group=g)

class SupportTests(unittest.TestCase):
    def test_complete(self):
        r = audit([row('T', 1), row('C1', 0), row('C2', 0), row('C3', 0)])
        self.assertEqual(r['status'], 'STRUCTURE_ONLY_NOT_AUTHENTICATED')
        self.assertEqual(r['complete_1_to_3_group_dates'], 1)
    def test_missing_control(self):
        self.assertEqual(audit([row('T', 1), row('C1', 0)])['status'], 'BLOCKED')
    def test_exchange_mismatch(self):
        r = audit([row('T', 1), row('C1', 0, 'Y'), row('C2', 0, 'Y'), row('C3', 0, 'Y')])
        self.assertEqual(r['paired_group_dates'], 1)
        self.assertEqual(r['paired_exchange_group_dates'], 0)
    def test_duplicate(self):
        self.assertEqual(audit([row('T', 1)] * 2)['status'], 'BLOCKED')
    def test_empty(self):
        self.assertEqual(audit([])['status'], 'BLOCKED')

if __name__ == '__main__':
    unittest.main()
