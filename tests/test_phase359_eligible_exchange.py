import unittest
from scripts.phase359_eligible_exchange import compare_exchange_support as run

class TestEligibility(unittest.TestCase):
    def setUp(self):
        self.k=('AAA','2025-10-01')
        self.rows=[('AAA','2025-10-01','X','observed',0),('AAA','2025-10-01','Y','exchange_not_applicable',None)]
    def test_eligible_zero_not_strict(self):
        r=run(self.rows,['X','Y'],{self.k:['X']})
        self.assertEqual(r['declared_eligible'][self.k],0)
        self.assertEqual(r['strict_n'],0)
    def test_full_strict(self):
        rows=[('AAA','2025-10-01','X','observed',2),('AAA','2025-10-01','Y','observed',3)]
        self.assertEqual(run(rows,['X','Y'],{self.k:['X','Y']})['strict_complete_universe'][self.k],5)
    def test_missing_eligible_excluded(self):
        rows=[('AAA','2025-10-01','X','source_missing',None),self.rows[1]]
        self.assertEqual(run(rows,['X','Y'],{self.k:['X']})['eligible_n'],0)
    def test_missing_grid_fails(self):
        with self.assertRaises(ValueError):run(self.rows[:1],['X','Y'],{self.k:['X']})
    def test_excluded_observed_fails(self):
        with self.assertRaises(ValueError):run([self.rows[0],('AAA','2025-10-01','Y','observed',0)],['X','Y'],{self.k:['X']})
    def test_eligible_inapplicable_fails(self):
        with self.assertRaises(ValueError):run(self.rows,['X','Y'],{self.k:['X','Y']})
    def test_duplicate_fails(self):
        with self.assertRaises(ValueError):run(self.rows+self.rows[:1],['X','Y'],{self.k:['X']})
    def test_nan_fails(self):
        with self.assertRaises(ValueError):run([('AAA','2025-10-01','X','observed',float('nan')),self.rows[1]],['X','Y'],{self.k:['X']})
    def test_order_invariance(self):
        self.assertEqual(run(self.rows,['X','Y'],{self.k:['X']})['declared_eligible'],run(self.rows[::-1],['Y','X'],{self.k:['X']})['declared_eligible'])
    def test_policy_required(self):
        with self.assertRaises(ValueError):run(self.rows,['X','Y'],{})

if __name__=='__main__': unittest.main()
