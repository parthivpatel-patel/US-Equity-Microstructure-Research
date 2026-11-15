"""Descriptive overlap audit for observed placebo trading-session windows."""
import argparse
import datetime as dt
import json
from collections import Counter

def audit(records):
    if not isinstance(records, list) or not records:
        raise ValueError("nonempty list required")
    windows = {}
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            raise ValueError("nonempty string id required")
        key = row["id"]
        if key in windows:
            raise ValueError("duplicate id")
        dates = row.get("sessions")
        if not isinstance(dates, list) or not dates:
            raise ValueError("nonempty session list required")
        parsed = []
        for date in dates:
            if not isinstance(date, str) or dt.date.fromisoformat(date).isoformat() != date:
                raise ValueError("invalid ISO session")
            parsed.append(date)
        if len(parsed) != len(set(parsed)):
            raise ValueError("duplicate session within window")
        windows[key] = set(parsed)
    keys = sorted(windows)
    pairs = []
    for i, left in enumerate(keys):
        for right in keys[i + 1:]:
            common = len(windows[left] & windows[right])
            union = len(windows[left] | windows[right])
            pairs.append(dict(left=left, right=right, shared_sessions=common,
                              jaccard=common / union, identical=common == union))
    counts = Counter(date for dates in windows.values() for date in dates)
    total = sum(counts.values())
    concentration = sum(n*n for n in counts.values())
    return dict(window_count=len(keys), unique_sessions=len(counts),
                session_appearances=total, max_session_reuse=max(counts.values()),
                identical_window_pairs=sum(p["identical"] for p in pairs),
                overlapping_pairs=sum(p["shared_sessions"] > 0 for p in pairs),
                pair_count=len(pairs), pairs=pairs,
                session_reuse_effective_count=total*total/concentration,
                interpretation="descriptive overlap only; not an effective number of independent placebo estimates")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    args = parser.parse_args()
    with open(args.json_file, encoding="utf-8") as f:
        print(json.dumps(audit(json.load(f)), indent=2, sort_keys=True))
