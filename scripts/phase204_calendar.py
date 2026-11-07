"""Compare observed contrasts with a separately supplied session calendar."""
from datetime import date
from math import isfinite

def audit_calendar(rows, expected_sessions):
    def parse(value):
        if type(value) is not str:
            raise ValueError('session must be ISO date string')
        d = date.fromisoformat(value)
        if d.isoformat() != value or d.weekday() >= 5:
            raise ValueError('invalid weekday session')
        return value
    expected = [parse(x) for x in expected_sessions]
    if not expected or expected != sorted(set(expected)):
        raise ValueError('expected calendar empty, unordered or duplicated')
    observed = []
    for row in rows:
        d = parse(row['date'])
        v = row['contrast']
        if type(v) not in (int, float) or not isfinite(v):
            raise ValueError('invalid contrast')
        observed.append(d)
    if observed != sorted(set(observed)):
        raise ValueError('observed sessions unordered or duplicated')
    missing = sorted(set(expected) - set(observed))
    unexpected = sorted(set(observed) - set(expected))
    return {'admitted':bool(observed) and not missing and not unexpected,
            'expected_sessions':len(expected),'observed_sessions':len(observed),
            'missing_sessions':missing,'unexpected_sessions':unexpected,
            'calendar_authenticated':False,'source_authenticated':False,
            'treatment_authenticated':False}
