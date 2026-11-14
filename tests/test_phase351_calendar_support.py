import unittest
from scripts.phase351_calendar_support import audit_calendar_support as audit

S = ['2025-09-02', '2025-09-03', '2025-09-04', '2025-09-05']

class CalendarSupportTests(unittest.TestCase):
    def test_gap_is_not_true_adjacent(self):
        result = audit([('A', S[0], 1), ('A', S[2], 2), ('B', S[2], 3)], S)
        self.assertEqual(result['true_calendar_adjacent_pairs'], 0)
        self.assertEqual(result['gap_spanning_pairs'], [(S[0], S[2], 1)])
        self.assertEqual(result['missing_sessions'], [S[1], S[3]])
    def test_contiguous(self):
        result = audit([('A', d, 1) for d in S], S)
        self.assertEqual(result['true_calendar_adjacent_pairs'], 3)
        self.assertEqual(result['missing_sessions'], [])
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            audit([('A', S[0], 1), ('A', S[0], 2)], S)
    def test_off_calendar(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            audit([('A', '2025-09-06', 1)], S)
    def test_invalid_calendar(self):
        with self.assertRaises(ValueError): audit([('A', S[0], 1)], S[::-1])
    def test_noncanonical(self):
        with self.assertRaises(ValueError): audit([('A', '2025-9-2', 1)], S)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): audit([('A', S[0], float('nan'))], S)
    def test_bool(self):
        with self.assertRaises(ValueError): audit([('A', S[0], True)], S)
    def test_empty(self):
        with self.assertRaises(ValueError): audit([], S)
    def test_multiple_groups_same_day(self):
        result = audit([('A', S[0], 1), ('B', S[0], 2)], S)
        self.assertEqual(result['observed_sessions'], 1)
        self.assertEqual(result['observations'], 2)

if __name__ == '__main__': unittest.main()
