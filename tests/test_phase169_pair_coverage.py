"""Phase 169: audit missing treatment-arm cells and fixed-roster coverage.

Constructed data only; no SEC estimates. Run: python -m unittest tests/test_phase169_pair_coverage.py
"""
from datetime import date
import math
import unittest


def audit_pairs(rows, expected_groups=None):
    cells = {}
    observed = set()
    for day, group, arm, outcome in rows:
        if not isinstance(day, str):
            raise ValueError("invalid date")
        try:
            parsed = date.fromisoformat(day)
        except ValueError as exc:
            raise ValueError("invalid date") from exc
        if parsed.isoformat() != day:
            raise ValueError("noncanonical date")
        if not isinstance(group, str) or not group.strip():
            raise ValueError("invalid group")
        if type(arm) is not int or arm not in (0, 1):
            raise ValueError("invalid arm")
        if isinstance(outcome, bool) or not isinstance(outcome, (int, float)) or not math.isfinite(outcome):
            raise ValueError("invalid outcome")
        key = (parsed, group, arm)
        if key in cells:
            raise ValueError("duplicate cell")
        cells[key] = float(outcome)
        observed.add(group)
    if not cells:
        raise ValueError("empty panel")
    if expected_groups is None:
        roster = observed
    else:
        if not isinstance(expected_groups, (list, tuple, set)):
            raise ValueError("invalid roster")
        roster = set(expected_groups)
        if not roster or len(roster) != len(expected_groups) or any(
            not isinstance(g, str) or not g.strip() for g in roster
        ):
            raise ValueError("invalid roster")
        if not observed <= roster:
            raise ValueError("unknown group")
    report = []
    for day in sorted({k[0] for k in cells}):
        complete = sum((day, g, 0) in cells and (day, g, 1) in cells for g in roster)
        partial = sum(((day, g, 0) in cells) != ((day, g, 1) in cells) for g in roster)
        absent = len(roster) - complete - partial
        report.append({"date": day.isoformat(), "complete": complete,
                       "partial": partial, "absent": absent, "roster": len(roster),
                       "coverage": complete / len(roster)})
    return report


class Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [("2025-10-01", "A", 0, 1), ("2025-10-01", "A", 1, 2),
                     ("2025-10-02", "A", 0, 1), ("2025-10-02", "A", 1, 2)]

    def test_complete(self):
        self.assertEqual([x["coverage"] for x in audit_pairs(self.rows)], [1, 1])

    def test_partial(self):
        x = audit_pairs(self.rows + [("2025-10-02", "B", 0, 1)])
        self.assertEqual((x[1]["complete"], x[1]["partial"], x[1]["coverage"]), (1, 1, .5))

    def test_absent_requires_roster(self):
        x = audit_pairs(self.rows, ["A", "B"])
        self.assertEqual((x[0]["absent"], x[0]["coverage"]), (1, .5))

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            audit_pairs(self.rows + [self.rows[0]])

    def test_bad_date(self):
        with self.assertRaises(ValueError):
            audit_pairs([("2025-9-30", "A", 0, 1)])

    def test_unknown_group(self):
        with self.assertRaises(ValueError):
            audit_pairs(self.rows, ["B"])

    def test_duplicate_roster(self):
        with self.assertRaises(ValueError):
            audit_pairs(self.rows, ["A", "A"])

    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            audit_pairs([("2025-10-01", "A", 0, float("nan"))])

    def test_empty(self):
        with self.assertRaises(ValueError):
            audit_pairs([])


if __name__ == "__main__":
    unittest.main()
