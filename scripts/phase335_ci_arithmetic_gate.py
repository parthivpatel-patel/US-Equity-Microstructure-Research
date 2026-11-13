#!/usr/bin/env python3
"""Check published CI arithmetic only; does not authenticate SEC source data."""
import argparse
import csv
import json
from decimal import Decimal as D

def audit(rows):
    results = []
    seen = set()
    for row in rows:
        key = (row["outcome"], row["period"], int(row["hac_lag"]))
        if key in seen:
            raise ValueError("duplicate outcome/period/lag")
        seen.add(key)
        slope, se, lo, hi = (D(row[k]) for k in
            ("slope_pp_per_trading_day", "two_way_se", "two_way_ci_low", "two_way_ci_high"))
        if not (se > 0 and lo <= slope <= hi):
            raise ValueError("invalid standard error or interval")
        center_error = (lo + hi) / 2 - slope
        implied = (hi - lo) / (2 * se)
        if abs(center_error) > D("0.000001") or abs(implied - D("1.96")) > D("0.0002"):
            raise ValueError("CI inconsistent with displayed slope, SE, and 1.96 multiplier")
        results.append((key, center_error, implied))
    expected = {(o,p,l) for o in ("count","volume")
                for p in ("Jul-Sep","Jul-Oct") for l in (0,3,5,10,15)}
    if seen != expected:
        raise ValueError("incomplete or unexpected 20-row grid")
    return {"rows":len(results),
            "min_implied_multiplier":str(min(x[2] for x in results)),
            "max_implied_multiplier":str(max(x[2] for x in results)),
            "max_abs_center_error":str(max(abs(x[1]) for x in results))}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("csv_path")
    args = p.parse_args()
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        print(json.dumps(audit(list(csv.DictReader(f))), indent=2))
