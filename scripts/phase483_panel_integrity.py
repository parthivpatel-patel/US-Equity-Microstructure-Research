"""Calendar-based panel integrity checks; no SEC observations bundled."""
import csv
import datetime as dt
import hashlib
import json
import math
import argparse
from collections import Counter, defaultdict

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def audit(panel, calendar, cutoff):
    with open(calendar, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        if r.fieldnames != ["date"]:
            raise ValueError("calendar requires exactly one date column")
        dates = [row["date"].strip() for row in r]
    if not dates or dates != sorted(set(dates)):
        raise ValueError("calendar must be nonempty, sorted and unique")
    for day in dates:
        if dt.date.fromisoformat(day).isoformat() != day:
            raise ValueError("noncanonical date")
    if cutoff not in dates[1:-1]:
        raise ValueError("cutoff must leave dates on both sides")
    pre = {d for d in dates if d < cutoff}
    post = set(dates) - pre
    seen = set()
    units = defaultdict(set)
    counts = Counter()
    with open(panel, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        if not {"security", "date", "exchange", "value"}.issubset(r.fieldnames or []):
            raise ValueError("missing panel columns")
        for row in r:
            s, d, e = (row[k].strip() for k in ("security", "date", "exchange"))
            if not s or not e or d not in dates:
                raise ValueError("blank key or off-calendar observation")
            key = (s, d, e)
            if key in seen:
                raise ValueError("duplicate security-date-exchange")
            value = float(row["value"])
            if not math.isfinite(value):
                raise ValueError("nonfinite value")
            seen.add(key)
            units[(s, e)].add(d)
            counts["zero" if value == 0 else "nonzero"] += 1
    if not seen:
        raise ValueError("empty panel")
    categories = Counter()
    for observed in units.values():
        a, b = pre <= observed, post <= observed
        categories["complete_both" if a and b else "complete_pre_only" if a else "complete_post_only" if b else "incomplete_both"] += 1
    return {
        "input_sha256": {"panel": digest(panel), "calendar": digest(calendar)},
        "cutoff": cutoff, "pre_dates": len(pre), "post_dates": len(post),
        "observed_rows": len(seen), "observed_zeros": counts["zero"],
        "union_security_exchange_units": len(units),
        "missing_rows_against_observed_union": len(units) * len(dates) - len(seen),
        "coverage_categories": {k: categories[k] for k in ("complete_both", "complete_pre_only", "complete_post_only", "incomplete_both")},
        "authentication_status": "UNVERIFIED: SHA256 identifies bytes, not SEC origin or redistribution rights",
        "interpretation": "Missing rows are not zeros; observed union is not an authenticated listing universe."
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("panel")
    p.add_argument("calendar")
    p.add_argument("cutoff")
    a = p.parse_args()
    print(json.dumps(audit(a.panel, a.calendar, a.cutoff), indent=2, sort_keys=True))
