import unittest
from phase260_sensitivity import audit

DATES = ['2025-10-27', '2025-10-28', '2025-11-03', '2025-11-04']

def fixture():
    return [{'date': d, 'pair_id': p, 'treated': float(i >= 2) * effect,
             'control': 0.0} for i, d in enumerate(DATES) for p, effect in [('A', 2), ('B', 4)]]

class SensitivityTests(unittest.TestCase):
    def test_baseline(self):
        r = audit(fixture(), '2025-11-03')
        self.assertEqual(r['full'], 3)
        self.assertEqual(r['leave_one_pair_out'], {'A': 4, 'B': 2})
        self.assertEqual(r['max_pair_deletion_change'], 1)
        self.assertEqual(r['max_date_deletion_change'], 0)
    def test_order_invariance(self):
        self.assertEqual(audit(fixture()[::-1], '2025-11-03'), audit(fixture(), '2025-11-03'))
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit(fixture() + fixture()[:1], '2025-11-03')
    def test_missing_cell(self):
        with self.assertRaises(ValueError): audit(fixture()[:-1], '2025-11-03')
    def test_nonfinite(self):
        x = fixture(); x[0]['treated'] = float('nan')
        with self.assertRaises(ValueError): audit(x, '2025-11-03')
    def test_weekend(self):
        x = fixture(); x[0]['date'] = '2025-11-01'
        with self.assertRaises(ValueError): audit(x, '2025-11-03')
    def test_bool(self):
        x = fixture(); x[0]['treated'] = True
        with self.assertRaises(ValueError): audit(x, '2025-11-03')
    def test_insufficient_dates(self):
        with self.assertRaises(ValueError): audit(fixture()[:6], '2025-11-03')

if __name__ == '__main__': unittest.main()
