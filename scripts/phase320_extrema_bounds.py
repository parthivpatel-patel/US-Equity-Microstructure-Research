"""Extrema-informed conservative bounds on placebo right-tail counts."""
from decimal import Decimal

def bounds(d, n, lower, absolute, minimum, maximum):
    d, minimum, maximum = map(lambda v: Decimal(str(v)), (d, minimum, maximum))
    if not all(v.is_finite() for v in (d, minimum, maximum)) or d == 0:
        raise ValueError("nonfinite or zero contrast")
    if any(type(v) is not int for v in (n, lower, absolute)) or n < 1 or not (0 <= lower <= n and 0 <= absolute <= n):
        raise ValueError("invalid counts")
    if minimum > maximum:
        raise ValueError("reversed extrema")
    if d > 0:
        # A = N + R, N = count(x <= -d), R = count(x >= d).
        # N <= L; the observed negative extreme establishes N >= 1.
        lo = max(0, absolute - lower, int(maximum >= d))
        hi = min(absolute - int(minimum <= -d), n)
    else:
        # R = n - L + count(x == d); strict minimum below d
        # establishes at least one non-tied lower-tail observation.
        if absolute < lower:
            raise ValueError("negative contrast requires A >= L")
        lo = n - lower
        hi = n - int(minimum < d)
        if maximum < d:
            hi = 0
    if lo > hi:
        raise ValueError("inconsistent summary counts/extrema")
    return lo, hi
