import unittest
from itertools import combinations
from phase255_placebo_effective_count import overlap_components

class TestOverlap(unittest.TestCase):
    def test_chain_overlap(self):
        x=overlap_components([5,8,11],3,20)
        self.assertEqual(x['component_count'],1)
        self.assertEqual(x['max_disjoint_windows'],2)
    def test_touching_windows_are_disjoint(self):
        x=overlap_components([3,9,15],3,18)
        self.assertEqual(x['component_count'],3)
        self.assertEqual(x['max_disjoint_windows'],3)
    def test_greedy_matches_brute_force(self):
        for cuts in ([3,4,5,6,9,12], [4,7,8,12,16], [3,9,15]):
            x=overlap_components(cuts,3,24)
            optimum=max(len(s) for n in range(len(cuts)+1) for s in combinations(cuts,n)
                        if all(b-a>=6 for a,b in zip(s,s[1:])))
            self.assertEqual(x['max_disjoint_windows'],optimum)
    def test_invalid(self):
        for cuts in ([3,3], [2,5], [5,4], [3,22]):
            with self.assertRaises(ValueError): overlap_components(cuts,3,24)
    def test_boolean_rejected(self):
        with self.assertRaises(ValueError): overlap_components([True,6],3,24)

if __name__=='__main__': unittest.main()
