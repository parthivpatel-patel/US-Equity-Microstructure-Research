import unittest
from fractions import Fraction as F
from phase386_two_way_cluster import two_way_cr0

class TwoWayTests(unittest.TestCase):
    def test_constant(self):
        r=two_way_cr0([('a','1',2),('a','2',2),('b','1',2),('b','2',2)])
        self.assertEqual((r['mean'],r['variance_cr0']), (F(2),F(0)))
    def test_pair_effect(self):
        r=two_way_cr0([('a','1',0),('a','2',0),('b','1',2),('b','2',2)])
        self.assertEqual((r['pair_component'],r['date_component'],r['intersection_component'],r['variance_cr0']), (F(1,2),F(0),F(1,4),F(1,4)))
    def test_date_effect(self):
        r=two_way_cr0([('a','1',0),('b','1',0),('a','2',2),('b','2',2)])
        self.assertEqual(r['variance_cr0'], F(1,4))
    def test_negative_possible(self):
        r=two_way_cr0([('a','1',0),('a','2',2),('b','1',2),('b','2',0)])
        self.assertEqual(r['variance_cr0'], F(-1,4))
        self.assertTrue(r['negative_variance'])
    def test_duplicate(self):
        with self.assertRaises(ValueError): two_way_cr0([('a','1',0)]*4)
    def test_unbalanced(self):
        with self.assertRaises(ValueError): two_way_cr0([('a','1',0),('a','2',0),('b','1',0)])
    def test_invalid_value(self):
        with self.assertRaises(ValueError): two_way_cr0([('a','1',0.5),('a','2',0),('b','1',0),('b','2',0)])
    def test_single_pair(self):
        with self.assertRaises(ValueError): two_way_cr0([('a','1',0),('a','2',0)])
    def test_order_invariance(self):
        x=[('a','1',F(1,3)),('a','2',2),('b','1',1),('b','2',F(4,3))]
        self.assertEqual(two_way_cr0(x),two_way_cr0(list(reversed(x))))

if __name__=='__main__': unittest.main()
