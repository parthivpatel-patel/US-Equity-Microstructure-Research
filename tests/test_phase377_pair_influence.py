import unittest
from fractions import Fraction
from phase377_pair_influence import pair_deletion_audit

def pair(pid, post_t, den=10):
    return [(pid,'pre','T',0,den),(pid,'pre','C',0,den),
            (pid,'post','T',max(post_t,0),den),(pid,'post','C',max(-post_t,0),den)]

class PairInfluenceTests(unittest.TestCase):
    def test_exact_deletion(self):
        out=pair_deletion_audit(pair('a',3)+pair('b',1),['pre'],['post'])
        self.assertEqual(out['estimate'],Fraction(1,5))
        self.assertEqual(out['leave_one_out'],{'a':Fraction(1,10),'b':Fraction(3,10)})
    def test_sign_reversal(self):
        out=pair_deletion_audit(pair('a',8)+pair('b',-2)+pair('c',-2),['pre'],['post'])
        self.assertTrue(out['sign_reversal_on_deletion'])
        self.assertEqual(out['leave_one_out']['a'],Fraction(-1,5))
    def test_no_sign_reversal(self):
        self.assertFalse(pair_deletion_audit(pair('a',3)+pair('b',1),['pre'],['post'])['sign_reversal_on_deletion'])
    def test_single_pair_rejected(self):
        with self.assertRaises(ValueError): pair_deletion_audit(pair('a',1),['pre'],['post'])
    def test_unbalanced_rejected(self):
        with self.assertRaises(ValueError): pair_deletion_audit((pair('a',1)+pair('b',1))[:-1],['pre'],['post'])
    def test_exact_large_integer(self):
        n=2**60
        out=pair_deletion_audit(pair('a',1,n)+pair('b',0,n),['pre'],['post'])
        self.assertEqual(out['estimate'],Fraction(1,2*n))
    def test_zero_estimate_no_false_sign_reversal(self):
        out=pair_deletion_audit(pair('a',2)+pair('b',-2),['pre'],['post'])
        self.assertFalse(out['sign_reversal_on_deletion'])

if __name__=='__main__': unittest.main()
