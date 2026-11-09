"""Full-series HAC contrast with cross-cutoff lag covariance. Descriptive only."""
import csv
import datetime as dt
import math
from collections import defaultdict

def daily_contrasts(rows):
    grouped = defaultdict(dict)
    for r in rows:
        d = dt.date.fromisoformat(r["date"])
        p = str(r["pair"])
        a, b = float(r["treated"]), float(r["control"])
        if not math.isfinite(a) or not math.isfinite(b):
            raise ValueError("nonfinite outcome")
        if p in grouped[d]:
            raise ValueError("duplicate date/pair")
        grouped[d][p] = a-b
    if not grouped:
        raise ValueError("empty panel")
    roster = set(next(iter(grouped.values())))
    if not roster or any(set(v) != roster for v in grouped.values()):
        raise ValueError("changing or incomplete observed roster")
    return [(d, sum(v.values())/len(v)) for d,v in sorted(grouped.items())]

def full_series_hac(series, cutoff, lag):
    n = len(series)
    if type(lag) is not int or not 0 <= lag < n or n < 4:
        raise ValueError("invalid lag or sample length")
    flags = [d >= cutoff for d,_ in series]
    n1 = sum(flags)
    n0 = n-n1
    if min(n0,n1) < 2:
        raise ValueError("need two dates in each period")
    values = [float(v) for _,v in series]
    if any(not math.isfinite(v) for v in values):
        raise ValueError("nonfinite contrast")
    pre = sum(v for v,p in zip(values,flags) if not p)/n0
    post = sum(v for v,p in zip(values,flags) if p)/n1
    z = [((1/n1 if p else -1/n0)*(v-(post if p else pre)))
         for v,p in zip(values,flags)]
    variance = sum(x*x for x in z)
    cross_cutoff = 0.0
    for k in range(1,lag+1):
        weight = 2*(1-k/(lag+1))
        for t in range(k,n):
            term = weight*z[t]*z[t-k]
            variance += term
            if flags[t] != flags[t-k]:
                cross_cutoff += term
    if variance < -1e-12:
        raise ArithmeticError("negative variance")
    return dict(difference=post-pre, pre_mean=pre, post_mean=post,
                hac_se=math.sqrt(max(0,variance)), cross_cutoff_component=cross_cutoff,
                pre_dates=n0, post_dates=n1, lag=lag)

if __name__ == "__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--csv",required=True)
    parser.add_argument("--cutoff",default="2025-11-03")
    parser.add_argument("--lag",type=int,default=3)
    args=parser.parse_args()
    with open(args.csv,newline="",encoding="utf-8") as f:
        series=daily_contrasts(csv.DictReader(f))
    print(full_series_hac(series,dt.date.fromisoformat(args.cutoff),args.lag))
