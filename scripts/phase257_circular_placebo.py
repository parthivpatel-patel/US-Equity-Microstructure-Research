"""Circular-shift reference diagnostic for ordered daily matched contrasts.

Not a generally valid randomization test: stationarity and shift-exchangeability
of the null series are strong assumptions. Do not interpret as causal inference.
"""
from math import isfinite


def circular_shift_reference(contrasts, pre, post):
    """Compare a fixed pre/post cut with all cyclic rotations of the same series.

    The entire vector is rotated, preserving adjacency except at the circular
    seam. Each rotation uses exactly the same fixed pre/post positions.
    """
    x = tuple(contrasts)
    n = len(x)
    if not isinstance(pre, int) or isinstance(pre, bool) or not isinstance(post, int) or isinstance(post, bool):
        raise ValueError('window sizes must be integers')
    if pre < 1 or post < 1 or pre + post != n or n < 3:
        raise ValueError('require nonempty windows covering at least three dates')
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v) for v in x):
        raise ValueError('finite numeric contrasts required')
    def stat(z):
        return sum(z[pre:]) / post - sum(z[:pre]) / pre
    observed = stat(x)
    references = [stat(x[k:] + x[:k]) for k in range(n)]
    extreme = sum(abs(v) >= abs(observed) - 1e-12 for v in references)
    return {'n_dates': n, 'pre_dates': pre, 'post_dates': post,
            'observed_post_minus_pre': observed, 'reference_statistics': references,
            'tail_fraction': extreme/n, 'rotations': n,
            'assumption': 'null distribution invariant to cyclic rotation; fixed cut and roster'}
