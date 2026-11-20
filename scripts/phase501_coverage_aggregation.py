"""Descriptive Phase 500 coverage aggregation; not causal inference."""
from collections import defaultdict

def aggregate_coverage(rows):
    """Separate equal-date and eligible-count weighting on common support."""
    groups = defaultdict(list)
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid row")
        try:
            ex, day, period = row["exchange"], row["date"], row["period"]
            te, to = row["treated_eligible"], row["treated_observed"]
            ce, co = row["control_eligible"], row["control_observed"]
        except KeyError as exc:
            raise ValueError("missing field") from exc
        if not all(isinstance(v, str) and v for v in (ex, day)) or period not in ("pre", "post"):
            raise ValueError("invalid group key")
        if (ex, day) in seen:
            raise ValueError("duplicate exchange-date")
        seen.add((ex, day))
        if any(type(v) is not int or v < 0 for v in (te, to, ce, co)) or to > te or co > ce or te + ce == 0:
            raise ValueError("invalid coverage counts")
        groups[(ex, period)].append((te, to, ce, co))
    if not groups:
        raise ValueError("empty input")
    out = []
    for (ex, period), cells in sorted(groups.items()):
        both = [(te, to, ce, co) for te, to, ce, co in cells if te and ce]
        te_all, to_all, ce_all, co_all = (sum(c[i] for c in cells) for i in range(4))
        gap = weighted_gap = None
        if both:
            gap = sum(to / te - co / ce for te, to, ce, co in both) / len(both)
            weighted_gap = (sum(c[1] for c in both) / sum(c[0] for c in both)
                            - sum(c[3] for c in both) / sum(c[2] for c in both))
        out.append({
            "exchange": ex, "period": period, "eligible_dates": len(cells),
            "common_support_dates": len(both), "excluded_dates": len(cells) - len(both),
            "treated_coverage_all": to_all / te_all if te_all else None,
            "control_coverage_all": co_all / ce_all if ce_all else None,
            "common_date_equal_weight_gap": gap,
            "common_date_eligible_weight_gap": weighted_gap,
            "common_date_gap_weighting_difference": gap - weighted_gap if gap is not None else None,
        })
    return out
