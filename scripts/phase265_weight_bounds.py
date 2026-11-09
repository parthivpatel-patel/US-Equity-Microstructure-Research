"""Exact descriptive bounds under capped nonnegative matched-pair weights.

No historical observations are loaded; no inference or causal claim is made.
"""
import math

def bounds(contrasts, lower=0.0, upper=1.0):
    values = tuple(float(x) for x in contrasts)
    n = len(values)
    if not n or any(not math.isfinite(x) for x in values):
        raise ValueError("nonempty finite contrasts required")
    if not (math.isfinite(lower) and math.isfinite(upper) and 0 <= lower <= upper <= 1):
        raise ValueError("invalid weight bounds")
    if n * lower > 1 + 1e-12 or n * upper < 1 - 1e-12:
        raise ValueError("infeasible weight bounds")

    def optimize(reverse):
        weights = [lower] * n
        remaining = max(0.0, 1 - n * lower)
        for i in sorted(range(n), key=lambda j: (values[j], j), reverse=reverse):
            add = min(upper - lower, remaining)
            weights[i] += add
            remaining -= add
        if remaining > 1e-10:
            raise ValueError("infeasible weights")
        return sum(w * v for w, v in zip(weights, values)), weights

    lo, wlo = optimize(False)
    hi, whi = optimize(True)
    return {"equal_weight": sum(values)/n, "minimum": lo, "maximum": hi,
            "minimum_weights": wlo, "maximum_weights": whi, "n_pairs": n}
