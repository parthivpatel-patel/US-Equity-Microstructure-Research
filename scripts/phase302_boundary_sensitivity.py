"""Exact small-sample circular versus non-circular moving-block audit.

Synthetic sequences only. Enumerates all equally likely ordered block-start
sequences, not historical SEC observations or a substitute for inference.
"""
from itertools import product
from math import fsum

def exact_block_means(values, block_length, circular):
    values = tuple(float(v) for v in values)
    n = len(values)
    if n < 2 or not 1 <= block_length <= n:
        raise ValueError('invalid length')
    starts = range(n if circular else n - block_length + 1)
    blocks = [tuple(values[(s+j) % n] for j in range(block_length)) for s in starts]
    nblocks = (n + block_length - 1) // block_length
    draws = []
    for selected in product(blocks, repeat=nblocks):
        sample = [x for block in selected for x in block][:n]
        draws.append(fsum(sample) / n)
    return sorted(draws)

def exact_summary(values, block_length):
    result = {}
    for circular in (False, True):
        draws = exact_block_means(values, block_length, circular)
        result['circular' if circular else 'noncircular'] = {
            'draws': len(draws), 'min': draws[0], 'max': draws[-1],
            'mean': fsum(draws)/len(draws),
            'p025': draws[int(.025*(len(draws)-1))],
            'p975': draws[int(.975*(len(draws)-1))]}
    return result
