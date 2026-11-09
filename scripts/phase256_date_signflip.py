"""Exact date-block sign-flip diagnostic for precomputed matched daily contrasts.

Assumptions: under the sharp null, entire date-level contrast vectors are jointly
sign symmetric. This is not automatically justified by common-date adjustment;
serial dependence and overlapping placebo windows may invalidate the test.
"""
from itertools import product
from math import isfinite


def exact_signflip(daily_contrasts, max_dates=18):
    """Return two-sided exact sign-flip p-value for mean daily contrast.

    Input: one finite numeric matched treated-minus-control contrast per date,
    ordered by date, after any pre-specified exchange/security aggregation.
    """
    values = tuple(daily_contrasts)
    if not 1 <= len(values) <= max_dates:
        raise ValueError('invalid date count')
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v) for v in values):
        raise ValueError('contrasts must be finite numbers')
    observed = abs(sum(values))
    exceed = sum(abs(sum(s*v for s, v in zip(signs, values))) >= observed - 1e-12
                 for signs in product((-1, 1), repeat=len(values)))
    return {'n_dates': len(values), 'mean_contrast': sum(values)/len(values),
            'p_two_sided': exceed/(2**len(values)), 'permutations': 2**len(values),
            'assumption': 'joint date-block sign symmetry under sharp null'}
