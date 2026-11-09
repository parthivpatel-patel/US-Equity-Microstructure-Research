"""Finite-sample HAC audit for a fixed-roster daily matched contrast series.

Synthetic tests only. Not an identification strategy or historical estimate.
"""
import math


def hac_mean_se(values, lag):
    """Bartlett HAC standard error of the sample mean, no finite-sample correction."""
    x = [float(v) for v in values]
    n = len(x)
    if n < 3 or any(not math.isfinite(v) for v in x):
        raise ValueError('need >=3 finite observations')
    if not isinstance(lag, int) or isinstance(lag, bool) or not 0 <= lag < n:
        raise ValueError('lag must be an integer in [0,n)')
    mu = sum(x) / n
    u = [v - mu for v in x]
    long_run = sum(v*v for v in u)/n
    for k in range(1, lag+1):
        gamma = sum(u[t]*u[t-k] for t in range(k,n))/n
        long_run += 2*(1-k/(lag+1))*gamma
    return math.sqrt(max(0.,long_run)/n)


def period_difference_hac(daily, pre_dates, post_dates, lag):
    """Separate-period HAC variance; assumes zero cross-period covariance.

    NOT valid automatically for adjacent pre/post periods. This is a sensitivity
    diagnostic only, and reports the unmodeled covariance explicitly.
    """
    if set(pre_dates) & set(post_dates):
        raise ValueError('overlapping periods')
    if len(set(pre_dates)) != len(pre_dates) or len(set(post_dates)) != len(post_dates):
        raise ValueError('duplicate dates')
    if not pre_dates or not post_dates or set(daily) != set(pre_dates) | set(post_dates):
        raise ValueError('date coverage mismatch')
    pre = [daily[d] for d in sorted(pre_dates)]
    post = [daily[d] for d in sorted(post_dates)]
    estimate = sum(post)/len(post) - sum(pre)/len(pre)
    se_pre = hac_mean_se(pre, lag)
    se_post = hac_mean_se(post, lag)
    return {'estimate': estimate, 'se_zero_cross_period_covariance': math.hypot(se_pre,se_post),
            'lag': lag, 'cross_period_covariance_modeled': False,
            'historical_inference_authorized': False}
