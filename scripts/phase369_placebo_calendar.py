"""Audit dated pseudo-event windows before any empirical p-value interpretation.

No SEC observations are bundled. Calendar uses supplied trading sessions, not weekdays.
"""
from datetime import date


def audit_calendar(sessions, event_dates, half_window=5):
    if type(half_window) is not int or half_window < 1:
        raise ValueError('half_window must be a positive integer')
    if not isinstance(sessions, (list, tuple)) or not isinstance(event_dates, (list, tuple)):
        raise ValueError('sessions and event_dates must be ordered sequences')
    if any(type(d) is not date for d in sessions + event_dates):
        raise ValueError('all entries must be datetime.date, not datetime.datetime')
    if list(sessions) != sorted(set(sessions)):
        raise ValueError('sessions must be strictly increasing and unique')
    if len(set(event_dates)) != len(event_dates):
        raise ValueError('duplicate event dates')
    index = {d: i for i, d in enumerate(sessions)}
    windows = {}
    for event in event_dates:
        if event not in index:
            raise ValueError(f'event absent from trading calendar: {event}')
        i = index[event]
        if i < half_window or i + half_window > len(sessions):
            raise ValueError(f'incomplete event window: {event}')
        windows[event.isoformat()] = {
            'pre': [d.isoformat() for d in sessions[i-half_window:i]],
            'post': [d.isoformat() for d in sessions[i:i+half_window]],
        }
    pairs = []
    for a, ea in enumerate(event_dates):
        for eb in event_dates[a+1:]:
            ia, ib = index[ea], index[eb]
            wa = set(range(ia-half_window, ia+half_window))
            wb = set(range(ib-half_window, ib+half_window))
            common = len(wa & wb)
            if common:
                pairs.append({'first': ea.isoformat(), 'second': eb.isoformat(),
                              'shared_sessions': common})
    return {'events': len(event_dates), 'overlapping_pairs': len(pairs),
            'pairs': pairs, 'windows': windows}
