"""Audit exact eligible placebo-date memberships, without estimating market effects.

Input CSV columns: window_days,placebo_date,outcome
Each row denotes one eligible cutoff for one outcome/window.
"""
import csv
import json
import sys
from datetime import date

WINDOWS = (3, 5, 7, 10, 15)
OUTCOMES = ("count", "volume")

def audit(rows, expected_counts=None):
    sets = {(w, o): set() for w in WINDOWS for o in OUTCOMES}
    for row in rows:
        if set(row) != {"window_days", "placebo_date", "outcome"}:
            raise ValueError("unexpected membership schema")
        try:
            w = int(row["window_days"])
            d = date.fromisoformat(row["placebo_date"]).isoformat()
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid window or ISO date") from exc
        o = row["outcome"]
        if w not in WINDOWS or o not in OUTCOMES:
            raise ValueError("unexpected window or outcome")
        key = (w, o)
        if d in sets[key]:
            raise ValueError("duplicate membership")
        sets[key].add(d)
    if any(not dates for dates in sets.values()):
        raise ValueError("empty window/outcome membership")
    for w in WINDOWS:
        if sets[w, "count"] != sets[w, "volume"]:
            raise ValueError("count and volume eligible dates differ")
        if expected_counts is not None and len(sets[w, "count"]) != expected_counts[w]:
            raise ValueError("membership disagrees with published denominator")
    common = set.intersection(*(sets[w, "count"] for w in WINDOWS))
    union = set.union(*(sets[w, "count"] for w in WINDOWS))
    nested = all(sets[b, "count"] <= sets[a, "count"] for a, b in zip(WINDOWS, WINDOWS[1:]))
    return {"counts": {str(w): len(sets[w, "count"]) for w in WINDOWS},
            "union_size": len(union), "intersection_size": len(common),
            "common_dates": sorted(common), "nested_eligibility": nested,
            "warning": "Memberships alone do not identify placebo contrasts or causal effects."}

def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["window_days", "placebo_date", "outcome"]:
            raise ValueError("expected window_days,placebo_date,outcome")
        return audit(list(reader), {3:82, 5:78, 7:74, 10:68, 15:58})

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/phase182_membership_audit.py membership.csv")
    print(json.dumps(load(sys.argv[1]), indent=2))
