"""Exact linear-trend sensitivity of symmetric event-window contrasts.

Pure algebraic diagnostic; does not estimate historical SEC observations.
"""
from fractions import Fraction

def contrast(values, half_window):
    if isinstance(half_window, bool) or not isinstance(half_window, int) or half_window < 1:
        raise ValueError('half_window must be positive integer')
    if len(values) != 2 * half_window:
        raise ValueError('requires exactly 2*half_window observations')
    try:
        x = [Fraction(v) for v in values]
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError('values must be finite rational-compatible numbers') from exc
    return (sum(x[half_window:]) - sum(x[:half_window])) / half_window

def linear_trend_bias(slope, half_window=5):
    """Difference of post and pre means under y_t = a + slope*t."""
    if isinstance(half_window, bool) or not isinstance(half_window, int) or half_window < 1:
        raise ValueError('half_window must be positive integer')
    try:
        return Fraction(slope) * half_window
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError('slope must be finite rational-compatible') from exc

def detrended_contrast(values, half_window, prespecified_slope):
    """Subtract externally specified slope contribution; NOT a causal estimator."""
    return contrast(values, half_window) - linear_trend_bias(prespecified_slope, half_window)

if __name__ == '__main__':
    import json
    print(json.dumps({'half_window':5,'slope_per_session':'1/100','trend_only_contrast':'%s' % linear_trend_bias('1/100',5), 'units':'same as input outcome'}, indent=2))
