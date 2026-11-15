import unittest
from scripts.phase382_placebo_overlap import audit_placebo_overlap

def row(boundary, pre, post, eligible=True):
    return {'boundary': boundary, 'pre': tuple(pre), 'post': tuple(post), 'eligible': eligible}

class PlaceboOverlapTests(unittest.TestCase):
    def test_identical_windows(self):
        a = audit_placebo_overlap({'results': [row('a',['1'],['2']),row('b',['1'],['2'])]})
        self.assertEqual(a['duplicate_window_pairs'], (('a','b'),))
        self.assertEqual(a['overlap_components'], (('a','b'),))
    def test_disjoint_windows(self):
        a = audit_placebo_overlap({'results': [row('a',['1'],['2']),row('b',['3'],['4'])]})
        self.assertFalse(a['overlapping_pairs'])
        self.assertEqual(len(a['overlap_components']), 2)
    def test_transitive_overlap_not_independence(self):
        a = audit_placebo_overlap({'results': [row('a',['1'],['2']),row('b',['2'],['3']),row('c',['3'],['4'])]})
        self.assertEqual(len(a['overlapping_pairs']), 2)
        self.assertEqual(a['overlap_components'], (('a','b','c'),))
    def test_ineligible_ignored(self):
        a = audit_placebo_overlap({'results': [row('a',['1'],['2']),row('b',['1'],['2'],False)]})
        self.assertEqual(a['eligible_boundaries'],1)
    def test_duplicate_boundary_rejected(self):
        with self.assertRaises(ValueError): audit_placebo_overlap({'results':[row('a',['1'],['2']),row('a',['3'],['4'])]})
    def test_within_window_overlap_rejected(self):
        with self.assertRaises(ValueError): audit_placebo_overlap({'results':[row('a',['1'],['1'])]})
    def test_unsorted_sessions_rejected(self):
        with self.assertRaises(ValueError): audit_placebo_overlap({'results':[row('a',['2','1'],['3'])]})
    def test_empty(self):
        a = audit_placebo_overlap({'results':[]})
        self.assertEqual(a['overlap_components'],())

if __name__ == '__main__': unittest.main()
