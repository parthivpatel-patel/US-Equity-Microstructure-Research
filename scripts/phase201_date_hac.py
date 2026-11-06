"""Date-level HAC diagnostic for prevalidated matched-group contrasts; descriptive only."""
from datetime import date
from math import isfinite, sqrt

def date_hac(records, lag):
    """Newey-West Bartlett SE for mean; lag measured in observed sessions."""
    if type(lag) is not int or lag < 0:
        raise ValueError("lag must be a nonnegative integer")
    records = list(records)
    if len(records) < 2 or lag >= len(records):
        raise ValueError("need at least two dates and lag < number of dates")
    dates, values = [], []
    for r in records:
        d = date.fromisoformat(r["date"])
        x = float(r["contrast"])
        if not isfinite(x):
            raise ValueError("nonfinite contrast")
        dates.append(d)
        values.append(x)
    if len(set(dates)) != len(dates) or dates != sorted(dates):
        raise ValueError("dates must be unique and increasing")
    n = len(values)
    mean = sum(values) / n
    residual = [x - mean for x in values]
    long_run = sum(x*x for x in residual) / n
    for h in range(1, lag + 1):
        gamma = sum(residual[t] * residual[t-h] for t in range(h, n)) / n
        long_run += 2 * (1 - h / (lag + 1)) * gamma
    variance = max(0.0, long_run / n)
    return {"n_dates": n, "lag": lag, "mean": mean, "hac_se": sqrt(variance),
            "warning": "Descriptive date-level uncertainty only; no causal inference, authentication, or valid small-sample guarantee."}
