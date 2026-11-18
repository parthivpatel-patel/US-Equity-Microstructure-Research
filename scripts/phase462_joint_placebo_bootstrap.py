"""Joint placebo uncertainty on a complete paired group-by-session panel.

Conditional diagnostic only. Does not authenticate source or treatment, and does
not identify reform effects. Common date blocks and matched-group draws are
shared across all placebo cutoffs to retain their dependence.
"""
from datetime import date
from math import isfinite
from random import Random


def joint_placebo_bootstrap(gaps, sessions, boundaries, *, block_length=3,
                            repetitions=999, seed=0):
    """Return observed placebo contrasts and percentile intervals.

    gaps maps (exchange, matched_group) to {ISO session: paired treated-control gap}.
    sessions is an externally supplied, ordered *complete* trading-session list.
    Resample groups and contiguous session blocks jointly, preserving the same
    resampled session sequence for every group and cutoff. Reject incomplete panels.
    """
    if not gaps or not sessions or not boundaries:
        raise ValueError('empty panel, sessions, or cutoffs')
    if type(block_length) is not int or block_length < 1 or block_length > len(sessions):
        raise ValueError('invalid block length')
    if type(repetitions) is not int or repetitions < 2 or type(seed) is not int:
        raise ValueError('invalid bootstrap configuration')
    days = [date.fromisoformat(s) for s in sessions]
    cuts = [date.fromisoformat(s) for s in boundaries]
    if len(set(days)) != len(days) or days != sorted(days):
        raise ValueError('sessions must be unique and ordered')
    if len(set(cuts)) != len(cuts) or any(not(days[0] < c <= days[-1]) for c in cuts):
        raise ValueError('cutoffs must fall within session support')
    groups = sorted(gaps)
    matrix = []
    for group in groups:
        if not isinstance(group, tuple) or len(group) != 2 or not all(isinstance(x,str) and x for x in group):
            raise ValueError('invalid group key')
        row = gaps[group]
        if set(row) != set(sessions):
            raise ValueError('incomplete or extra group-session observations')
        vals = [row[s] for s in sessions]
        if any(type(v) not in (int, float) or not isfinite(v) for v in vals):
            raise ValueError('nonfinite or invalid gap')
        matrix.append(vals)
    n = len(days)
    rng = Random(seed)

    def estimate(group_ids, indices, cut):
        before = [j for j in indices if days[j] < cut]
        after = [j for j in indices if days[j] >= cut]
        if not before or not after:
            return None
        return sum((sum(matrix[g][j] for j in after)/len(after) -
                    sum(matrix[g][j] for j in before)/len(before))
                   for g in group_ids)/len(group_ids)

    observed = [estimate(range(len(groups)), range(n), c) for c in cuts]
    draws = [[] for _ in cuts]
    complete = 0
    for _ in range(repetitions):
        selected_groups = [rng.randrange(len(groups)) for _ in groups]
        sampled = []
        while len(sampled) < n:
            start = rng.randrange(n - block_length + 1)
            sampled.extend(range(start, start + block_length))
        sampled = sampled[:n]
        vals = [estimate(selected_groups, sampled, c) for c in cuts]
        if all(v is not None for v in vals):
            complete += 1
            for bucket, value in zip(draws, vals):
                bucket.append(value)

    def percentile(values, p):
        values = sorted(values)
        position = p * (len(values) - 1)
        low = int(position)
        fraction = position - low
        return values[low] * (1-fraction) + values[min(low+1,len(values)-1)] * fraction

    out = []
    for cut, point, samples in zip(boundaries, observed, draws):
        out.append({'cutoff': cut, 'observed': point,
                    'percentile_95': [percentile(samples, .025), percentile(samples, .975)] if samples else None})
    return {'placebos': out, 'complete_draws': complete,
            'requested_draws': repetitions, 'groups': len(groups), 'sessions': n,
            'block_length': block_length, 'seed': seed,
            'source_authenticated': False, 'treatment_authenticated': False,
            'calendar_authenticated': False,
            'note': 'Exploratory joint group/session moving-block bootstrap; percentile intervals are not causal confidence intervals.'}
