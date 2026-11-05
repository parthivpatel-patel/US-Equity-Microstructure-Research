"""Audit published window-sensitivity summary; does not re-estimate SEC observations."""
import csv
import json
import math
import sys

REQUIRED = {"outcome","window_days","november_pp","october6_pp","pre_placebo_count","pre_placebo_at_least_as_negative","pre_placebo_at_least_as_extreme_abs","nov_minus_oct_pp"}

def audit(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("Missing columns")
        rows = list(reader)
    if not rows:
        raise ValueError("Empty table")
    seen, grouped = set(), {}
    for r in rows:
        outcome, window = r["outcome"].strip(), int(r["window_days"])
        if outcome not in ("count","volume") or window <= 0 or (outcome,window) in seen:
            raise ValueError("Invalid or duplicate outcome/window")
        seen.add((outcome,window))
        n, negative, extreme = (int(r[k]) for k in ("pre_placebo_count","pre_placebo_at_least_as_negative","pre_placebo_at_least_as_extreme_abs"))
        if n <= 0 or not (0 <= negative <= n and 0 <= extreme <= n):
            raise ValueError("Invalid placebo counts")
        nov, octo, delta = (float(r[k]) for k in ("november_pp","october6_pp","nov_minus_oct_pp"))
        if not all(map(math.isfinite,(nov,octo,delta))) or abs(nov-octo-delta)>0.000002:
            raise ValueError("Inconsistent estimate")
        grouped.setdefault(outcome,[]).append({"window_days":window,"difference_pp":delta,"absolute_placebo_fraction":extreme/n,"negative_placebo_fraction":negative/n,"placebo_count":n})
    return {o:{"windows":sorted(v,key=lambda x:x["window_days"]),"positive_windows":sum(x["difference_pp"]>0 for x in v),"negative_windows":sum(x["difference_pp"]<0 for x in v),"min_difference_pp":min(x["difference_pp"] for x in v),"max_difference_pp":max(x["difference_pp"] for x in v)} for o,v in sorted(grouped.items())}

if __name__ == "__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python scripts/phase178_window_audit.py CSV_PATH")
    print(json.dumps(audit(sys.argv[1]),indent=2,sort_keys=True))
