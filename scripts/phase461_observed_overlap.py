"""Observed matched-cell overlap across pre-reform placebo boundaries.

Descriptive only: inputs are not authenticated; no inference or causal claim.
"""
from collections import defaultdict
from datetime import date
from math import isfinite


def observed_overlap(rows, boundaries, reform="2025-11-03", min_pre=2, min_post=2):
    reform_day = date.fromisoformat(reform)
    cuts = sorted(date.fromisoformat(x) for x in boundaries)
    if not cuts or len(set(cuts)) != len(cuts) or any(c >= reform_day for c in cuts):
        raise ValueError("invalid placebo boundaries")
    if type(min_pre) is not int or type(min_post) is not int or min_pre < 1 or min_post < 1:
        raise ValueError("invalid minimum support")
    seen, assignment, global_arm = set(), {}, {}
    cells = defaultdict(lambda: {True: [], False: []})
    for row in rows:
        s, e, g = (row[k] for k in ("security", "exchange", "matched_group"))
        if not all(isinstance(v, str) and v.strip() for v in (s, e, g)):
            raise ValueError("invalid identifier")
        d = date.fromisoformat(row["date"])
        t, y = row["treated"], row["outcome"]
        if type(t) is not bool or type(y) not in (int, float) or not isfinite(y):
            raise ValueError("invalid treatment/outcome")
        if (s, e, d) in seen:
            raise ValueError("duplicate observation")
        seen.add((s, e, d))
        if (s, e) in assignment and assignment[(s, e)] != (g, t):
            raise ValueError("unstable matched assignment")
        assignment[(s, e)] = (g, t)
        if s in global_arm and global_arm[s] != t:
            raise ValueError("cross-exchange treatment conflict")
        global_arm[s] = t
        if d < reform_day:
            cells[(e, g, d)][t].append(float(y))
    paired = defaultdict(set)
    for (e, g, d), arms in cells.items():
        if arms[True] and arms[False]:
            paired[(e, g)].add(d)
    eligible = {}
    windows = []
    for cut in cuts:
        supported = {k for k, dates in paired.items()
                     if sum(d < cut for d in dates) >= min_pre
                     and sum(cut <= d < reform_day for d in dates) >= min_post}
        eligible[cut] = supported
        windows.append({"cutoff": cut.isoformat(), "eligible_groups": len(supported),
                        "paired_dates_in_eligible_groups": sum(len(paired[k]) for k in supported)})
    common = set.intersection(*(eligible[c] for c in cuts))
    comparisons = []
    for i, a in enumerate(cuts):
        for b in cuts[i + 1:]:
            shared = eligible[a] & eligible[b]
            dates = set().union(*(paired[k] for k in shared)) if shared else set()
            comparisons.append({"first": a.isoformat(), "second": b.isoformat(),
                                "common_eligible_groups": len(shared),
                                "distinct_paired_dates_on_common_groups": len(dates),
                                "reassigned_observed_dates": sum(a <= d < b for d in dates),
                                "shared_pre_dates": sum(d < a for d in dates),
                                "shared_post_dates": sum(b <= d < reform_day for d in dates),
                                "note": "Distinct dates are not independent observations; groups may overlap."})
    return {"windows": windows, "comparisons": comparisons,
            "common_groups_all_boundaries": len(common),
            "paired_group_date_cells": sum(map(len, paired.values())),
            "unpaired_group_date_cells": len(cells) - sum(map(len, paired.values())),
            "source_authenticated": False, "treatment_authenticated": False,
            "serial_dependence_inference_performed": False}
