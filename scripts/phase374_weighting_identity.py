"""Exact aggregation identities for hidden execution fractions; no SEC data bundled."""
from decimal import Decimal


def summarize(rows):
    """Rows: (hidden_count, total_count, hidden_shares, total_shares).

    Returns pooled ratios and equal-row averages. Zero denominators make
    equal-row means undefined and are rejected, rather than silently dropped.
    """
    rows = list(rows)
    if not rows:
        raise ValueError('empty rows')
    parsed = []
    for row in rows:
        if len(row) != 4:
            raise ValueError('expected four measures')
        vals = tuple(Decimal(str(x)) for x in row)
        if any(not v.is_finite() or v != v.to_integral_value() or v < 0 for v in vals):
            raise ValueError('counts and shares must be finite nonnegative integers')
        hc, tc, hs, ts = vals
        if not (0 <= hc <= tc and 0 <= hs <= ts and tc > 0 and ts > 0):
            raise ValueError('invalid numerator or denominator')
        parsed.append(vals)
    hc, tc, hs, ts = (sum((r[i] for r in parsed), Decimal(0)) for i in range(4))
    n = Decimal(len(parsed))
    return {
        'rows': len(parsed),
        'pooled_count': hc / tc,
        'pooled_shares': hs / ts,
        'equal_row_count': sum((r[0] / r[1] for r in parsed), Decimal(0)) / n,
        'equal_row_shares': sum((r[2] / r[3] for r in parsed), Decimal(0)) / n,
    }
