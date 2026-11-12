"""Conservative placebo right-tail bounds; conditional tightening without ties."""
from decimal import Decimal

def right_tail_bounds(contrast, n, lower, absolute, *, no_ties=False):
    d = Decimal(str(contrast))
    if not d.is_finite() or d == 0:
        raise ValueError("contrast must be finite and nonzero")
    if any(type(x) is not int for x in (n, lower, absolute)):
        raise ValueError("counts must be integers")
    if n < 1 or not (0 <= lower <= n and 0 <= absolute <= n):
        raise ValueError("invalid counts")
    if d > 0:
        if not no_ties:
            return max(0, absolute - lower), absolute
        return max(0, absolute - lower), min(absolute, n - lower)
    if absolute < lower:
        raise ValueError("negative contrast requires absolute >= lower")
    return n - lower, n
