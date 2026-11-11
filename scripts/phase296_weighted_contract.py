"""Fail-closed, overflow-resistant weighted mean for finite positive weights."""
from math import fsum, isfinite
from scripts.phase299_numeric_admission import finite_float

def safe_weighted_mean(values, weights):
    values, weights = list(values), list(weights)
    if not values or len(values) != len(weights):
        raise ValueError('nonempty equal-length inputs required')
    values = [finite_float(v) for v in values]
    weights = [finite_float(w, positive=True) for w in weights]
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
