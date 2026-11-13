import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase343_weighting_sensitivity import analyze

def r(sec, group, arm, num, den, day='2025-10-01', ex='XNAS'):
    return dict(security=sec, match_group=group, treated=arm, numerator=str(num), denominator=str(den), date=day, exchange=ex)

class TestWeighting(unittest.TestCase):
    def test_weighting_divergence(self):
        rows=[r('a','A','1',9,10),r('b','A','0',1,10),
              r('c','B','1',1,100),r('d','B','0',9,100),
              r('c','B','1',1,100,'2025-10-02'),r('d','B','0',9,100,'2025-10-02')]
        v=analyze(rows)['estimates_pp']
        self.assertAlmostEqual(v['equal_group'], 36)
        self.assertAlmostEqual(v['equal_paired_cell'], 64/3)
        self.assertAlmostEqual(v['combined_denominator_weighted_cell'], -80/21)
    def test_no_paired(self):
        self.assertEqual(analyze([r('a','A','1',1,2)])['status'],'NO_PAIRED_SUPPORT')
    def test_exchange_support(self):
        self.assertEqual(analyze([r('a','A','1',1,2,ex='XNAS'),r('b','A','0',1,2,ex='XNYS')])['paired_cells'],0)
    def test_duplicate(self):
        x=r('a','A','1',1,2)
        with self.assertRaises(ValueError): analyze([x,x])
    def test_drift(self):
        with self.assertRaises(ValueError): analyze([r('a','A','1',1,2),r('a','A','0',1,2,'2025-10-02')])
    def test_bad_denominator(self):
        with self.assertRaises(ValueError): analyze([r('a','A','1',1,0)])
    def test_bad_rate(self):
        with self.assertRaises(ValueError): analyze([r('a','A','1',3,2)])
    def test_bad_date(self):
        with self.assertRaises(ValueError): analyze([r('a','A','1',1,2,day='2025-13-01')])
    def test_empty(self):
        with self.assertRaises(ValueError): analyze([])
    def test_unpaired_excluded(self):
        out=analyze([r('a','A','1',1,2),r('b','A','0',0,2),r('c','A','1',1,2,'2025-10-02')])
        self.assertEqual((out['paired_cells'],out['discarded_cells']),(1,1))

if __name__ == '__main__': unittest.main()
