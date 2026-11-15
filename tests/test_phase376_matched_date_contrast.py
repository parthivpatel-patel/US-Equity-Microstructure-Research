import unittest
from fractions import Fraction
from phase376_matched_date_contrast import contrast

class Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [('a','pre','T',1,4),('a','pre','C',1,4),('a','post','T',3,4),('a','post','C',1,4)]
    def test_exact(self):
        self.assertEqual(contrast(self.rows,['pre'],['post'])['estimate'],Fraction(1,2))
    def test_common_date_shock_cancels(self):
        rows=[('a','pre','T',1,10),('a','pre','C',1,10),('a','post','T',8,10),('a','post','C',8,10)]
        self.assertEqual(contrast(rows,['pre'],['post'])['estimate'],0)
    def test_equal_pair_weights(self):
        rows=self.rows+[('b','pre','T',0,100),('b','pre','C',0,100),('b','post','T',0,100),('b','post','C',0,100)]
        self.assertEqual(contrast(rows,['pre'],['post'])['estimate'],Fraction(1,4))
    def test_missing(self):
        with self.assertRaises(ValueError): contrast(self.rows[:-1],['pre'],['post'])
    def test_duplicate(self):
        with self.assertRaises(ValueError): contrast(self.rows+self.rows[:1],['pre'],['post'])
    def test_overlap(self):
        with self.assertRaises(ValueError): contrast(self.rows,['pre'],['pre'])
    def test_fractional(self):
        bad=list(self.rows); bad[0]=('a','pre','T',0.5,4)
        with self.assertRaises(ValueError): contrast(bad,['pre'],['post'])
    def test_large_integers(self):
        n=2**60
        rows=[('a','pre','T',0,n),('a','pre','C',0,n),('a','post','T',1,n),('a','post','C',0,n)]
        self.assertEqual(contrast(rows,['pre'],['post'])['estimate'],Fraction(1,n))

if __name__=='__main__': unittest.main()
