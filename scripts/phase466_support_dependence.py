"""Exact joint eligibility dependence of moving-block placebo bootstrap paths.

Synthetic/design-only diagnostic. Does not estimate SEC outcomes or p-values.
"""
from datetime import date
from itertools import product
from math import ceil


def support_dependence(sessions, cutoffs, block_length, max_paths=1_000_000):
    days = [date.fromisoformat(s) for s in sessions]
    cuts = [date.fromisoformat(s) for s in cutoffs]
    n = len(days)
    if n < 2 or days != sorted(set(days)):
        raise ValueError('sessions must be unique, increasing and at least two')
    if not cuts or len(cuts) != len(set(cuts)) or any(not days[0] < c <= days[-1] for c in cuts):
        raise ValueError('cutoffs must be distinct and inside observable support')
    if type(block_length) is not int or not 1 <= block_length <= n:
        raise ValueError('invalid block length')
    starts = n - block_length + 1
    blocks = ceil(n / block_length)
    total = starts ** blocks
    if total > max_paths:
        raise ValueError('path count exceeds limit')
    k = len(cuts)
    count = [0] * k
    pairs = [[0] * k for _ in range(k)]
    for choice in product(range(starts), repeat=blocks):
        ix = [j for s in choice for j in range(s, s + block_length)][:n]
        lo = min(days[j] for j in ix)
        hi = max(days[j] for j in ix)
        ok = [lo < c <= hi for c in cuts]
        for a in range(k):
            count[a] += ok[a]
            for b in range(k):
                pairs[a][b] += ok[a] and ok[b]
    p = [x / total for x in count]
    joint = [[v / total for v in row] for row in pairs]
    covariance = [[joint[a][b] - p[a] * p[b] for b in range(k)] for a in range(k)]
    conditional = [[joint[a][b] / p[b] if p[b] else None for b in range(k)] for a in range(k)]
    return {'total_paths': total, 'cutoffs': list(cutoffs), 'eligible_counts': count,
            'eligible_probabilities': p, 'joint_probabilities': joint,
            'eligibility_covariance': covariance,
            'conditional_probability_a_given_b': conditional,
            'note': 'Exact design-level eligibility dependence; not bootstrap-estimate covariance or calibrated inference.'}
