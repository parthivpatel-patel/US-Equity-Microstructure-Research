"""Date-by-exchange treatment/control coverage; descriptive, not causal inference."""
from collections import defaultdict
from datetime import date


def date_coverage(eligibility, observations, treatment, cutoff):
    """Report all eligible exchange/date cells, including entirely missing groups."""
    if not isinstance(cutoff, str):
        raise ValueError('invalid cutoff')
    try:
        parsed = date.fromisoformat(cutoff)
    except ValueError as exc:
        raise ValueError('invalid cutoff') from exc
    if parsed.isoformat() != cutoff:
        raise ValueError('noncanonical cutoff')

    def checked(rows):
        result = set()
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
            if key in result:
                raise ValueError('duplicate key')
            result.add(key)
        return result

    eligible, observed = checked(eligibility), checked(observations)
    if not eligible or observed - eligible:
        raise ValueError('empty eligibility or out-of-universe observation')
    if not isinstance(treatment, dict):
        raise ValueError('invalid treatment map')
    counts = defaultdict(lambda: {0: [0, 0], 1: [0, 0]})
    for sec, ex, day in eligible:
        label = treatment.get(sec)
        if type(label) not in (int, bool) or label not in (0, 1):
            raise ValueError('missing or invalid treatment label')
        cell = counts[(ex, day)][int(label)]
        cell[0] += 1
        cell[1] += int((sec, ex, day) in observed)
    result = []
    for (ex, day), groups in sorted(counts.items()):
        t, c = groups[1], groups[0]
        result.append({
            'exchange': ex, 'date': day, 'period': 'pre' if day < cutoff else 'post',
            'treated_eligible': t[0], 'treated_observed': t[1],
            'control_eligible': c[0], 'control_observed': c[1],
            'treated_coverage': t[1] / t[0] if t[0] else None,
            'control_coverage': c[1] / c[0] if c[0] else None,
            'coverage_gap_treated_minus_control': t[1] / t[0] - c[1] / c[0] if t[0] and c[0] else None,
            'both_groups_eligible': bool(t[0] and c[0]),
            'both_groups_observed': bool(t[1] and c[1]),
        })
    return result
