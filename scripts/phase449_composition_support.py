"""Phase 449: common-date composition audit; descriptive, not source authentication."""
from collections import defaultdict
from datetime import date

def audit(rows, *, cutoff="2025-11-03"):
    boundary = date.fromisoformat(cutoff)
    seen = set()
    cells = defaultdict(lambda: defaultdict(lambda: {True: set(), False: set()}))
    assignment = {}
    count = 0
    for row in rows:
        d = date.fromisoformat(row["date"])
        security, exchange, group = (row[k] for k in ("security", "exchange", "matched_group"))
        if not all(isinstance(x, str) and x.strip() for x in (security, exchange, group)):
            raise ValueError("invalid identifier")
        treated = row["treated"]
        if type(treated) is not bool:
            raise ValueError("treated must be Boolean")
        key = (d, security, exchange)
        if key in seen:
            raise ValueError("duplicate security-date-exchange")
        seen.add(key)
        identity = (security, exchange)
        value = (group, treated)
        if identity in assignment and assignment[identity] != value:
            raise ValueError("unstable within-exchange assignment")
        assignment[identity] = value
        cells[(exchange, group)][d][treated].add(security)
        count += 1
    if count == 0:
        raise ValueError("empty input")
    output = []
    for (exchange, group), days in sorted(cells.items()):
        common = sorted(d for d, arms in days.items() if arms[True] and arms[False])
        def summarize(selected):
            if not selected:
                return {"dates": 0, "treated_intersection": 0, "control_intersection": 0,
                        "treated_union": 0, "control_union": 0, "stable_both_arms": False}
            result = {"dates": len(selected)}
            for arm, name in ((True, "treated"), (False, "control")):
                sets = [days[d][arm] for d in selected]
                result[name + "_intersection"] = len(set.intersection(*sets))
                result[name + "_union"] = len(set.union(*sets))
            result["stable_both_arms"] = (result["treated_intersection"] > 0
                                          and result["control_intersection"] > 0)
            return result
        pre = summarize([d for d in common if d < boundary])
        post = summarize([d for d in common if d >= boundary])
        output.append({"exchange": exchange, "matched_group": group,
                       "common_dates": len(common), "pre": pre, "post": post,
                       "stable_arms_across_both_periods":
                       bool(pre["stable_both_arms"] and post["stable_both_arms"]
                            and any(assignment[(s, exchange)] == (group, True)
                                    for s in set.intersection(
                                        *(days[d][True] for d in common)))
                            and any(assignment[(s, exchange)] == (group, False)
                                    for s in set.intersection(
                                        *(days[d][False] for d in common)))
                            ) if common else False})
    return {"observations": count, "cutoff": cutoff, "strata": output,
            "source_authenticated": False, "effect_estimated": False}
