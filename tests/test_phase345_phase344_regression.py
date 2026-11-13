"""Regression checks for the published Phase 344 support/attrition diagnostic.

Run: python -m unittest discover -s tests -p 'test_phase345_phase344_regression.py'
Synthetic observations only; no SEC source authentication implied.
"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("phase344", ROOT / "scripts" / "phase344_support_attrition.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def row(sec, day, exchange, treated, group, num, den=10):
    return dict(security=sec, date=day, exchange=exchange, treated=str(treated),
                match_group=group, numerator=str(num), denominator=str(den))


class SupportAttritionRegression(unittest.TestCase):
    def test_equal_group_not_equal_cell(self):
        data = [
            row("t1", "2025-09-01", "X", 1, "A", 9),
            row("c1", "2025-09-01", "X", 0, "A", 1),
            row("t1", "2025-09-02", "X", 1, "A", 9),
            row("c1", "2025-09-02", "X", 0, "A", 1),
            row("t2", "2025-09-01", "X", 1, "B", 1),
            row("c2", "2025-09-01", "X", 0, "B", 9),
        ]
        result = MOD.analyze(data)
        self.assertAlmostEqual(result["equal_group_pp"], 0)
        self.assertEqual(result["paired_cells"], 3)
        self.assertEqual(result["supported_groups"], 2)

    def test_exchange_nonoverlap_is_unsupported(self):
        result = MOD.analyze([
            row("t", "2025-09-01", "X", 1, "A", 8),
            row("c", "2025-09-01", "Y", 0, "A", 2),
        ])
        self.assertEqual(result["paired_cells"], 0)
        self.assertIsNone(result["equal_group_pp"])
        self.assertEqual(result["unsupported_cells"], {"treated_only": 1, "control_only": 1})

    def test_leave_one_group_out_single_group_undefined(self):
        result = MOD.analyze([
            row("t", "2025-09-01", "X", 1, "A", 8),
            row("c", "2025-09-01", "X", 0, "A", 2),
        ])
        self.assertEqual(result["leave_one_group_out"]["undefined"], 1)
        self.assertEqual(result["leave_one_date_out"]["undefined"], 1)

    def test_duplicate_rejected(self):
        data = [row("t", "2025-09-01", "X", 1, "A", 8)]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            MOD.analyze(data + data)

    def test_assignment_drift_rejected(self):
        with self.assertRaisesRegex(ValueError, "assignment drift"):
            MOD.analyze([
                row("t", "2025-09-01", "X", 1, "A", 8),
                row("t", "2025-09-02", "X", 0, "A", 2),
            ])

    def test_nonfinite_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid numerator/denominator"):
            MOD.analyze([row("t", "2025-09-01", "X", 1, "A", "nan")])

    def test_noncanonical_date_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid date"):
            MOD.analyze([row("t", "2025-9-1", "X", 1, "A", 8)])


if __name__ == "__main__":
    unittest.main()
