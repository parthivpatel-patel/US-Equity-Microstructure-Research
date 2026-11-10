"""Strict float-domain admission for bootstrap helper inputs (synthetic contracts)."""
import math

def finite_float(value, *, positive=False):
    if type(value) not in (int, float):
        raise ValueError('expected finite int or float, excluding bool')
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError('numeric input outside finite float domain') from exc
    if not math.isfinite(result) or (positive and result <= 0):
        raise ValueError('numeric input must be finite and positive when required')
    return result
