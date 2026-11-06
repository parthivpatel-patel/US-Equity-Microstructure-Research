import unittest
from scripts.phase198_pair_consistency import audit

def row(outcome, **kwargs):
    r=dict(window='pre',date='2025-10-06',security='ABC',exchange='X',outcome=outcome,group='G',treated=True)
    r.update(kwargs)
    return r

class PairConsistencyTests(unittest.TestCase):
    def test_valid(self):
        r=audit([row('count'),row('volume')]); self.assertEqual(r['within_pair_assignment_conflicts'],[]); self.assertFalse(r['treatment_authenticated'])
    def test_treatment_disagreement(self):
        self.assertEqual(len(audit([row('count'),row('volume',treated=False)])['within_pair_assignment_conflicts']),1)
    def test_group_disagreement(self):
        self.assertEqual(len(audit([row('count'),row('volume',group='H')])['within_pair_assignment_conflicts']),1)
    def test_missing_pair(self):
        self.assertEqual(len(audit([row('count')])['unpaired_entity_dates']),1)
    def test_duplicate_outcome_with_different_group(self):
        with self.assertRaises(ValueError): audit([row('count'),row('count',group='H')])
    def test_distinct_exchanges(self):
        self.assertEqual(len(audit([row('count'),row('volume',exchange='Y')])['unpaired_entity_dates']),2)
    def test_disjoint_dates(self):
        self.assertEqual(audit([row('count'),row('volume'),row('count',date='2025-11-03'),row('volume',date='2025-11-03')])['entity_dates'],2)
    def test_bad_treatment(self):
        with self.assertRaises(ValueError): audit([row('count',treated=1)])
    def test_weekend(self):
        with self.assertRaises(ValueError): audit([row('count',date='2025-10-05')])
    def test_missing_field(self):
        r=row('count'); del r['group']
        with self.assertRaises(ValueError): audit([r])

if __name__=='__main__': unittest.main()
