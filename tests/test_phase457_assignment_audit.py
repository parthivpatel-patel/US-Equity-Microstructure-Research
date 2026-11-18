"""Deterministic synthetic tests; no historical observations."""
import unittest
from scripts.phase457_assignment_audit import audit


def r(s="A", e="X", g="G", d="2025-10-31", t=True):
    return dict(security=s, exchange=e, matched_group=g, date=d, treated=t)


class AuditTests(unittest.TestCase):
    def test_consistent(self):
        a = audit([r(), r(d="2025-11-03"), r(s="B", t=False),
                   r(s="B", t=False, d="2025-11-03")])
        self.assertTrue(a["pass_assignment_consistency"])
        self.assertEqual(a["single_arm_group_periods"], [])

    def test_cross_exchange_conflict(self):
        self.assertEqual(audit([r(), r(e="Y", t=False)])["global_treatment_conflicts"], ["A"])

    def test_within_exchange_conflict(self):
        self.assertEqual(audit([r(), r(d="2025-11-03", g="H")])["exchange_assignment_conflicts"], [("A", "X")])

    def test_single_arm(self):
        self.assertEqual(audit([r()])["single_arm_group_periods"], [("X", "G", "pre")])

    def test_missing_period(self):
        self.assertEqual(audit([r()])["securities_missing_pre_or_post"], ["A"])

    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit([r(), r()])

    def test_bad_boolean(self):
        with self.assertRaisesRegex(ValueError, "boolean"):
            audit([r(t=1)])

    def test_empty(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            audit([])


if __name__ == "__main__":
    unittest.main()
