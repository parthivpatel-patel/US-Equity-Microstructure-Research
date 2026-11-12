"""Logical bounds on right-tail counts from published placebo aggregates.

Combinatorial bounds only; not confidence intervals or p-values.
"""
import csv
import json
import sys
from decimal import Decimal


def bounds(contrast, n, lower, absolute):
    d = Decimal(str(contrast))
    if not d.is_finite() or d == 0 or not all(type(x) is int for x in (n, lower, absolute)):
        raise ValueError('requires finite nonzero contrast and integer counts')
    if n < 1 or not (0 <= lower <= n and 0 <= absolute <= n):
        raise ValueError('invalid counts')
    # L = number of x <= d; A = number of |x| >= |d|; R = number of x >= d.
    # For positive d, R belongs to A and negative extremes belong to L.
    # For negative d, n-L observations are strictly greater than d.
    if d > 0:
        return {'right_tail_min': max(0, absolute-lower),
                'right_tail_max': absolute,
                'note': 'ties and sign distribution prevent point identification'}
    if absolute < lower:
        raise ValueError('negative threshold implies lower tail subset of absolute tail')
    return {'right_tail_min': n-lower, 'right_tail_max': n,
            'note': 'ties and sign distribution prevent point identification'}


def audit(path):
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    out = {}
    for r in rows:
        name = r['outcome']
        if name in out:
            raise ValueError('duplicate outcome')
        out[name] = bounds(r['nov_minus_oct_pp'], int(r['pre_placebo_n']),
                           int(r['pre_placebo_at_least_as_negative']),
                           int(r['pre_placebo_at_least_as_extreme_absolute']))
    if set(out) != {'count', 'volume'}:
        raise ValueError('expected count and volume')
    return out


if __name__ == '__main__':
    print(json.dumps(audit(sys.argv[1]), indent=2))
