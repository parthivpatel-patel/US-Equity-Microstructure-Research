import unittest
from scripts.phase358_panel_gate import aggregate_complete_cells as f

class CoverageGateTests(unittest.TestCase):
    def test_complete_and_zero(self):
        x=f([('A','2025-10-01','X','observed',0),('A','2025-10-01','Y','observed',3)],['X','Y'])
        self.assertEqual(x['complete'],{('A','2025-10-01'):3})
        self.assertEqual(x['excluded'],{})
    def test_missing_source_not_zero(self):
        x=f([('A','d','X','observed',0),('A','d','Y','source_missing',None)],['X','Y'])
        self.assertFalse(x['complete'])
        self.assertEqual(x['excluded'][('A','d')]['nonobserved_exchanges'],['Y'])
    def test_undeclared_exchange(self):
        x=f([('A','d','X','observed',1)],['X','Y'])
        self.assertEqual(x['excluded'][('A','d')]['undeclared_exchanges'],['Y'])
    def test_inapplicable_not_automatically_zero(self):
        x=f([('A','d','X','observed',1),('A','d','Y','exchange_not_applicable',None)],['X','Y'])
        self.assertFalse(x['complete'])
    def test_duplicate(self):
        with self.assertRaises(ValueError): f([('A','d','X','observed',1)]*2,['X'])
    def test_nonfinite(self):
        with self.assertRaises(ValueError): f([('A','d','X','observed',float('nan'))],['X'])
    def test_overflow(self):
        with self.assertRaises(ValueError): f([('A','d','X','observed',1e308),('A','d','Y','observed',1e308)],['X','Y'])
    def test_boolean(self):
        with self.assertRaises(ValueError): f([('A','d','X','observed',True)],['X'])
    def test_invalid_exchange_universe(self):
        with self.assertRaises(ValueError): f([('A','d','X','observed',1)],['X','X'])
    def test_order_independent(self):
        rows=[('A','d','X','observed',2),('A','d','Y','observed',3)]
        self.assertEqual(f(rows,['X','Y']),f(list(reversed(rows)),['Y','X']))

if __name__=='__main__': unittest.main()
