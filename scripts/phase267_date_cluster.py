"""Date-level HAC diagnostic for complete matched treated-control panels."""
import math

def analyze(rows, cutoff, lag=None):
    if not rows:
        raise ValueError("empty panel")
    dates = sorted({r[0] for r in rows})
    pairs = sorted({r[1] for r in rows})
    if any(not isinstance(d, str) or len(d) != 10 for d in dates):
        raise ValueError("dates must be ISO strings")
    if len(dates) < 6 or len(pairs) < 2:
        raise ValueError("requires six dates and two pairs")
    seen = {}
    for date, pair, value in rows:
        if (date, pair) in seen or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("duplicate or nonfinite observation")
        seen[date, pair] = float(value)
    if len(seen) != len(dates) * len(pairs):
        raise ValueError("incomplete fixed roster")
    daily = [sum(seen[d, p] for p in pairs) / len(pairs) for d in dates]
    pre = [v for d, v in zip(dates, daily) if d < cutoff]
    post = [v for d, v in zip(dates, daily) if d >= cutoff]
    if len(pre) < 3 or len(post) < 3:
        raise ValueError("requires three dates on each side")
    estimate = sum(post) / len(post) - sum(pre) / len(pre)
    mean_pre, mean_post = sum(pre) / len(pre), sum(post) / len(post)
    residuals = [v - (mean_pre if d < cutoff else mean_post) for d, v in zip(dates, daily)]
    n = len(dates)
    weights = [-1 / len(pre) if d < cutoff else 1 / len(post) for d in dates]
    z = [w * e for w, e in zip(weights, residuals)]
    if lag is None:
        lag = max(0, int(4 * (n / 100) ** (2 / 9)))
    if type(lag) is not int or not 0 <= lag < n:
        raise ValueError("invalid lag")
    variance = sum(v * v for v in z)
    for k in range(1, lag + 1):
        variance += 2 * (1 - k / (lag + 1)) * sum(z[t] * z[t-k] for t in range(k, n))
    return {"n_dates": n, "n_pairs": len(pairs), "n_pre": len(pre), "n_post": len(post),
            "estimate": estimate, "hac_lag": lag, "hac_se": math.sqrt(max(0.0, variance)),
            "source_authenticated": False, "causal_effect_established": False,
            "warning": "HAC assumes weak dependence and cannot resolve pretrends or placebo failures."}
