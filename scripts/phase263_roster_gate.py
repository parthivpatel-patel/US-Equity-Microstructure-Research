"""Fail-closed fixed-roster panel audit; structural validation only."""
from datetime import date
from math import isfinite

def audit(rows, expected_sessions, expected_pairs, cutoff):
    if not isinstance(expected_sessions, (list, tuple)) or not expected_sessions:
        raise ValueError("expected sessions required")
    if not isinstance(expected_pairs, (list, tuple)) or not expected_pairs:
        raise ValueError("external fixed roster required")
    if any(not isinstance(p, str) or not p.strip() for p in expected_pairs):
        raise ValueError("invalid pair identifier")
    if len(set(expected_pairs)) != len(expected_pairs):
        raise ValueError("duplicate expected pair")
    sessions = [date.fromisoformat(s) for s in expected_sessions]
    if sessions != sorted(set(sessions)) or any(s.weekday() >= 5 for s in sessions):
        raise ValueError("invalid expected session sequence")
    cut = date.fromisoformat(cutoff)
    if not any(s < cut for s in sessions) or not any(s >= cut for s in sessions):
        raise ValueError("cutoff must separate expected sessions")
    observed = set()
    for r in rows:
        d = date.fromisoformat(r["date"])
        p = r["pair_id"]
        if not isinstance(p, str) or not p.strip():
            raise ValueError("invalid observed pair")
        key = (d, p)
        if key in observed:
            raise ValueError("duplicate observation")
        observed.add(key)
        for field in ("treated", "control"):
            v = r[field]
            if type(v) not in (int, float) or not isfinite(v):
                raise ValueError("nonfinite or nonnumeric outcome")
    required = {(d, p) for d in sessions for p in expected_pairs}
    missing = sorted(required - observed)
    extra = sorted(observed - required)
    return {
        "n_expected_cells": len(required), "n_observed_cells": len(observed),
        "missing_cells": [{"date": d.isoformat(), "pair_id": p} for d,p in missing],
        "extra_cells": [{"date": d.isoformat(), "pair_id": p} for d,p in extra],
        "structurally_complete": not missing and not extra,
        "source_authenticated": False, "calendar_authenticated": False,
        "treatment_authenticated": False, "historical_inference_authorized": False,
    }
