"""Descriptive fixed-date placebo and HAC lag sensitivity; no causal authorization."""
import datetime as dt
import math
try:
    from scripts.phase269_full_series_hac import full_series_hac
except ModuleNotFoundError:
    from phase269_full_series_hac import full_series_hac

def placebo_grid(series, cutoffs, lags, min_period=5):
    dates = [d for d, _ in series]
    if not dates or any(type(d) is not dt.date for d in dates) or dates != sorted(set(dates)):
        raise ValueError("dates must be strictly increasing unique date objects")
    if any(not math.isfinite(float(v)) for _, v in series):
        raise ValueError("nonfinite observations")
    if type(min_period) is not int or min_period < 2:
        raise ValueError("min_period must be integer >= 2")
    if not cutoffs or any(type(d) is not dt.date for d in cutoffs) or list(cutoffs) != sorted(set(cutoffs)):
        raise ValueError("cutoffs must be unique, increasing date objects")
    if not lags or any(type(l) is not int or l < 0 for l in lags) or list(lags) != sorted(set(lags)):
        raise ValueError("lags must be unique, increasing nonnegative integers")
    output = []
    for cutoff in cutoffs:
        pre = sum(d < cutoff for d in dates)
        post = len(dates) - pre
        if min(pre, post) < min_period:
            raise ValueError(f"cutoff {cutoff} has insufficient pre/post dates")
        for lag in lags:
            result = full_series_hac(series, cutoff, lag)
            output.append(dict(cutoff=cutoff.isoformat(), lag=lag,
                               difference=result["difference"], hac_se=result["hac_se"],
                               cross_cutoff_component=result["cross_cutoff_component"],
                               pre_dates=pre, post_dates=post))
    return output
