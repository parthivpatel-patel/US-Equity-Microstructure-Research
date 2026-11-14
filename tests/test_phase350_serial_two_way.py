import unittest
from scripts.phase350_serial_two_way import serial_two_way_components as calc

class TestPhase350(unittest.TestCase):
    def setUp(self):
        self.rows=[('A','2025-09-01',1.),('A','2025-09-02',3.),('A','2025-09-03',5.),('B','2025-09-01',2.),('B','2025-09-02',4.),('B','2025-09-03',6.)]
    def test_lag_zero(self):
        r=calc(self.rows,0); self.assertAlmostEqual(r['two_way_raw_variance'],r['serial_adjusted_raw_variance'])
    def test_lag_one(self):
        r=calc(self.rows,1); self.assertAlmostEqual(r['serial_increment'],r['lag_products'][1])
    def test_mean(self): self.assertAlmostEqual(calc(self.rows)['mean_pp'],3.5)
    def test_order(self): self.assertEqual(calc(self.rows),calc(list(reversed(self.rows))))
    def test_duplicate(self):
        with self.assertRaises(ValueError): calc(self.rows+self.rows[:1])
    def test_nan(self):
        with self.assertRaises(ValueError): calc(self.rows[:-1]+[('B','2025-09-03',float('nan'))])
    def test_date(self):
        with self.assertRaises(ValueError): calc([('A','2025-9-1',1.)]+self.rows[1:])
    def test_bool_lag(self):
        with self.assertRaises(ValueError): calc(self.rows,True)
    def test_imbalance(self):
        r=calc(self.rows[:-1]); self.assertAlmostEqual(r['mean_pp'],(1+3+5)/6+(2+4)/4)
    def test_missing_date(self):
        r=calc([x for x in self.rows if x[1]!='2025-09-02']); self.assertEqual(r['dates'],2)
if __name__=='__main__': unittest.main()
