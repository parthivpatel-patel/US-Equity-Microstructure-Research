"""Exact support probabilities for Phase 462 moving-block placebo resampling.

No market data, source authentication, or inferential validity is implied.
"""
from datetime import date
from itertools import product


def enumerate_support(sessions, boundaries, block_length, *, max_paths=1000000):
    if not sessions or not boundaries or type(block_length) is not int:
        raise ValueError('invalid inputs')
    days = [date.fromisoformat(x) for x in sessions]
    cuts = [date.fromisoformat(x) for x in boundaries]
    n = len(days)
    if len(set(days)) != n or days != sorted(days):
        raise ValueError('sessions not strictly ordered')
    if len(set(cuts)) != len(cuts) or any(not(days[0] < c <= days[-1]) for c in cuts):
        raise ValueError('cutoffs outside support or repeated')
    if not 1 <= block_length <= n:
        raise ValueError('invalid block length')
    blocks = (n + block_length - 1) // block_length
    starts = n - block_length + 1
    paths = starts ** blocks
    if paths > max_paths:
        raise ValueError('exact enumeration exceeds max_paths')
    eligible = [0] * len(cuts)
    joint = 0
    for choices in product(range(starts), repeat=blocks):
        indices = tuple(j for start in choices for j in range(start, start + block_length))[:n]
        flags = [any(days[j] < cut for j in indices) and any(days[j] >= cut for j in indices) for cut in cuts]
        eligible = [v + int(ok) for v, ok in zip(eligible, flags)]
        joint += int(all(flags))
    return {'total_paths': paths, 'eligible_per_cutoff': dict(zip(boundaries, eligible)),
            'eligible_joint': joint, 'fraction_per_cutoff': dict(zip(boundaries, [v / paths for v in eligible])),
            'fraction_joint': joint / paths, 'block_length': block_length,
            'note': 'Exact support enumeration only; not a valid hypothesis test.'}
