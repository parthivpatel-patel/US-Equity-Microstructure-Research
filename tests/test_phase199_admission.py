import unittest
from scripts.phase199_admission import admit


def pair(window='pre', date='2025-10-06', **overrides):
    base = dict(window=window, date=date, security='ABC', exchange='X', group='G', treated=True)
    base.update(overrides)
    return [dict(base, outcome='count'), dict(base, outcome='volume')]


class AdmissionTests(unittest.TestCase):
    def test_empty_rejected(self):
        self.assertEqual(admit([], ['pre'])['reasons'], ['empty_panel'])
    def test_valid_pair_admitted_structurally(self):
        r = admit(pair(), ['pre'])
        self.assertTrue(r['admitted'])
        self.assertFalse(r['audit']['treatment_authenticated'])
    def test_missing_expected_window(self):
        self.assertIn('window_mismatch', admit(pair(), ['pre', 'post'])['reasons'])
    def test_unexpected_window(self):
        self.assertIn('window_mismatch', admit(pair(), ['post'])['reasons'])
    def test_unpaired_rejected(self):
        self.assertIn('unpaired_entity_dates', admit(pair()[:1], ['pre'])['reasons'])
    def test_conflict_rejected(self):
        rows = pair(); rows[1]['treated'] = False
        self.assertIn('within_pair_assignment_conflicts', admit(rows, ['pre'])['reasons'])
    def test_two_windows_disjoint_dates(self):
        rows = pair() + pair('post', '2025-11-03')
        self.assertTrue(admit(rows, ['pre', 'post'])['admitted'])
    def test_duplicate_window_declaration(self):
        with self.assertRaises(ValueError): admit(pair(), ['pre', 'pre'])
    def test_empty_window_declaration(self):
        with self.assertRaises(ValueError): admit(pair(), [])
    def test_duplicate_observation_fails(self):
        rows = pair(); rows.append(dict(rows[0]))
        with self.assertRaises(ValueError): admit(rows, ['pre'])


if __name__ == '__main__':
    unittest.main()
