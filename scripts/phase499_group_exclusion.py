"""Treatment-stratified eligibility coverage audit. Descriptive only."""
from collections import defaultdict
from datetime import date

def group_exclusion_audit(eligibility, observations, treatment, cutoff):
    if not isinstance(cutoff, str):
        raise ValueError('invalid cutoff')
    try:
        boundary = date.fromisoformat(cutoff)
    except ValueError as exc:
        raise ValueError('invalid cutoff') from exc
    if boundary.isoformat() != cutoff:
        raise ValueError('noncanonical cutoff')
    def keys(rows):
        out = set()
        for row in rows:
            if not isinstance(row, (tuple, list)) or len(row) != 3 or not all(isinstance(v, str) and v.strip() for v in row):
                raise ValueError('invalid key')
            try:
                parsed = date.fromisoformat(row[2])
            except ValueError as exc:
                raise ValueError('invalid date') from exc
            if parsed.isoformat() != row[2]:
                raise ValueError('noncanonical date')
            key = tuple(row)
            if key in out:
                raise ValueError('duplicate key')
            out.add(key)
        return out
    eligible, observed = keys(eligibility), keys(observations)
    if not eligible or observed - eligible:
        raise ValueError('empty eligibility or out-of-universe observation')
    if not isinstance(treatment, dict):
        raise ValueError('invalid treatment map')
    by_unit = defaultdict(set)
    for sec, ex, day in eligible:
        if sec not in treatment or type(treatment[sec]) not in (bool, int) or treatment[sec] not in (0, 1):
            raise ValueError('missing or invalid treatment label')
        by_unit[(sec, ex)].add(day)
    buckets = defaultdict(lambda: {'eligible_units': 0, 'two_sided_units': 0, 'one_sided_units': 0,
                                   'eligible_rows': 0, 'observed_rows': 0,
                                   'two_sided_missing_rows': 0, 'one_sided_missing_rows': 0})
    for (sec, ex), days in by_unit.items():
        group = int(treatment[sec])
        b = buckets[(ex, group)]
        two = any(d < cutoff for d in days) and any(d >= cutoff for d in days)
        missing = sum((sec, ex, d) not in observed for d in days)
        b['eligible_units'] += 1
        b['two_sided_units' if two else 'one_sided_units'] += 1
        b['eligible_rows'] += len(days)
        b['observed_rows'] += len(days) - missing
        b['two_sided_missing_rows' if two else 'one_sided_missing_rows'] += missing
    return {ex: {str(group): dict(buckets[(ex, group)]) for group in (0, 1)}
            for ex in sorted({ex for ex, _ in buckets})}
