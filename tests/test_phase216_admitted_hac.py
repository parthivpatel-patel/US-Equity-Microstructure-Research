"""Synthetic integration tests, not historical results."""
import unittest
from datetime import date, timedelta
from scripts.phase216_admitted_hac import admitted_joint_hac


def fixture():
    days = [(date(2025, 9, 2) + timedelta(days=i)).isoformat() for i in range(24)]
    rows = [{'date': d, 'contrast': float(i % 4 + (i >= 12) * 3)} for i, d in enumerate(days)]
    return rows, days, (days[0], days[9]), (days[14], days[23])


class AdmittedHacTests(unittest.TestCase):
    def test_valid_and_metadata(self):
        r, c, e, l = fixture()
        out = admitted_joint_hac(r, c, e, l)
        self.assertEqual(out['admission']['gap_sessions'], 4)
        self.assertEqual(out['admission']['early_n'], 10)
        self.assertEqual(out['estimate']['early_n'], 10)
        self.assertFalse(out['historical_inference_validated'])
        self.assertFalse(out['causal_effect_established'])
        self.assertEqual(set(out['estimate']['hac_standard_errors']), {0, 1, 3})

    def test_missing_session_fails(self):
        r, c, e, l = fixture()
        with self.assertRaises(ValueError): admitted_joint_hac(r[:5]+r[6:], c, e, l)

    def test_calendar_missing_session_fails(self):
        r, c, e, l = fixture()
        with self.assertRaises(ValueError): admitted_joint_hac(r, c[:5]+c[6:], e, l)

    def test_duplicate_session_fails(self):
        r, c, e, l = fixture()
        with self.assertRaises(ValueError): admitted_joint_hac(r[:5]+[r[4]]+r[5:], c, e, l)

    def test_window_overlap_fails(self):
        r, c, e, l = fixture()
        with self.assertRaises(ValueError): admitted_joint_hac(r, c, e, (c[9], c[23]))

    def test_window_below_minimum_fails(self):
        r, c, e, l = fixture()
        with self.assertRaises(ValueError): admitted_joint_hac(r, c, e, l, min_per_window=11)

    def test_invalid_lag_fails(self):
        r, c, e, l = fixture()
        with self.assertRaises(ValueError): admitted_joint_hac(r, c, e, l, lags=(24,))

    def test_post_reform_fails(self):
        r, c, e, l = fixture()
        r[-1] = {'date': '2025-11-03', 'contrast': 1.0}
        c[-1] = '2025-11-03'
        with self.assertRaises(ValueError): admitted_joint_hac(r, c, e, l)


if __name__ == '__main__':
    unittest.main()
