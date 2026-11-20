"""Descriptive audit of one-sided eligible units excluded by two-sided support gates."""
from collections import defaultdict
from datetime import date

def audit_exclusions(eligibility, observations, cutoff):
    if not isinstance(cutoff, str):
        raise ValueError('invalid cutoff')
    try:
        boundary = date.fromisoformat(cutoff)
    except ValueError as exc:
        raise ValueError('invalid cutoff') from exc
    if boundary.isoformat() != cutoff:
        raise ValueError('noncanonical cutoff')
    def canonical(rows):
        out = set()
        for row in rows:
            if not isinstance(row, (tuple, list)) or len(row) != 3 or not all(isinstance(x, str) and x.strip() for x in row):
                raise ValueError('invalid key')
            try:
                d = date.fromisoformat(row[2])
            except ValueError as exc:
                raise ValueError('invalid date') from exc
            if d.isoformat() != row[2]:
                raise ValueError('noncanonical date')
            key = tuple(row)
            if key in out:
                raise ValueError('duplicate key')
            out.add(key)
        return out
    eligible = canonical(eligibility)
    observed = canonical(observations)
    if not eligible or observed - eligible:
        raise ValueError('empty eligibility or out-of-universe observation')
    units = defaultdict(set)
    seen = defaultdict(set)
    for sec, ex, day in eligible:
        units[(sec, ex)].add(day)
    for sec, ex, day in observed:
        seen[(sec, ex)].add(day)
    result = {}
    for ex in sorted({u[1] for u in units}):
        ex_units = [u for u in units if u[1] == ex]
        two = [u for u in ex_units if any(d < cutoff for d in units[u]) and any(d >= cutoff for d in units[u])]
        one = [u for u in ex_units if u not in two]
        result[ex] = {
            'all_eligible_units': len(ex_units),
            'two_sided_units': len(two),
            'excluded_one_sided_units': len(one),
            'excluded_one_sided_missing_observations': sum(len(units[u] - seen[u]) for u in one),
            'two_sided_missing_observations': sum(len(units[u] - seen[u]) for u in two),
            'all_eligible_observation_coverage': f'{len(observed & {k for k in eligible if k[1] == ex})}/{sum(len(units[u]) for u in ex_units)}',
        }
    return result
