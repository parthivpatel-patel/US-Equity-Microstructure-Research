import unittest
from fractions import Fraction
from phase375_weighting_decomposition import decompose

class TestDecomposition(unittest.TestCase):
    def test_within_only(self):
        x=decompose([('A',0,1),('A',9,9)])
        self.assertEqual(x['pooled'],Fraction(9,10))
        self.assertEqual(x['equal'],Fraction(1,2))
        self.assertEqual(x['within'],Fraction(2,5))
        self.assertEqual(x['between'],0)
    def test_between_only(self):
        x=decompose([('A',0,1),('B',9,9)])
        self.assertEqual(x['between'],Fraction(2,5))
        self.assertEqual(x['within'],0)
    def test_both(self):
        x=decompose([('A',0,1),('A',0,1),('B',0,1),('B',10,10)])
        self.assertEqual(x['gap'],x['between']+x['within'])
        self.assertNotEqual(x['between'],0)
        self.assertNotEqual(x['within'],0)
    def test_large_integer(self):
        n=2**60
        x=decompose([('A',n-1,n),('B',0,1)])
        self.assertEqual(x['pooled'],Fraction(n-1,n+1))
    def test_invalid(self):
        for rows in [[],[('A',2,1)],[('A',1,0)],[('A',1.0,2)],[('',0,1)]]:
            with self.subTest(rows=rows),self.assertRaises(ValueError): decompose(rows)

if __name__=='__main__': unittest.main()
