"""Fail-closed, overflow-resistant weighted mean for finite positive weights."""
from math import fsum, isfinite

def safe_weighted_mean(values, weights):
    values, weights = list(values), list(weights)
    if not values or len(values) != len(weights):
        raise ValueError('nonempty equal-length inputs required')
    if any(type(v) not in (int, float) or not isfinite(v) for v in values):
        raise ValueError('finite numeric values required')
    if any(type(w) not in (int, float) or not isfinite(w) or w <= 0 for w in weights):
        raise ValueError('finite strictly positive weights required')
    scale = max(abs(v) for v in values)
    if scale == 0:
        return 0.0
    max_weight = max(weights)
    normalized_weights = [w / max_weight for w in weights]
    denominator = fsum(normalized_weights)
    if not isfinite(denominator) or denominator <= 0:
        raise ValueError('invalid normalized weight sum')
    result = scale * (fsum((v / scale) * w for v, w in zip(values, normalized_weights)) / denominator)
    if not isfinite(result):
        raise ValueError('nonfinite weighted result')
    return result
