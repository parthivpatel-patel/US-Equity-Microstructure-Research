"""Explicit calendar coverage gate. Calendar source authentication is external."""
from datetime import date
from math import isfinite

def validate(rows, expected_sessions, cutoff):
    cut = date.fromisoformat(cutoff)
    if not isinstance(expected_sessions, (list, tuple)) or not expected_sessions:
        raise ValueError("nonempty calendar required")
    sessions = [date.fromisoformat(s) for s in expected_sessions]
    if sessions != sorted(set(sessions)) or any(d.weekday() >= 5 for d in sessions):
        raise ValueError("calendar must be sorted, unique, weekdays")
    if not any(d < cut for d in sessions) or not any(d >= cut for d in sessions):
        raise ValueError("calendar must straddle cutoff")
    seen, by_date = set(), {}
    for r in rows:
        d, p = date.fromisoformat(r["date"]), r["pair_id"]
        if not isinstance(p, str) or not p:
            raise ValueError("invalid pair")
        if (d,p) in seen:
            raise ValueError("duplicate date-pair")
        seen.add((d,p))
        for k in ("treated","control"):
            v = r[k]
            if type(v) not in (int,float) or not isfinite(v):
                raise ValueError("invalid outcome")
        by_date.setdefault(d,set()).add(p)
    expected, actual = set(sessions), set(by_date)
    roster = set.union(*by_date.values()) if by_date else set()
    missing, extra = sorted(expected-actual), sorted(actual-expected)
    partial = {d.isoformat():sorted(roster-by_date[d]) for d in sorted(expected&actual) if roster-by_date[d]}
    return {"missing_sessions":[d.isoformat() for d in missing],
            "extra_sessions":[d.isoformat() for d in extra],
            "partial_sessions":partial,"n_pairs_union":len(roster),
            "n_expected_sessions":len(sessions),"n_observed_sessions":len(actual),
            "admitted":bool(roster) and not (missing or extra or partial),
            "calendar_authenticated":False,"historical_inference_authorized":False}
