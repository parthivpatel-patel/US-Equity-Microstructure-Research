import unittest
from phase349_serial_dependence import date_lag_diagnostic

class DateLagTests(unittest.TestCase):
    def setUp(self):
        self.rows=[('A','2025-10-01',2),('B','2025-10-01',0),('A','2025-10-02',4),('B','2025-10-02',2),('A','2025-10-03',6),('B','2025-10-03',4)]
    def test_exact_scores(self):
        r=date_lag_diagnostic(self.rows,1)
        self.assertAlmostEqual(r['mean_pp'],3)
        self.assertEqual(list(r['date_scores'].values()),[-2/3,0,2/3])
        self.assertEqual(r['lag_products'],[8/9,0])
        self.assertEqual(r['bartlett_date_component'],8/9)
    def test_order_invariance(self):
        self.assertEqual(date_lag_diagnostic(self.rows,2),date_lag_diagnostic(list(reversed(self.rows)),2))
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): date_lag_diagnostic(self.rows+[self.rows[0]])
    def test_invalid_value(self):
        with self.assertRaises(ValueError): date_lag_diagnostic(self.rows[:-1]+[('B','2025-10-03',float('nan'))])
    def test_bad_lag(self):
        with self.assertRaises(ValueError): date_lag_diagnostic(self.rows,-1)
    def test_unbalanced_groups(self):
        r=date_lag_diagnostic([('A','2025-10-01',10),('A','2025-10-02',10),('B','2025-10-01',0)],1)
        self.assertAlmostEqual(r['mean_pp'],5)
if __name__=='__main__': unittest.main()
