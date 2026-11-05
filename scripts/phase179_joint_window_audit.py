"""Descriptive cross-outcome window audit of published summary data, not causal inference."""
import csv
import json
import math
import sys

def audit(path):
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {"outcome", "window_days", "nov_minus_oct_pp", "pre_placebo_count", "pre_placebo_at_least_as_extreme_abs"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Missing rows or columns")
    windows = {}
    for row in rows:
        outcome = row["outcome"]
        if outcome not in ("count", "volume"):
            raise ValueError("Unexpected outcome")
        window = int(row["window_days"])
        pair = windows.setdefault(window, {})
        if window <= 0 or outcome in pair:
            raise ValueError("Invalid or duplicate window")
        effect = float(row["nov_minus_oct_pp"])
        n = int(row["pre_placebo_count"])
        k = int(row["pre_placebo_at_least_as_extreme_abs"])
        if not math.isfinite(effect) or n <= 0 or not 0 <= k <= n:
            raise ValueError("Invalid estimate or placebo count")
        pair[outcome] = (effect, k, n)
    if any(set(pair) != {"count", "volume"} for pair in windows.values()):
        raise ValueError("Unpaired window")
    output = []
    for window, pair in sorted(windows.items()):
        count, ck, cn = pair["count"]
        volume, vk, vn = pair["volume"]
        output.append({"window_days": window, "count_pp": count, "volume_pp": volume,
                       "volume_minus_count_pp": round(volume - count, 6),
                       "opposite_sign": count * volume < 0,
                       "count_abs_placebo_fraction": ck / cn,
                       "volume_abs_placebo_fraction": vk / vn,
                       "placebo_denominators_equal": cn == vn})
    return {"windows": output, "window_count": len(output),
            "opposite_sign_windows": sum(row["opposite_sign"] for row in output),
            "count_sign_changes": sum((a["count_pp"] > 0) != (b["count_pp"] > 0) for a, b in zip(output, output[1:])),
            "volume_sign_changes": sum((a["volume_pp"] > 0) != (b["volume_pp"] > 0) for a, b in zip(output, output[1:]))}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/phase179_joint_window_audit.py CSV")
    print(json.dumps(audit(sys.argv[1]), indent=2))
