"""Exact overlap correlation of equal-weight pre/post event-window contrasts.

Constructed white-noise benchmark, not SEC empirical inference.
"""
from fractions import Fraction

def weights(half_window=5):
    if not isinstance(half_window, int) or isinstance(half_window, bool) or half_window < 1:
        raise ValueError('half_window must be a positive integer')
    return (-1,) * half_window + (1,) * half_window

def correlation(lag, half_window=5):
    """Correlation under independent homoskedastic daily innovations."""
    if not isinstance(lag, int) or isinstance(lag, bool) or lag < 0:
        raise ValueError('lag must be a nonnegative integer')
    w = weights(half_window)
    dot = sum(w[i] * w[i - lag] for i in range(lag, len(w)))
    return Fraction(dot, sum(v*v for v in w))

def report(half_window=5):
    weights(half_window)
    return {str(k): str(correlation(k, half_window)) for k in range(2*half_window+1)}

if __name__ == '__main__':
    import json
    print(json.dumps(report(), indent=2))
