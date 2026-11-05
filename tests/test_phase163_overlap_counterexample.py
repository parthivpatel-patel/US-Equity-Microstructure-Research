"""Deterministic common-range overlap counterexample; no market observations."""
import math
import unittest

def diagnostics(treated, comparison):
    if not treated or not comparison:
        raise ValueError('both groups required')
    if any(not math.isfinite(x) for x in treated + comparison):
        raise ValueError('finite baselines required')
    lo = max(min(treated), min(comparison))
    hi = min(max(treated), max(comparison))
    if lo > hi:
        return {'overlap': False, 'treated_in': 0, 'comparison_in': 0}
    return {'overlap': True,
            'treated_in': sum(lo <= x <= hi for x in treated),
            'comparison_in': sum(lo <= x <= hi for x in comparison)}

class OverlapTests(unittest.TestCase):
    def test_range_overlap_can_hide_near_disjoint_samples(self):
        a = [0.10] * 99 + [0.50]
        b = [0.50] + [0.90] * 99
        d = diagnostics(a, b)
        self.assertTrue(d['overlap'])
        self.assertEqual((d['treated_in'], d['comparison_in']), (1, 1))

    def test_disjoint_ranges(self):
        self.assertFalse(diagnostics([0.1, 0.2], [0.8, 0.9])['overlap'])

    def test_complete_overlap(self):
        d = diagnostics([0.2, 0.8], [0.2, 0.8])
        self.assertEqual((d['treated_in'], d['comparison_in']), (2, 2))

    def test_single_boundary_point(self):
        d = diagnostics([0.1, 0.5], [0.5, 0.9])
        self.assertEqual((d['treated_in'], d['comparison_in']), (1, 1))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): diagnostics([], [0.1])
        with self.assertRaises(ValueError): diagnostics([math.nan], [0.1])

if __name__ == '__main__':
    unittest.main()
