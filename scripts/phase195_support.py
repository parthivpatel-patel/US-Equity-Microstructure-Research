"""Audit within-window pairing and across-window unit identity; not an estimator."""
from collections import defaultdict
from datetime import date
from math import isfinite

FIELDS = ("window", "date", "security", "exchange", "group", "outcome", "value")
OUTCOMES = {"count", "volume"}

def audit(rows):
    rows = list(rows)
    if not rows:
        raise ValueError("empty panel")
    seen, pairs = set(), defaultdict(set)
    daily = defaultdict(lambda: defaultdict(set))
    for r in rows:
        if any(k not in r for k in FIELDS):
            raise ValueError("missing field")
        w, d, s, e, g, o = (r[k] for k in FIELDS[:-1])
        if not all(isinstance(v, str) and v.strip() for v in (w, d, s, e, g)):
            raise ValueError("invalid identifier")
        try:
            parsed = date.fromisoformat(d)
        except (ValueError, TypeError):
            raise ValueError("invalid date") from None
        if parsed.isoformat() != d or parsed.weekday() >= 5:
            raise ValueError("noncanonical or weekend date")
        if o not in OUTCOMES:
            raise ValueError("invalid outcome")
        try:
            value = float(r["value"])
        except (TypeError, ValueError):
            raise ValueError("invalid value") from None
        if not isfinite(value):
            raise ValueError("nonfinite value")
        key = (w, d, s, e, g, o)
        if key in seen:
            raise ValueError("duplicate observation")
        seen.add(key)
        unit = (s, e, g)
        daily[w][d].add(unit)
        pairs[(w, d, *unit)].add(o)
    incomplete = sorted([list(k) for k, v in pairs.items() if v != OUTCOMES])
    rosters = {w: set.union(*days.values()) for w, days in daily.items()}
    drift = {w: sorted(d for d, units in days.items() if units != rosters[w])
             for w, days in daily.items()}
    windows = sorted(daily)
    comparisons = []
    for i, a in enumerate(windows):
        for b in windows[i + 1:]:
            comparisons.append({
                "windows": [a, b],
                "shared_units": len(rosters[a] & rosters[b]),
                "identical_units": rosters[a] == rosters[b],
                "shared_dates": len(set(daily[a]) & set(daily[b]))
            })
    return {
        "rows": len(rows),
        "incomplete_pairs": incomplete,
        "roster_drift_dates": drift,
        "cross_window": comparisons,
        "structurally_valid": not incomplete and all(not v for v in drift.values())
    }
