"""Common-date circular block bootstrap; descriptive, unauthenticated panels only."""
from math import isfinite, fsum
from random import Random

def _safe_mean(values):
    """Compute finite arithmetic means without overflowing intermediate sums."""
    values = list(values)
    if not values:
        raise ValueError("empty mean")
    scale = max(abs(v) for v in values)
    if not isfinite(scale):
        raise ValueError("nonfinite mean input")
    if scale == 0:
        return 0.0
    result = scale * (fsum(v / scale for v in values) / len(values))
    if not isfinite(result):
        raise ValueError("nonfinite mean result")
    return result

def _safe_weighted_mean(values, weights):
    """Normalize values and weights before summing."""
    scale = max(abs(v) for v in values)
    max_weight = max(weights)
    if scale == 0:
        return 0.0
    denominator = fsum(w / max_weight for w in weights)
    result = scale * (fsum((v / scale) * (w / max_weight) for v, w in zip(values, weights)) / denominator)
    if not isfinite(result):
        raise ValueError("nonfinite weighted contrast")
    return result

def bootstrap_common_dates(admitted, *, weighting="pair", block_length=3, repetitions=999, seed=20261110):
    if not isinstance(admitted, dict) or admitted.get("source_authenticated") is not False:
        raise ValueError("explicit unauthenticated provenance required")
    dates, counts = admitted.get("dates"), admitted.get("pair_counts_by_exchange")
    if not isinstance(dates, list) or not isinstance(counts, dict) or not counts:
        raise ValueError("invalid panel")
    n = len(dates)
    if n < 2 or type(block_length) is not int or not 1 <= block_length <= n:
        raise ValueError("invalid block length")
    if type(repetitions) is not int or repetitions < 2 or type(seed) is not int:
        raise ValueError("invalid bootstrap settings")
    if weighting not in ("pair", "exchange"):
        raise ValueError("invalid weighting")
    if any(not isinstance(k, str) or not k or type(v) is not int or v <= 0 for k, v in counts.items()):
        raise ValueError("invalid roster")
    exchanges = sorted(counts)
    weights = [counts[e] if weighting == "pair" else 1 for e in exchanges]
    series, last = [], None
    for row in dates:
        if not isinstance(row, dict) or not isinstance(row.get("date"), str):
            raise ValueError("invalid date")
        date = row["date"]
        if last is not None and date <= last:
            raise ValueError("duplicate or unordered date")
        last = date
        by = row.get("by_exchange")
        if not isinstance(by, dict) or set(by) != set(exchanges):
            raise ValueError("incomplete exchange panel")
        if any(type(by[e]) not in (int, float) or not isfinite(by[e]) for e in exchanges):
            raise ValueError("nonfinite contrast")
        series.append(_safe_weighted_mean([by[e] for e in exchanges], weights))
    rng = Random(seed)
    draws = []
    for _ in range(repetitions):
        indices = []
        while len(indices) < n:
            start = rng.randrange(n)
            indices.extend((start+j) % n for j in range(block_length))
        draws.append(_safe_mean(series[i] for i in indices[:n]))
    draws.sort()
    return {"mean": _safe_mean(series),
            "interval_95_percentile": [draws[int(.025*(repetitions-1))], draws[int(.975*(repetitions-1))]],
            "n_dates": n, "weighting": weighting, "block_length": block_length,
            "repetitions": repetitions, "seed": seed,
            "source_authenticated": False, "causal_inference_authorized": False}
