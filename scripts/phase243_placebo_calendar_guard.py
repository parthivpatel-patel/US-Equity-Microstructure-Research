"""Structural date guard for descriptive placebo scans; not exchange-calendar authentication."""
from datetime import date

def validate_placebo_sessions(daily, cuts, half_window, *, require_weekdays=True):
    if not isinstance(daily, list) or not daily:
        raise ValueError('nonempty daily list required')
    if type(half_window) is not int or half_window < 2:
        raise ValueError('half_window must be integer >= 2')
    if not isinstance(cuts, (list, tuple)) or not cuts or any(type(c) is not int for c in cuts):
        raise ValueError('integer cuts required')
    if list(cuts) != sorted(set(cuts)):
        raise ValueError('cuts must be sorted and unique')
    sessions = []
    for row in daily:
        if not isinstance(row, dict) or type(row.get('date')) is not str:
            raise ValueError('date string required')
        value = row['date']
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError('invalid ISO session date') from exc
        if parsed.isoformat() != value:
            raise ValueError('noncanonical session date')
        if require_weekdays and parsed.weekday() >= 5:
            raise ValueError('weekend date is not a regular equity session')
        sessions.append(parsed)
    if sessions != sorted(set(sessions)):
        raise ValueError('sessions must be strictly increasing and unique')
    if any(c < half_window or c + half_window > len(sessions) for c in cuts):
        raise ValueError('cut lacks complete symmetric observation window')
    return {'n_sessions': len(sessions), 'n_cuts': len(cuts),
            'calendar_independently_verified': False,
            'warning': 'Weekday/date structure is not authoritative exchange-session authentication. Holidays and exceptional closures require independent evidence.'}
