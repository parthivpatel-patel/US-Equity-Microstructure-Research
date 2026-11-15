"""Exact circular-block bootstrap enumeration for a common-date matched-gap series.

Methodological diagnostic only; no inference without authenticated input and a
justified dependence horizon. Enumerates all n**ceil(n/block) block-index draws,
so intentionally limited to small panels.
"""
from fractions import Fraction
from itertools import product
from math import ceil


def enumerate_circular_block_means(values, block_length, max_draws=100000):
    """Enumerate date-level circular-block resampled means, not pair clusters."""
    values = tuple(values)
    if not values or any(type(v) not in (int, Fraction) for v in values):
        raise ValueError('nonempty integer or Fraction series required')
    if type(block_length) is not int or not 1 <= block_length <= len(values):
        raise ValueError('invalid block length')
    if type(max_draws) is not int or max_draws < 1:
        raise ValueError('invalid enumeration budget')
    n = len(values)
    blocks = ceil(n / block_length)
    draws = n ** blocks
    if draws > max_draws:
        raise ValueError('enumeration budget exceeded')
    values = tuple(Fraction(v) for v in values)
    counts = {}
    for starts in product(range(n), repeat=blocks):
        indices = [((start + offset) % n) for start in starts for offset in range(block_length)][:n]
        mean = sum((values[i] for i in indices), Fraction()) / n
        counts[mean] = counts.get(mean, 0) + 1
    assert sum(counts.values()) == draws
    return {'observed_mean': sum(values, Fraction()) / n,
            'distribution': tuple(sorted(counts.items())),
            'draws': draws, 'n_dates': n, 'block_length': block_length,
            'joint_date_resampling': True, 'pair_cluster_inference': False,
            'causal_identification_established': False}


def exact_quantile(distribution, numerator, denominator):
    """Smallest outcome whose cumulative mass reaches q, q in (0,1]."""
    if (type(numerator) is not int or type(denominator) is not int or
            denominator <= 0 or not 0 < numerator <= denominator):
        raise ValueError('invalid quantile')
    if not distribution:
        raise ValueError('empty distribution')
    total = sum(count for _, count in distribution)
    if total <= 0 or any(type(c) is not int or c <= 0 for _, c in distribution):
        raise ValueError('invalid frequency')
    if any(distribution[i][0] >= distribution[i + 1][0] for i in range(len(distribution) - 1)):
        raise ValueError('unordered support')
    cumulative = 0
    for value, count in distribution:
        cumulative += count
        if cumulative * denominator >= numerator * total:
            return value
    raise AssertionError('unreachable')
