#!/usr/bin/env python3
"""Audit published pretrend precision across HAC lag choices; not raw SEC estimates."""
import argparse
import csv
import json

def audit(rows):
    groups = {}
    for row in rows:
        key = (row["outcome"], row["period"])
        lag = int(row["hac_lag"])
        d = groups.setdefault(key, {})
        if lag in d:
            raise ValueError("duplicate lag")
        low, high = float(row["two_way_ci_low"]), float(row["two_way_ci_high"])
        slope, se = float(row["slope_pp_per_trading_day"]), float(row["two_way_se"])
        if not low <= slope <= high or se <= 0:
            raise ValueError("invalid interval or SE")
        d[lag] = (slope, se, low > 0 or high < 0)
    expected = {(o,p) for o in ("count","volume") for p in ("Jul-Sep","Jul-Oct")}
    if set(groups) != expected:
        raise ValueError("unexpected outcome-period groups")
    result = []
    for key in sorted(groups):
        d = groups[key]
        if set(d) != {0,3,5,10,15}:
            raise ValueError("incomplete lag grid")
        if max(x[0] for x in d.values())-min(x[0] for x in d.values()) > 0.000002:
            raise ValueError("inconsistent slopes")
        result.append({"outcome":key[0], "period":key[1],
                       "se_lag0":d[0][1], "se_lag15":d[15][1],
                       "se_ratio_lag15_to_lag0":round(d[15][1]/d[0][1],6),
                       "zero_excluded_all_lags":all(x[2] for x in d.values()),
                       "zero_excluded_any_lag":any(x[2] for x in d.values())})
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase136_csv")
    args = parser.parse_args()
    with open(args.phase136_csv, newline="", encoding="utf-8") as f:
        print(json.dumps(audit(list(csv.DictReader(f))), indent=2))
