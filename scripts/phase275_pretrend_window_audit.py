"""Strict pretrend-window admission; supplied calendar is NOT authenticated."""
from datetime import date

def audit_windows(calendar, early, late, *, require_contiguous_partition=False):
    def parse(value):
        if not isinstance(value, str) or len(value) != 10 or value[4] != '-' or value[7] != '-':
            raise ValueError('dates must use YYYY-MM-DD')
        try:
            d = date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError('invalid ISO date') from exc
        if d.isoformat() != value:
            raise ValueError('noncanonical date')
        return d
    sessions = [parse(s) for s in calendar]
    if len(sessions) < 4 or any(a >= b for a, b in zip(sessions, sessions[1:])):
        raise ValueError('calendar must contain >=4 strictly increasing sessions')
    if len(early) != 2 or len(late) != 2:
        raise ValueError('windows must have exactly two endpoints')
    a, b = map(parse, early)
    c, d = map(parse, late)
    if not a <= b < c <= d:
        raise ValueError('windows must be ordered and disjoint')
    if any(x not in sessions for x in (a, b, c, d)):
        raise ValueError('window endpoints must be actual supplied exchange sessions')
    e = [x for x in sessions if a <= x <= b]
    l = [x for x in sessions if c <= x <= d]
    if len(e) < 2 or len(l) < 2:
        raise ValueError('each window requires at least two sessions')
    if require_contiguous_partition and (a != sessions[0] or d != sessions[-1] or sessions.index(c) != sessions.index(b)+1):
        raise ValueError('windows must partition the supplied calendar without gaps')
    return {'early_sessions': len(e), 'late_sessions': len(l), 'gap_sessions': sum(b < x < c for x in sessions),
            'excluded_before': sum(x < a for x in sessions), 'excluded_after': sum(x > d for x in sessions),
            'calendar_authenticated': False, 'historical_inference_authorized': False}
