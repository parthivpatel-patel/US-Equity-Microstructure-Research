import unittest
from scripts.phase290_bootstrap_audit import quantile_linear, audit_indices

class Audit(unittest.TestCase):
    def test_indices_999(self):
        self.assertEqual((audit_indices(999)['lower_index_phase289'],audit_indices(999)['upper_index_phase289']),(24,973))
    def test_indices_99(self):
        self.assertEqual((audit_indices(99)['lower_index_phase289'],audit_indices(99)['upper_index_phase289']),(2,95))
    def test_interpolation(self):
        self.assertAlmostEqual(quantile_linear([0,10,20,30,40],.125),5)
    def test_endpoints(self):
        self.assertEqual(quantile_linear([1,3,5],0),1)
        self.assertEqual(quantile_linear([1,3,5],1),5)
    def test_reject_short(self):
        with self.assertRaises(ValueError): quantile_linear([1],.5)
    def test_reject_probability(self):
        with self.assertRaises(ValueError): quantile_linear([1,2],1.1)
    def test_reject_boolean_repetitions(self):
        with self.assertRaises(ValueError): audit_indices(True)

if __name__=='__main__': unittest.main()
