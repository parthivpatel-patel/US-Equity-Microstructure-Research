"""Balanced matched-group composition audit; deterministic fixtures only."""
import math
import unittest
from collections import defaultdict

def balanced_contrasts(rows, cutoff):
    cells = {}
    for date, group, arm, outcome in rows:
        if arm not in (0, 1) or not isinstance(outcome, (int, float)) or not math.isfinite(outcome):
            raise ValueError("invalid arm/outcome")
        key = (date, group, arm)
        if key in cells:
            raise ValueError("duplicate cell")
        cells[key] = float(outcome)
    dates = sorted({d for d, _, _ in cells})
    if not dates or not any(d < cutoff for d in dates) or not any(d >= cutoff for d in dates):
        raise ValueError("pre and post dates required")
    groups = sorted({g for _, g, _ in cells})
    eligible = [g for g in groups if all((d, g, arm) in cells for d in dates for arm in (0, 1))]
    if not eligible:
        raise ValueError("no balanced groups")
    contrasts = {d: sum(cells[d,g,1]-cells[d,g,0] for g in eligible)/len(eligible) for d in dates}
    return contrasts, {"all_groups":len(groups), "balanced_groups":len(eligible),
                       "excluded_groups":len(groups)-len(eligible), "dates":len(dates)}

def available_case_contrasts(rows):
    cells = defaultdict(dict)
    for d,g,a,y in rows:
        cells[(d,g)][a] = y
    bydate = defaultdict(list)
    for (d,g), arms in cells.items():
        if 0 in arms and 1 in arms:
            bydate[d].append(arms[1]-arms[0])
    return {d:sum(v)/len(v) for d,v in bydate.items()}

class CompositionTests(unittest.TestCase):
    def test_roster_creates_spurious_break(self):
        rows = []
        for d in ("01","02","03","04"):
            for g,effect in (("A",0.),("B",10.)):
                if g == "B" and d in ("01","02"): continue
                rows += [(d,g,0,100.),(d,g,1,100.+effect)]
        self.assertEqual([available_case_contrasts(rows)[d] for d in ("01","02","03","04")],
                         [0.,0.,5.,5.])
        balanced,audit = balanced_contrasts(rows,"03")
        self.assertEqual(list(balanced.values()),[0.,0.,0.,0.])
        self.assertEqual(audit["excluded_groups"],1)
    def test_complete_panel(self):
        rows = [(d,g,a,float(a)) for d in ("01","02") for g in ("A","B") for a in (0,1)]
        c,a = balanced_contrasts(rows,"02")
        self.assertEqual(c,{"01":1.,"02":1.})
        self.assertEqual(a["balanced_groups"],2)
    def test_duplicate_rejected(self):
        rows = [("01","A",0,0.),("01","A",0,0.),("01","A",1,1.),
                ("02","A",0,0.),("02","A",1,1.)]
        with self.assertRaises(ValueError): balanced_contrasts(rows,"02")
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            balanced_contrasts([("01","A",0,float("nan"))],"02")
    def test_no_balanced_group_rejected(self):
        rows = [("01","A",0,0.),("01","A",1,1.),("02","B",0,0.),("02","B",1,1.)]
        with self.assertRaises(ValueError): balanced_contrasts(rows,"02")
    def test_missing_period_rejected(self):
        with self.assertRaises(ValueError):
            balanced_contrasts([("01","A",0,0.),("01","A",1,1.)],"02")

if __name__ == "__main__":
    unittest.main()
