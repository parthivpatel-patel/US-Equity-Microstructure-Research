"""Deterministic audit: marginal overlap does not imply joint overlap."""
import unittest

def bounds(points):
    return [(min(p[j] for p in points), max(p[j] for p in points)) for j in (0, 1)]

def inside(point, limits):
    return all(lo <= x <= hi for x, (lo, hi) in zip(point, limits))

def marginal_overlap(a, b):
    aa, bb = bounds(a), bounds(b)
    return all(max(x[0], y[0]) <= min(x[1], y[1]) for x, y in zip(aa, bb))

def cross_group_near_pairs(a, b, tolerance):
    if tolerance < 0:
        raise ValueError('tolerance must be nonnegative')
    return sum(max(abs(x-y) for x,y in zip(p,q)) <= tolerance for p in a for q in b)

class JointSupportTests(unittest.TestCase):
    def setUp(self):
        self.treated = [(0.0, 0.0), (1.0, 1.0)]
        self.control = [(0.0, 1.0), (1.0, 0.0)]
    def test_both_marginal_ranges_identical(self):
        self.assertEqual(bounds(self.treated), bounds(self.control))
        self.assertTrue(marginal_overlap(self.treated, self.control))
    def test_every_observation_inside_other_bounding_box(self):
        self.assertTrue(all(inside(p, bounds(self.control)) for p in self.treated))
        self.assertTrue(all(inside(p, bounds(self.treated)) for p in self.control))
    def test_no_joint_near_neighbors(self):
        self.assertEqual(cross_group_near_pairs(self.treated, self.control, 0.49), 0)
    def test_pairs_emerge_at_full_unit_distance(self):
        self.assertEqual(cross_group_near_pairs(self.treated, self.control, 1.0), 4)
    def test_identical_points_are_near(self):
        self.assertEqual(cross_group_near_pairs(self.treated, self.treated, 0), 2)
    def test_negative_tolerance_rejected(self):
        with self.assertRaises(ValueError):
            cross_group_near_pairs(self.treated, self.control, -0.1)

if __name__ == '__main__':
    unittest.main()
