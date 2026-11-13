import unittest
from scripts.phase327_cross_outcome_audit import audit

def row(outcome, wid, start='2025-09-01', end='2025-09-05', value='0.1'):
    return dict(outcome=outcome, window_id=wid, start_date=start, end_date=end, placebo_pp=value)

class TestAudit(unittest.TestCase):
    def test_aligned(self):
        self.assertTrue(audit([row('count','a'),row('volume','a')])['pairwise']['count|volume']['same_window_identity_and_dates'])
    def test_missing_window(self):
        r=audit([row('count','a'),row('volume','b')])['pairwise']['count|volume']
        self.assertEqual(r['only_left'],['a']); self.assertEqual(r['only_right'],['b'])
    def test_disagree_dates(self):
        self.assertEqual(audit([row('count','a'),row('volume','a',end='2025-09-06')])['pairwise']['count|volume']['shared_id_date_disagreements'],['a'])
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit([row('count','a'),row('count','a')])
    def test_nonfinite(self):
        with self.assertRaises(ValueError): audit([row('count','a',value='NaN')])
    def test_post_reform(self):
        with self.assertRaises(ValueError): audit([row('count','a',end='2025-11-03')])
    def test_reversed(self):
        with self.assertRaises(ValueError): audit([row('count','a',start='2025-09-06')])
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])

if __name__=='__main__': unittest.main()
