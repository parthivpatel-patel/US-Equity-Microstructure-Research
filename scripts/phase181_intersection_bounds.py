"""Partial-identification bounds for common placebo dates from aggregate counts.

Combinatorial bounds only, not market estimates.
"""
import csv
import json
import sys

def bounds(counts, universe_size):
    if not counts or any(type(n) is not int or n < 0 for n in counts):
        raise ValueError("counts must be nonempty nonnegative integers")
    if type(universe_size) is not int or universe_size < max(counts):
        raise ValueError("universe must contain every eligible set")
    return {"lower": max(0, sum(counts) - (len(counts) - 1) * universe_size),
            "upper": min(counts)}

def audit(path, universe_sizes=(82, 90, 100)):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {"outcome", "window_days", "pre_placebo_count"}.issubset(reader.fieldnames):
            raise ValueError("missing fields")
        rows = list(reader)
    by_outcome = {}
    for r in rows:
        o = r["outcome"]
        if o not in ("count", "volume"):
            raise ValueError("unknown outcome")
        w, n = int(r["window_days"]), int(r["pre_placebo_count"])
        if w <= 0 or n <= 0 or w in by_outcome.setdefault(o, {}):
            raise ValueError("invalid or duplicate window")
        by_outcome[o][w] = n
    if not by_outcome or set(by_outcome) != {"count", "volume"} or by_outcome["count"] != by_outcome["volume"]:
        raise ValueError("outcomes must have identical window denominators")
    counts = by_outcome["count"]
    return {"window_counts": dict(sorted(counts.items())),
            "sum_memberships": sum(counts.values()),
            "conditional_common_date_bounds": {str(n): bounds(list(counts.values()), n) for n in universe_sizes},
            "warning": "Universe sizes are hypothetical; eligible date identities are absent. Common-date contrasts cannot be reconstructed."}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/phase181_intersection_bounds.py results/phase131_window_sensitivity.csv")
    print(json.dumps(audit(sys.argv[1]), indent=2))
