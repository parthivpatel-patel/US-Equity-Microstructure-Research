"""Strict row-level audit of common-date placebo contrasts; no causal inference."""
import csv
import json
import math
import re
import sys
from datetime import date

WINDOWS = (3, 5, 7, 10, 15)
OUTCOMES = ("count", "volume")
FIELDS = ("window_days", "placebo_date", "outcome", "contrast_pp", "matched_groups")

def audit(rows):
    records = {}
    for row in rows:
        if set(row) != set(FIELDS):
            raise ValueError("invalid schema")
        raw = row["placebo_date"]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
            raise ValueError("date must be YYYY-MM-DD")
        day = date.fromisoformat(raw).isoformat()
        window = int(row["window_days"])
        outcome = row["outcome"]
        if window not in WINDOWS or outcome not in OUTCOMES:
            raise ValueError("invalid window/outcome")
        value = float(row["contrast_pp"])
        roster = int(row["matched_groups"])
        if not math.isfinite(value) or roster <= 0:
            raise ValueError("nonfinite value or empty roster")
        key = (window, day, outcome)
        if key in records:
            raise ValueError("duplicate row")
        records[key] = (value, roster)
    windows = {}
    for window in WINDOWS:
        a = {d: v for (w, d, o), v in records.items() if w == window and o == "count"}
        b = {d: v for (w, d, o), v in records.items() if w == window and o == "volume"}
        if not a or set(a) != set(b):
            raise ValueError("outcome-specific date mismatch")
        if any(a[d][1] != b[d][1] for d in a):
            raise ValueError("roster count mismatch")
        windows[window] = a
    common = set.intersection(*(set(windows[w]) for w in WINDOWS))
    if not common:
        raise ValueError("no shared dates")
    return {"window_counts": {str(w): len(windows[w]) for w in WINDOWS},
            "common_dates": sorted(common),
            "common_count_means_pp": {str(w): sum(windows[w][d][0] for d in common) / len(common) for w in WINDOWS},
            "warning": "Descriptive only; roster identities and dependence-aware inference not validated."}

def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("invalid CSV header")
        return audit(list(reader))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/phase183_common_date_audit.py contrasts.csv")
    print(json.dumps(load(sys.argv[1]), indent=2))
