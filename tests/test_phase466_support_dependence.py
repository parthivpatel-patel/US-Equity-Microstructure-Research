import unittest
from phase466_support_dependence import support_dependence

S = [f'2025-09-{d:02d}' for d in range(1, 7)]

class Tests(unittest.TestCase):
    def test_exact_counts(self):
        r = support_dependence(S, ['2025-09-02','2025-09-04'], 3)
        self.assertEqual(r['total_paths'], 16)
        self.assertEqual(r['eligible_counts'], [7,14])
        self.assertEqual(r['joint_probabilities'][0][1], 6/16)
    def test_covariance(self):
        r = support_dependence(S, ['2025-09-02','2025-09-04'], 3)
        self.assertAlmostEqual(r['eligibility_covariance'][0][1], 6/16-(7/16)*(14/16))
        self.assertAlmostEqual(r['conditional_probability_a_given_b'][0][1], 6/14)
    def test_symmetry(self):
        r = support_dependence(S, ['2025-09-02','2025-09-04'], 3)
        self.assertEqual(r['eligibility_covariance'][0][1],r['eligibility_covariance'][1][0])
    def test_single(self):
        r = support_dependence(S,['2025-09-04'],3)
        self.assertAlmostEqual(r['eligibility_covariance'][0][0], (14/16)*(2/16))
    def test_bad_dates(self):
        with self.assertRaises(ValueError): support_dependence(S[::-1],['2025-09-04'],3)
    def test_duplicate_cutoffs(self):
        with self.assertRaises(ValueError): support_dependence(S,['2025-09-04']*2,3)
    def test_invalid_block(self):
        with self.assertRaises(ValueError): support_dependence(S,['2025-09-04'],True)
    def test_path_cap(self):
        with self.assertRaises(ValueError): support_dependence(S,['2025-09-04'],3,max_paths=15)

if __name__ == '__main__': unittest.main()
