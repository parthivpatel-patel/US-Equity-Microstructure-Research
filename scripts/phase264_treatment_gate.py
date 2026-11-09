"""Fail-closed structural roster validation. Does not authenticate historical data."""
from collections import Counter
from math import isfinite

def audit(roster, observations, expected_dates):
    """Roster: (pair, security, exchange, arm); observations: (date, pair, security, exchange, arm, value)."""
    roster, observations, dates = list(roster), list(observations), list(expected_dates)
    problems = []
    if not dates or len(set(dates)) != len(dates): problems.append("invalid_calendar")
    if not roster: problems.append("empty_roster")
    if len(set(roster)) != len(roster): problems.append("duplicate_roster_entry")
    pair_arm = Counter((p, a) for p, s, e, a in roster)
    for p, a in pair_arm:
        if a not in ("treated", "control"): problems.append("invalid_arm")
        if pair_arm[p, a] != 1: problems.append("multiple_securities_per_pair_arm")
    for p in {p for p, s, e, a in roster}:
        if pair_arm[p, "treated"] != 1 or pair_arm[p, "control"] != 1:
            problems.append("unbalanced_pair")
    identities = Counter((s, e) for p, s, e, a in roster)
    if any(n > 1 for n in identities.values()): problems.append("security_exchange_reused")
    required = {(d, p, s, e, a) for d in dates for p, s, e, a in roster}
    observed = Counter((d, p, s, e, a) for d, p, s, e, a, v in observations)
    if any(n > 1 for n in observed.values()): problems.append("duplicate_observation")
    if required - set(observed): problems.append("missing_observation")
    if set(observed) - required: problems.append("unexpected_observation")
    for d, p, s, e, a, v in observations:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v):
            problems.append("invalid_outcome")
            break
    return {"passed": not problems, "problems": sorted(set(problems)),
            "required_cells": len(required), "observed_cells": len(observed),
            "authenticated": False, "historical_inference_authorized": False}
