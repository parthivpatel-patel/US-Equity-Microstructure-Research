import unittest
from phase246_overlap_audit import audit_placebo_overlap

class OverlapAuditTests(unittest.TestCase):
    def test_adjacent_windows(self):
        r = audit_placebo_overlap([4, 5, 6], 3, 12)
        self.assertEqual(r['n_overlapping_pairs'], 3)
        self.assertEqual([p['shared_sessions'] for p in r['overlapping_pairs']], [5, 4, 5])
        self.assertEqual(r['nonoverlapping_cut_subset'], [4])
    def test_disjoint(self):
        r = audit_placebo_overlap([3, 9], 3, 12)
        self.assertEqual(r['n_overlapping_pairs'], 0)
        self.assertEqual(r['nonoverlapping_cut_subset'], [3, 9])
    def test_touching_boundary(self):
        self.assertEqual(audit_placebo_overlap([2, 6], 2, 8)['n_overlapping_pairs'], 0)
    def test_bad_inputs(self):
        for args in [([3, 3], 2, 8), ([3, 2], 2, 8), ([1], 2, 8), ([3], 2, 4), ([3], True, 8), ([3.0], 2, 8)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                audit_placebo_overlap(*args)

if __name__ == '__main__': unittest.main()
