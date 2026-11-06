"""Audit published window placebo denominators and arithmetic; descriptive only."""
import csv
import json
import math
import sys

def audit(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {"outcome", "window_days", "november_pp", "october6_pp", "nov_minus_oct_pp",
                "pre_placebo_count", "pre_placebo_at_least_as_negative", "pre_placebo_at_least_as_extreme_abs"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("missing fields")
    pairs = {}
    for row in rows:
        outcome = row["outcome"]
        window = int(row["window_days"])
        pair = pairs.setdefault(window, {})
        if outcome not in ("count", "volume") or window <= 0 or outcome in pair:
            raise ValueError("invalid or duplicate outcome/window")
        nov, oct_, diff = (float(row[k]) for k in ("november_pp", "october6_pp", "nov_minus_oct_pp"))
        n, negative, absolute = (int(row[k]) for k in ("pre_placebo_count", "pre_placebo_at_least_as_negative", "pre_placebo_at_least_as_extreme_abs"))
        if (not all(map(math.isfinite, (nov, oct_, diff))) or abs(nov - oct_ - diff) > 0.000002
                or not (n > 0 and 0 <= negative <= n and 0 <= absolute <= n)):
            raise ValueError("invalid arithmetic or placebo counts")
        pair[outcome] = (diff, n, negative, absolute)
    if any(set(pair) != {"count", "volume"} for pair in pairs.values()):
        raise ValueError("unpaired outcomes")
    result = []
    for window, pair in sorted(pairs.items()):
        count, volume = pair["count"], pair["volume"]
        if count[1] != volume[1]:
            raise ValueError("different placebo denominators")
        result.append({"window_days": window, "placebo_count": count[1],
                       "count_abs_fraction": count[3] / count[1],
                       "volume_abs_fraction": volume[3] / volume[1],
                       "volume_minus_count_abs_fraction": (volume[3] - count[3]) / count[1]})
    return {"windows": result,
            "denominator_range": [min(r["placebo_count"] for r in result), max(r["placebo_count"] for r in result)],
            "same_denominator_all_windows": len({r["placebo_count"] for r in result}) == 1,
            "warning": "Overlapping placebo windows: fractions are descriptive, not calibrated p-values."}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/phase180_placebo_denominator_audit.py results/phase131_window_sensitivity.csv")
    print(json.dumps(audit(sys.argv[1]), indent=2))
