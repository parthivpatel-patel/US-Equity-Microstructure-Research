import unittest
from fractions import Fraction
from phase378_exchange_stratified import exchange_contrast

def fixture():
    rows=[]
    for p in ('a','b'):
        for d in ('pre','post'):
            for e in ('X','Y'):
                for arm in ('T','C'):
                    rate = 1 if arm=='T' and d=='post' and e=='X' else 0
                    rows.append((p,d,e,arm,rate,2))
    return rows

class TestExchangeContrast(unittest.TestCase):
    def test_exact_equal_exchange_weight(self):
        r=exchange_contrast(fixture(),['pre'],['post'])
        self.assertEqual(r['by_exchange'],{'X':Fraction(1,2),'Y':Fraction(0)})
        self.assertEqual(r['estimate'],Fraction(1,4))
    def test_duplicate_rejected(self):
        rows=fixture(); rows.append(rows[0])
        with self.assertRaises(ValueError): exchange_contrast(rows,['pre'],['post'])
    def test_missing_exchange_arm_rejected(self):
        with self.assertRaises(ValueError): exchange_contrast(fixture()[:-1],['pre'],['post'])
    def test_fractional_count_rejected(self):
        rows=fixture(); rows[0]=(*rows[0][:4],0.0,2)
        with self.assertRaises(ValueError): exchange_contrast(rows,['pre'],['post'])
    def test_big_integer_precision(self):
        rows=fixture(); big=2**60
        rows=[(p,d,e,a,h*big,t*big) for p,d,e,a,h,t in rows]
        self.assertEqual(exchange_contrast(rows,['pre'],['post'])['estimate'],Fraction(1,4))
    def test_window_overlap_rejected(self):
        with self.assertRaises(ValueError): exchange_contrast(fixture(),['pre'],['pre'])
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): exchange_contrast([],['pre'],['post'])
    def test_invalid_numerator_rejected(self):
        rows=fixture(); rows[0]=(*rows[0][:4],3,2)
        with self.assertRaises(ValueError): exchange_contrast(rows,['pre'],['post'])

if __name__=='__main__': unittest.main()
