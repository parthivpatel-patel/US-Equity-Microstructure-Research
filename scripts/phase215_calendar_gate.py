"""Explicit session-calendar gate. Input calendar requires independent authentication."""
from datetime import date
from math import isfinite

REFORM = '2025-11-03'

def admit_sessions(rows, sessions, early, late):
    def valid_date(x):
        if type(x) is not str:
            raise ValueError('date must be ISO string')
        try:
            if date.fromisoformat(x).isoformat() != x:
                raise ValueError('noncanonical date')
        except (TypeError, ValueError) as exc:
            raise ValueError('invalid ISO date') from exc
        return x
    calendar = [valid_date(x) for x in sessions]
    if not calendar or calendar != sorted(set(calendar)) or calendar[-1] >= REFORM:
        raise ValueError('calendar must be unique, ordered and pre-reform')
    if type(rows) not in (tuple, list) or not rows:
        raise ValueError('observations required')
    dates = []
    for row in rows:
        if type(row) is not dict or set(row) != {'date', 'contrast'}:
            raise ValueError('invalid row schema')
        dates.append(valid_date(row['date']))
        if type(row['contrast']) not in (int, float) or not isfinite(row['contrast']):
            raise ValueError('invalid contrast')
    if dates != calendar:
        raise ValueError('observations must match all supplied sessions exactly')
    def check_window(w):
        if type(w) not in (tuple, list) or len(w) != 2:
            raise ValueError('invalid window')
        a, b = map(valid_date, w)
        if a not in calendar or b not in calendar or a > b:
            raise ValueError('window endpoints must be observed sessions')
        return calendar.index(a), calendar.index(b)
    e, l = check_window(early), check_window(late)
    if e[1] >= l[0]:
        raise ValueError('overlapping or reversed windows')
    return {'n_sessions': len(calendar), 'early_n': e[1]-e[0]+1,
            'late_n': l[1]-l[0]+1, 'gap_sessions': l[0]-e[1]-1,
            'calendar_authenticated': False, 'source_authenticated': False,
            'treatment_authenticated': False}
