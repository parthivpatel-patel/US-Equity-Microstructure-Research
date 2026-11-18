"""Audit internal historical treatment consistency across exchanges and periods.

Does not authenticate external treatment provenance or establish causality.
"""
from collections import defaultdict
from datetime import date


def audit(rows, cutoff="2025-11-03"):
    boundary = date.fromisoformat(cutoff)
    if not rows:
        raise ValueError("empty observations")
    seen = set()
    by_security = defaultdict(lambda: defaultdict(set))
    by_exchange = defaultdict(lambda: defaultdict(set))
    by_group = defaultdict(set)
    for r in rows:
        s, e, g = (r[k] for k in ("security", "exchange", "matched_group"))
        if not all(isinstance(x, str) and x.strip() for x in (s, e, g)):
            raise ValueError("invalid identifier")
        d = date.fromisoformat(r["date"])
        t = r["treated"]
        if type(t) is not bool:
            raise ValueError("treatment must be boolean")
        if (s, e, d) in seen:
            raise ValueError("duplicate security-exchange-date")
        seen.add((s, e, d))
        period = "pre" if d < boundary else "post"
        by_security[s][period].add(t)
        by_exchange[(s, e)][period].add((g, t))
        by_group[(e, g, period)].add(t)
    conflicts = sorted(s for s, periods in by_security.items()
                       if len(set().union(*periods.values())) > 1)
    unstable_exchange = sorted((s, e) for (s, e), periods in by_exchange.items()
                               if len(set().union(*periods.values())) > 1)
    one_arm = sorted((e, g, p) for (e, g, p), arms in by_group.items() if len(arms) == 1)
    missing_period = sorted(s for s, periods in by_security.items() if len(periods) != 2)
    return {"observations": len(seen), "securities": len(by_security),
            "global_treatment_conflicts": conflicts,
            "exchange_assignment_conflicts": unstable_exchange,
            "single_arm_group_periods": one_arm,
            "securities_missing_pre_or_post": missing_period,
            "pass_assignment_consistency": not conflicts and not unstable_exchange,
            "source_authenticated": False, "treatment_authenticated": False}
