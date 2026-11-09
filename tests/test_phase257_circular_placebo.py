import unittest
from phase257_circular_placebo import circular_shift_reference as run

class TestCircular(unittest.TestCase):
    def test_known(self):
        z=run([0,0,3,3],2,2)
        self.assertEqual(z['reference_statistics'],[3,0,-3,0])
        self.assertEqual(z['tail_fraction'],0.5)
    def test_constant(self):
        self.assertEqual(run([4,4,4],1,2)['tail_fraction'],1)
    def test_rotation_invariance_of_reference_multiset(self):
        a=run([1,3,2,8,4],2,3)
        b=run([2,8,4,1,3],2,3)
        self.assertEqual(sorted(a['reference_statistics']),sorted(b['reference_statistics']))
    def test_reject_bool(self):
        with self.assertRaises(ValueError): run([1,True,3],1,2)
    def test_reject_nan(self):
        with self.assertRaises(ValueError): run([1,float('nan'),3],1,2)
    def test_reject_bad_window(self):
        with self.assertRaises(ValueError): run([1,2,3],1,1)
    def test_reject_bool_window(self):
        with self.assertRaises(ValueError): run([1,2,3],True,2)
    def test_reject_too_short(self):
        with self.assertRaises(ValueError): run([1,2],1,1)

if __name__=='__main__': unittest.main()
