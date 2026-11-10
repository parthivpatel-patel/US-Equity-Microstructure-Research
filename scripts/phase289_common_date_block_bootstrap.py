"""Common-date circular block bootstrap; descriptive, unauthenticated panels only."""
from math import isfinite
from random import Random

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
    denominator = sum(weights)
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
        series.append(sum(w * by[e] for w, e in zip(weights, exchanges)) / denominator)
    rng = Random(seed)
    draws = []
    for _ in range(repetitions):
        indices = []
        while len(indices) < n:
            start = rng.randrange(n)
            indices.extend((start+j) % n for j in range(block_length))
        draws.append(sum(series[i] for i in indices[:n]) / n)
    draws.sort()
    return {"mean": sum(series)/n,
            "interval_95_percentile": [draws[int(.025*(repetitions-1))], draws[int(.975*(repetitions-1))]],
            "n_dates": n, "weighting": weighting, "block_length": block_length,
            "repetitions": repetitions, "seed": seed,
            "source_authenticated": False, "causal_inference_authorized": False}
