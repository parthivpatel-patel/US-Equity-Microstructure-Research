"""Fail-closed pre-reform placebo-window admission; no historical observations."""
from datetime import date

def admit_windows(sessions, pre, post, reform="2025-11-03", min_each=10):
    def check(xs, name):
        if not isinstance(xs, (list, tuple)) or not xs or any(type(x) is not str for x in xs):
            raise ValueError(name + ": invalid input")
        try:
            parsed = [date.fromisoformat(x) for x in xs]
        except ValueError as exc:
            raise ValueError(name + ": invalid date") from exc
        if any(d.isoformat() != x for d, x in zip(parsed, xs)) or len(set(xs)) != len(xs) or list(xs) != sorted(xs):
            raise ValueError(name + ": noncanonical, duplicate or unordered")
    for name, xs in (("sessions", sessions), ("pre", pre), ("post", post)):
        check(xs, name)
    if type(min_each) is not int or min_each < 2 or len(pre) < min_each or len(post) < min_each:
        raise ValueError("insufficient sessions")
    if not set(pre).issubset(sessions) or not set(post).issubset(sessions):
        raise ValueError("window outside observed sessions")
    if set(pre) & set(post) or pre[-1] >= post[0]:
        raise ValueError("overlapping or interleaved windows")
    reform_date = date.fromisoformat(reform)
    if reform_date.isoformat() != reform or post[-1] >= reform or pre[-1] >= reform:
        raise ValueError("placebo not strictly pre-reform")
    return {"pre_n": len(pre), "post_n": len(post), "placebo_date": post[0],
            "reform_date": reform, "source_authenticated": False,
            "treatment_authenticated": False, "causal_effect_established": False}
