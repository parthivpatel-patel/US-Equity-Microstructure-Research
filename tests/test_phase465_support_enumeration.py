import unittest
from phase465_support_enumeration import enumerate_support

S = ['2025-09-%02d' % i for i in range(1, 7)]

class ExactSupportTests(unittest.TestCase):
    def test_phase464_joint(self):
        r = enumerate_support(S, [S[1], S[3]], 3)
        self.assertEqual((r['total_paths'], r['eligible_joint']), (16, 6))
        self.assertEqual(r['eligible_per_cutoff'], {S[1]: 7, S[3]: 14})
    def test_single_session_blocks(self):
        r = enumerate_support(S[:2], [S[1]], 1)
        self.assertEqual((r['total_paths'], r['eligible_joint']), (4, 2))
    def test_full_block(self):
        r = enumerate_support(S, [S[1], S[3]], 6)
        self.assertEqual((r['total_paths'], r['eligible_joint']), (1, 1))
    def test_outside(self):
        with self.assertRaises(ValueError): enumerate_support(S, [S[0]], 3)
    def test_duplicates(self):
        with self.assertRaises(ValueError): enumerate_support(S, [S[1], S[1]], 3)
    def test_path_limit(self):
        with self.assertRaises(ValueError): enumerate_support(S, [S[1]], 1, max_paths=10)
    def test_unsorted(self):
        with self.assertRaises(ValueError): enumerate_support(S[::-1], [S[1]], 3)
    def test_invalid_block(self):
        with self.assertRaises(ValueError): enumerate_support(S, [S[1]], 0)

if __name__ == '__main__': unittest.main()
