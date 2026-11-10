"""Independent deterministic audit of Phase 289's percentile-bootstrap index convention."""
from math import floor

def quantile_linear(sorted_draws, p):
    if len(sorted_draws) < 2 or not 0 <= p <= 1:
        raise ValueError('invalid draws/probability')
    h = (len(sorted_draws)-1)*p
    lo = floor(h)
    return sorted_draws[lo] + (h-lo)*(sorted_draws[min(lo+1,len(sorted_draws)-1)]-sorted_draws[lo])

def audit_indices(repetitions):
    if type(repetitions) is not int or repetitions < 2:
        raise ValueError('invalid repetitions')
    return {'repetitions': repetitions,
            'lower_index_phase289': int(.025*(repetitions-1)),
            'upper_index_phase289': int(.975*(repetitions-1)),
            'lower_fractional_rank': .025*(repetitions-1),
            'upper_fractional_rank': .975*(repetitions-1)}
