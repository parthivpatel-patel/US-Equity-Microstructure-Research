"""Common-date descriptive Bartlett HAC estimator; not causal inference."""
from math import sqrt, isfinite

def common_date_hac(admitted, lag=0, weighting="pair"):
    if not isinstance(admitted, dict) or admitted.get("source_authenticated") is not False:
        raise ValueError("expected explicitly unauthenticated Phase 282 admission")
    dates = admitted["dates"]
    counts = admitted["pair_counts_by_exchange"]
    if not dates or not counts or type(lag) is not int or lag < 0 or lag >= len(dates):
        raise ValueError("invalid sample or lag")
    if weighting not in ("pair", "exchange"):
        raise ValueError("invalid weighting")
    if any(type(v) is not int or v <= 0 for v in counts.values()):
        raise ValueError("invalid roster")
    exchanges = set(counts)
    weights = {e: (counts[e] if weighting == "pair" else 1) for e in exchanges}
    denom = sum(weights.values())
    series = []
    seen = set()
    for row in dates:
        d = row["date"]
        if d in seen or (seen and d <= previous):
            raise ValueError("duplicate or unordered date")
        seen.add(d)
        previous = d
        by = row["by_exchange"]
        if set(by) != exchanges or any(type(v) not in (int, float) or not isfinite(v) for v in by.values()):
            raise ValueError("incomplete or invalid exchange panel")
        series.append(sum(weights[e]*by[e] for e in exchanges)/denom)
    n = len(series)
    mean = sum(series)/n
    residuals = [x-mean for x in series]
    gamma0 = sum(x*x for x in residuals)/n
    long_run = gamma0
    for k in range(1, lag+1):
        gamma = sum(residuals[t]*residuals[t-k] for t in range(k,n))/n
        long_run += 2*(1-k/(lag+1))*gamma
    variance = max(0.0, long_run/n)
    return {"n_dates":n, "lag":lag, "weighting":weighting, "mean":mean,
            "hac_standard_error":sqrt(variance), "source_authenticated":False,
            "causal_inference_authorized":False}
