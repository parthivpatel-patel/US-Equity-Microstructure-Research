"""Fail-closed descriptive HAC inference gate for Phase 283 output.

This gate cannot authenticate source data or authorize causal inference.
"""
from math import isfinite


def assess_hac(result, *, min_dates=20, max_lag_fraction=0.25, se_floor=1e-12):
    """Return admissibility and reasons, never a p-value or causal claim."""
    if not isinstance(result, dict):
        raise ValueError('result must be a dictionary')
    if result.get('source_authenticated') is not False or result.get('causal_inference_authorized') is not False:
        raise ValueError('missing or contradictory provenance flags')
    n, lag = result.get('n_dates'), result.get('lag')
    mean, se = result.get('mean'), result.get('hac_standard_error')
    if type(min_dates) is not int or min_dates < 2:
        raise ValueError('invalid min_dates')
    if type(max_lag_fraction) not in (int, float) or not isfinite(max_lag_fraction) or not 0 <= max_lag_fraction < 1:
        raise ValueError('invalid max_lag_fraction')
    if type(se_floor) not in (int, float) or not isfinite(se_floor) or se_floor <= 0:
        raise ValueError('invalid se_floor')
    if type(n) is not int or n < 1 or type(lag) is not int or not 0 <= lag < n:
        raise ValueError('invalid sample size or lag')
    if type(mean) not in (int, float) or type(se) not in (int, float) or not isfinite(mean) or not isfinite(se) or se < 0:
        raise ValueError('invalid estimate or standard error')
    if result.get('weighting') not in ('pair', 'exchange'):
        raise ValueError('unknown weighting')
    reasons = []
    if n < min_dates:
        reasons.append('short_common_date_sample')
    if lag > max_lag_fraction * n:
        reasons.append('large_hac_lag_relative_to_sample')
    if se <= se_floor:
        reasons.append('zero_or_near_zero_standard_error')
    return {'descriptive_inference_admissible': not reasons,
            'reasons': reasons, 'n_dates': n, 'lag': lag,
            'weighting': result['weighting'], 'source_authenticated': False,
            'causal_inference_authorized': False}
