"""Synthetic integration regression; never evidence of an historical reform effect."""
import unittest
from datetime import date
from scripts.phase218_weekday_fixture import weekday_fixture
from scripts.phase216_admitted_hac import admitted_joint_hac

class WeekdayIntegrationTests(unittest.TestCase):
    def test_weekend_free_fixture_passes_admission(self):
        rows, sessions, early, late = weekday_fixture()
        self.assertTrue(all(date.fromisoformat(d).weekday() < 5 for d in sessions))
        out = admitted_joint_hac(rows, sessions, early, late)
        self.assertEqual(out['admission']['early_n'], 10)
        self.assertEqual(out['admission']['late_n'], 10)
        self.assertEqual(out['admission']['gap_sessions'], 4)
        self.assertFalse(out['historical_inference_validated'])
        self.assertFalse(out['causal_effect_established'])

    def test_missing_session_rejected(self):
        rows, sessions, early, late = weekday_fixture()
        with self.assertRaises(ValueError):
            admitted_joint_hac(rows[:12]+rows[13:], sessions, early, late)

    def test_no_reform_intrusion(self):
        with self.assertRaises(ValueError):
            weekday_fixture('2025-10-31', 24)

    def test_bandwidths_present(self):
        rows, sessions, early, late = weekday_fixture()
        out = admitted_joint_hac(rows, sessions, early, late, lags=(0,1,3))
        self.assertEqual(set(out['estimate']['hac_standard_errors']), {0,1,3})

if __name__ == '__main__':
    unittest.main()
