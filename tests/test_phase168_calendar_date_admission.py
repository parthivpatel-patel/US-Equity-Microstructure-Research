"""Phase 168: canonical calendar-date admission for matched daily contrasts.

Constructed fixtures only; not SEC empirical estimates.
"""
from datetime import date
import math
import unittest

def canonical_date(value):
    if not isinstance(value, str):
        raise ValueError("date must be text")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("invalid calendar date") from exc
    if parsed.isoformat() != value:
        raise ValueError("noncanonical ISO date")
    return parsed

def paired_contrasts(rows, cutoff):
    boundary = canonical_date(cutoff)
    cells = {}
    for day, group, arm, outcome in rows:
        d = canonical_date(day)
        if not isinstance(group, str) or not group.strip():
            raise ValueError("invalid group")
        if type(arm) is not int or arm not in (0, 1):
            raise ValueError("invalid arm")
        if isinstance(outcome, bool) or not isinstance(outcome, (int, float)) or not math.isfinite(outcome):
            raise ValueError("invalid outcome")
        key = (d, group, arm)
        if key in cells:
            raise ValueError("duplicate cell")
        cells[key] = float(outcome)
    days = sorted({d for d, _, _ in cells})
    groups = sorted({g for _, g, _ in cells})
    if not any(d < boundary for d in days) or not any(d >= boundary for d in days):
        raise ValueError("both periods required")
    pairs = {(d, g): cells[d, g, 1] - cells[d, g, 0]
             for d in days for g in groups
             if (d, g, 0) in cells and (d, g, 1) in cells}
    if any(not any((d, g) in pairs for g in groups) for d in days):
        raise ValueError("date without complete pair")
    balanced = [g for g in groups if all((d, g) in pairs for d in days)]
    available = {d.isoformat(): sum(pairs[d, g] for g in groups if (d, g) in pairs) /
                 sum((d, g) in pairs for g in groups) for d in days}
    fixed = ({d.isoformat(): sum(pairs[d, g] for g in balanced) / len(balanced)
              for d in days} if balanced else None)
    return {"available": available, "balanced": fixed, "balanced_groups": len(balanced),
            "paired_counts": {d.isoformat(): sum((d, g) in pairs for g in groups) for d in days}}

class Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [(d, "A", a, 10 + a * effect)
                     for d, effect in (("2025-10-01", 0), ("2025-10-02", 2)) for a in (0, 1)]
    def test_valid(self):
        self.assertEqual(list(paired_contrasts(self.rows, "2025-10-02")["balanced"].values()), [0, 2])
    def test_noncanonical(self):
        with self.assertRaises(ValueError): canonical_date("2025-9-30")
    def test_impossible(self):
        with self.assertRaises(ValueError): canonical_date("2025-02-30")
    def test_timestamp(self):
        with self.assertRaises(ValueError): canonical_date("2025-10-01T00:00:00")
    def test_duplicate(self):
        with self.assertRaises(ValueError): paired_contrasts(self.rows + [self.rows[0]], "2025-10-02")
    def test_unpaired_date(self):
        with self.assertRaises(ValueError): paired_contrasts(self.rows[:2] + [("2025-10-02", "A", 0, 1)], "2025-10-02")
    def test_boolean_arm(self):
        with self.assertRaises(ValueError): paired_contrasts(self.rows + [("2025-10-03", "B", True, 1)], "2025-10-02")
    def test_nonfinite(self):
        with self.assertRaises(ValueError): paired_contrasts(self.rows + [("2025-10-03", "B", 0, float("inf"))], "2025-10-02")
    def test_composition(self):
        rows = [(d, g, a, 100 + a * effect)
                for d in ("2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04")
                for g, effect in (("A", 0), ("B", 10))
                if not (g == "B" and d < "2025-10-03") for a in (0, 1)]
        x = paired_contrasts(rows, "2025-10-03")
        self.assertEqual(list(x["available"].values()), [0, 0, 5, 5])
        self.assertEqual(list(x["balanced"].values()), [0, 0, 0, 0])
    def test_no_balanced(self):
        rows = [("2025-10-01", "A", 0, 1), ("2025-10-01", "A", 1, 2),
                ("2025-10-02", "B", 0, 1), ("2025-10-02", "B", 1, 2)]
        self.assertIsNone(paired_contrasts(rows, "2025-10-02")["balanced"])

if __name__ == "__main__":
    unittest.main()
