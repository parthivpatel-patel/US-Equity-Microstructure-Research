"""Structural temporal gate for HAC input; does not authenticate exchange calendar."""
import datetime as dt
import math

def validate_temporal_series(series, expected_sessions, cutoff):
    if type(cutoff) is not dt.date:
        raise ValueError("cutoff must be a date")
    expected = list(expected_sessions)
    if not expected or any(type(d) is not dt.date for d in expected):
        raise ValueError("invalid expected sessions")
    if expected != sorted(set(expected)):
        raise ValueError("expected sessions must be unique and increasing")
    observed = list(series)
    if not observed:
        raise ValueError("empty series")
    if any(not isinstance(item, (tuple, list)) or len(item) != 2 for item in observed):
        raise ValueError("expected date/value records")
    dates = [item[0] for item in observed]
    if any(type(d) is not dt.date for d in dates):
        raise ValueError("invalid observation dates")
    if dates != sorted(set(dates)):
        raise ValueError("observations must be unique and increasing")
    missing = sorted(set(expected) - set(dates))
    extra = sorted(set(dates) - set(expected))
    if missing or extra:
        raise ValueError(f"calendar mismatch: missing={missing}, extra={extra}")
    if any(not math.isfinite(float(item[1])) for item in observed):
        raise ValueError("nonfinite outcome")
    pre = sum(d < cutoff for d in dates)
    post = len(dates) - pre
    if min(pre, post) < 2:
        raise ValueError("at least two dates per period required")
    return {"dates": len(dates), "pre_dates": pre, "post_dates": post,
            "structural_coverage_pass": True, "calendar_authenticated": False,
            "source_authenticated": False, "historical_inference_authorized": False}
