"""Descriptive pre-reform diagnostics; no inference or causal identification."""
from datetime import date
from math import isfinite

REFORM = "2025-11-03"

def diagnose(observations, early, late, min_dates=3):
    obs = list(observations)
    if type(min_dates) is not int or min_dates < 3 or not obs:
        raise ValueError("invalid minimum or empty observations")
    def valid_date(s):
        return type(s) is str and date.fromisoformat(s).isoformat() == s
    dates, values = [], []
    for r in obs:
        if not isinstance(r, dict) or set(r) != {"date", "contrast"}:
            raise ValueError("invalid record")
        d, v = r["date"], r["contrast"]
        if not valid_date(d) or type(v) not in (int, float) or not isfinite(v):
            raise ValueError("invalid date or contrast")
        dates.append(d)
        values.append(float(v))
    if dates != sorted(set(dates)) or dates[-1] >= REFORM:
        raise ValueError("dates must be unique, ordered, and pre-reform")
    windows = []
    for w in (early, late):
        if not isinstance(w, (tuple, list)) or len(w) != 2 or not all(valid_date(d) for d in w):
            raise ValueError("invalid window")
        a, b = w
        if a > b or b >= REFORM or a not in dates or b not in dates:
            raise ValueError("invalid window boundaries")
        i, j = dates.index(a), dates.index(b)
        if j-i+1 < min_dates:
            raise ValueError("short window")
        windows.append((i, j))
    if windows[0][1] >= windows[1][0]:
        raise ValueError("windows overlap or are reversed")
    def stats(pair):
        i, j = pair
        ys = values[i:j+1]
        n = len(ys)
        mu = sum(ys)/n
        mid = (n-1)/2
        slope = sum((k-mid)*(y-mu) for k,y in enumerate(ys))/sum((k-mid)**2 for k in range(n))
        return {"n":n,"mean":mu,"slope_per_observed_session":slope,
                "start":dates[i],"end":dates[j]}
    first, second = (stats(w) for w in windows)
    return {"early":first,"late":second,"placebo_mean_shift":second["mean"]-first["mean"],
            "calendar_authenticated":False,"source_authenticated":False,
            "treatment_authenticated":False,"causal_effect_established":False}
