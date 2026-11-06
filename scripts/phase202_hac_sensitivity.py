"""Observed-session HAC lag sensitivity; descriptive only."""
from datetime import date
from math import isfinite, sqrt

def lag_sensitivity(records, lags=(0, 1, 3, 5)):
    rows = list(records)
    if len(rows) < 2:
        raise ValueError("at least two dates required")
    dates, values = [], []
    for row in rows:
        if not isinstance(row["date"], str):
            raise ValueError("date must be ISO string")
        d = date.fromisoformat(row["date"])
        if d.isoformat() != row["date"]:
            raise ValueError("date must be canonical ISO")
        x = float(row["contrast"])
        if not isfinite(x):
            raise ValueError("nonfinite contrast")
        dates.append(d)
        values.append(x)
    if dates != sorted(set(dates)):
        raise ValueError("dates must be strictly increasing and unique")
    lags = list(lags)
    if not lags or any(type(h) is not int or h < 0 or h >= len(rows) for h in lags) or len(lags) != len(set(lags)):
        raise ValueError("invalid or duplicate lag")
    n = len(values)
    mean = sum(values) / n
    u = [x - mean for x in values]
    gamma = [sum(u[t] * u[t-h] for t in range(h, n)) / n for h in range(max(lags)+1)]
    sensitivity = []
    for lag in lags:
        long_run = gamma[0] + 2 * sum((1-h/(lag+1))*gamma[h] for h in range(1,lag+1))
        sensitivity.append({"lag":lag, "hac_se":sqrt(max(0.,long_run/n)), "clipped_negative_variance":long_run < 0})
    return {"n_dates":n, "mean":mean, "first_date":dates[0].isoformat(), "last_date":dates[-1].isoformat(),
            "lag_units":"observed_sessions", "sensitivity":sensitivity,
            "warning":"Descriptive only; authentication, common support, cross-sectional dependence and causal identification not established."}
