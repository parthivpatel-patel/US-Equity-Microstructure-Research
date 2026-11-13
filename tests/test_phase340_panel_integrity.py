import unittest
from phase340_panel_integrity import audit

def row(sec='A',date='2025-10-01',exc='X',treated='1',group='g',**kw):
    r=dict(security=sec,date=date,exchange=exc,treated=treated,match_group=group,
           hidden_count='1',trade_count='2',hidden_shares='5',total_shares='10')
    r.update(kw);return r
class PanelIntegrityTests(unittest.TestCase):
    def test_valid(self):
        result=audit([row(),row(sec='B',treated='0')]);self.assertEqual(result['status'],'STRUCTURAL_CHECKS_PASS')
        self.assertEqual(result['authentication'],'NOT_ESTABLISHED')
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):audit([row(),row()])
    def test_drift(self):
        with self.assertRaisesRegex(ValueError,'drift'):audit([row(),row(date='2025-10-02',treated='0')])
    def test_invalid_count(self):
        for val in ['-1','NaN','1.2','Infinity']:
            with self.subTest(val=val),self.assertRaises(ValueError):audit([row(hidden_count=val)])
    def test_exceeds(self):
        with self.assertRaisesRegex(ValueError,'exceeds'):audit([row(hidden_shares='11')])
    def test_unmatched(self):
        self.assertEqual(audit([row()])['status'],'BLOCK')
    def test_date(self):
        with self.assertRaisesRegex(ValueError,'date'):audit([row(date='2025-02-30')])
    def test_blank(self):
        with self.assertRaisesRegex(ValueError,'blank'):audit([row(sec='')])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'):audit([])
    def test_missing(self):
        with self.assertRaisesRegex(ValueError,'missing'):audit([{'security':'A'}])
if __name__=='__main__':unittest.main()
