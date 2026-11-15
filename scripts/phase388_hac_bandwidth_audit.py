"""Exact Bartlett HAC bandwidth sensitivity for balanced matched-pair date gaps.

Methodology diagnostic only. No empirical observations, p-values, or causal claim.
"""
from datetime import date
from fractions import Fraction

def audit_bandwidths(rows, bandwidths):
    rows = tuple(rows)
    if not rows:
        raise ValueError("empty panel")
    cells, pairs, dates = {}, set(), set()
    for pair, day, gap in rows:
        if not isinstance(pair, str) or not pair or not isinstance(day, str):
            raise ValueError("invalid identifiers")
        try:
            if date.fromisoformat(day).isoformat() != day:
                raise ValueError("noncanonical date")
        except ValueError as exc:
            raise ValueError("invalid date") from exc
        if type(gap) not in (int, Fraction):
            raise ValueError("nonexact gap")
        if (pair, day) in cells:
            raise ValueError("duplicate pair/date")
        cells[pair, day] = Fraction(gap)
        pairs.add(pair)
        dates.add(day)
    t = len(dates)
    if len(pairs) < 2 or t < 3 or len(cells) != len(pairs) * t:
        raise ValueError("balanced >=2 pair, >=3 date panel required")
    bandwidths = tuple(bandwidths)
    if not bandwidths or len(set(bandwidths)) != len(bandwidths) or any(type(b) is not int or b < 0 or b >= t for b in bandwidths):
        raise ValueError("distinct integer bandwidths in [0,T) required")
    means = [sum((cells[p, d] for p in sorted(pairs)), Fraction()) / len(pairs) for d in sorted(dates)]
    mean = sum(means, Fraction()) / t
    centered = [v - mean for v in means]
    autocov = [sum((centered[i] * centered[i-k] for i in range(k,t)), Fraction()) / t for k in range(max(bandwidths)+1)]
    results = []
    for b in bandwidths:
        lrv = autocov[0] + 2 * sum((Fraction(b+1-k,b+1)*autocov[k] for k in range(1,b+1)), Fraction())
        variance = lrv / t
        results.append({"bandwidth":b, "long_run_variance":lrv, "variance_of_mean":variance,
                        "zero_variance_warning":variance == 0, "n_dates":t})
    return {"mean":mean, "n_pairs":len(pairs), "n_dates":t,
            "results":tuple(results), "bandwidth_sensitive":len({r["variance_of_mean"] for r in results}) > 1,
            "empirical_data_authenticated":False, "causal_identification_established":False}
