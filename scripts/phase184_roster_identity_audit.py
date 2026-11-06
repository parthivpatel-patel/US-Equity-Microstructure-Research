"""Strict balanced common-date matched-group identity audit; descriptive only."""
import csv
import json
import math
import sys
from collections import defaultdict
from datetime import date

WINDOWS = (3, 5, 7, 10, 15)
OUTCOMES = ("count", "volume")
FIELDS = ("window_days", "placebo_date", "outcome", "matched_group_id", "contrast_pp")

def audit(rows):
    values = {}
    rosters = defaultdict(set)
    for row in rows:
        if set(row) != set(FIELDS):
            raise ValueError("schema mismatch")
        d = row["placebo_date"]
        if len(d) != 10 or date.fromisoformat(d).isoformat() != d:
            raise ValueError("invalid ISO date")
        raw_w = row["window_days"]
        if not raw_w.isdigit() or int(raw_w) not in WINDOWS:
            raise ValueError("invalid window")
        w = int(raw_w)
        o, g = row["outcome"], row["matched_group_id"]
        if o not in OUTCOMES or not g or g.strip() != g:
            raise ValueError("invalid outcome/group")
        v = float(row["contrast_pp"])
        if not math.isfinite(v):
            raise ValueError("nonfinite contrast")
        key = (w, d, o, g)
        if key in values:
            raise ValueError("duplicate group observation")
        values[key] = v
        rosters[w, d, o].add(g)
    if not values:
        raise ValueError("empty input")
    dates = {}
    for w in WINDOWS:
        a = {d for ww, d, o in rosters if ww == w and o == "count"}
        b = {d for ww, d, o in rosters if ww == w and o == "volume"}
        if not a or a != b:
            raise ValueError("outcome date mismatch or missing window")
        dates[w] = a
        for d in a:
            if rosters[w, d, "count"] != rosters[w, d, "volume"]:
                raise ValueError("count/volume roster identity mismatch")
    common = set.intersection(*(dates.values()))
    if not common:
        raise ValueError("no common dates")
    roster_sets = [rosters[w, d, "count"] for w in WINDOWS for d in common]
    if any(s != roster_sets[0] for s in roster_sets[1:]):
        raise ValueError("roster changes across common dates/windows")
    groups = sorted(roster_sets[0])
    means = {}
    for w in WINDOWS:
        means[str(w)] = {}
        for o in OUTCOMES:
            sample = [values[w, d, o, g] for d in sorted(common) for g in groups]
            means[str(w)][o] = math.fsum(sample) / len(sample)
    return {"common_dates": sorted(common), "fixed_group_ids": groups,
            "window_date_counts": {str(w): len(dates[w]) for w in WINDOWS},
            "balanced_equal_group_date_means_pp": means,
            "warning": "Descriptive only; source/treatment authentication and dependence-aware inference not established."}

def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("CSV header mismatch")
        return audit(list(reader))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/phase184_roster_identity_audit.py group_contrasts.csv")
    print(json.dumps(load(sys.argv[1]), indent=2))
