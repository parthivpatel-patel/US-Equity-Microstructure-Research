"""Audit observed trading dates against an explicitly supplied, authenticated session calendar.

No exchange calendar is inferred from weekdays or holidays. This is a data-quality gate,
not an estimator, significance test, or claim about SEC observations.
"""
from collections import Counter
from datetime import date
from math import isfinite


def _iso(value):
    if not isinstance(value, str):
        raise ValueError('date must be a string')
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('invalid date') from exc
    if parsed.isoformat() != value:
        raise ValueError('noncanonical date')
    return value


def audit_calendar_support(rows, sessions):
    """rows: (group, date, contrast) tuples; sessions: verified chronological dates.

    Reports gaps and adjacency by *calendar position*, not observed-row position.
    """
    sessions = [_iso(s) for s in sessions]
    if len(sessions) < 2 or sessions != sorted(set(sessions)):
        raise ValueError('sessions must be unique, increasing and contain >=2 dates')
    index = {d: i for i, d in enumerate(sessions)}
    seen = set()
    groups = set()
    observed = set()
    group_dates = Counter()
    for row in rows:
        if len(row) != 3:
            raise ValueError('expected group, date, contrast')
        group, day, contrast = row
        if not isinstance(group, str) or not group.strip():
            raise ValueError('invalid group')
        day = _iso(day)
        if day not in index:
            raise ValueError('observation outside supplied calendar')
        if isinstance(contrast, bool) or not isinstance(contrast, (int, float)) or not isfinite(contrast):
            raise ValueError('invalid contrast')
        if (group, day) in seen:
            raise ValueError('duplicate group/date')
        seen.add((group, day))
        groups.add(group)
        observed.add(day)
        group_dates[group] += 1
    if not seen:
        raise ValueError('empty observations')
    ordered = sorted(observed)
    true_adjacent = sum(index[b] - index[a] == 1 for a, b in zip(ordered, ordered[1:]))
    skipped_pairs = [(a, b, index[b] - index[a] - 1) for a, b in zip(ordered, ordered[1:]) if index[b] - index[a] > 1]
    return {
        'calendar_sessions': len(sessions), 'observed_sessions': len(observed),
        'missing_sessions': [d for d in sessions if d not in observed],
        'groups': len(groups), 'observations': len(seen),
        'observed_neighbor_pairs': max(0, len(ordered)-1),
        'true_calendar_adjacent_pairs': true_adjacent,
        'gap_spanning_pairs': skipped_pairs,
        'group_observation_counts': dict(sorted(group_dates.items())),
        'status': 'CALENDAR_SUPPORT_ONLY_NO_EMPIRICAL_INFERENCE',
    }
