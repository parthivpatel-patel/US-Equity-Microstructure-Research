"""Compare local paired-date and globally balanced matched-group DiD support.

Descriptive sensitivity only. Requires authenticated inputs before empirical use.
"""
from collections import defaultdict
from datetime import date
import math

def compare(rows, cutoff="2025-11-03"):
    boundary = date.fromisoformat(cutoff)
    sums = defaultdict(lambda: [0.0, 0])
    seen = set()
    assignments = {}
    for row in rows:
        s, e, g = (row[k] for k in ("security", "exchange", "matched_group"))
        if not all(isinstance(v, str) and v.strip() for v in (s, e, g)):
            raise ValueError("invalid identifier")
        d = date.fromisoformat(row["date"])
        t, y = row["treated"], row["outcome"]
        if type(t) is not bool or isinstance(y, bool) or not isinstance(y, (int, float)) or not math.isfinite(y):
            raise ValueError("invalid treatment or outcome")
        if (s, e, d) in seen:
            raise ValueError("duplicate security-exchange-date")
        seen.add((s, e, d))
        if (s, e) in assignments and assignments[(s, e)] != (g, t):
            raise ValueError("unstable assignment")
        assignments[(s, e)] = (g, t)
        a = sums[(e, g, d, t)]
        a[0] += y
        a[1] += 1
    if not sums:
        raise ValueError("empty input")
    strata = {(e, g) for e, g, _, _ in sums}
    cells = {}
    for e, g, d, t in sums:
        left = sums.get((e, g, d, True))
        right = sums.get((e, g, d, False))
        if left and right:
            cells[(e, g, d)] = left[0] / left[1] - right[0] / right[1]
    dates_by_stratum = {st: {d for e, g, d in cells if (e, g) == st} for st in strata}
    global_dates = set.intersection(*dates_by_stratum.values())
    def estimate(eligible):
        effects = []
        used = 0
        for e, g in sorted(strata):
            pre = [v for (ee, gg, d), v in cells.items() if (ee, gg) == (e, g) and d < boundary and eligible(d)]
            post = [v for (ee, gg, d), v in cells.items() if (ee, gg) == (e, g) and d >= boundary and eligible(d)]
            if pre and post:
                effects.append(sum(post) / len(post) - sum(pre) / len(pre))
                used += len(pre) + len(post)
        return {"estimate": sum(effects) / len(effects) if effects else None,
                "eligible_strata": len(effects), "paired_stratum_date_cells": used}
    local = estimate(lambda d: True)
    balanced = estimate(lambda d: d in global_dates)
    return {"local": local, "globally_balanced": balanced,
            "difference_global_minus_local": balanced["estimate"] - local["estimate"] if local["estimate"] is not None and balanced["estimate"] is not None else None,
            "globally_balanced_dates": len(global_dates), "total_strata": len(strata),
            "source_authenticated": False, "causal_identification_established": False}
