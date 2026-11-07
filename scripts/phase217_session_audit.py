"""Pre-reform US-equity session plausibility check; not an authenticated calendar."""
from datetime import date, timedelta
REFORM = date(2025, 11, 3)

def audit_candidate_sessions(sessions, closures=()):
    """Screen for weekends, duplicates and unexplained weekday gaps.

    closures are caller-supplied, NOT independently authenticated.
    """
    def parse(x):
        if type(x) is not str:
            raise ValueError('date must be a string')
        try:
            d = date.fromisoformat(x)
        except ValueError as exc:
            raise ValueError('invalid date') from exc
        if d.isoformat() != x:
            raise ValueError('noncanonical date')
        return d
    if type(sessions) not in (tuple, list) or not sessions:
        raise ValueError('nonempty sessions required')
    ds = [parse(x) for x in sessions]
    if ds != sorted(set(ds)) or ds[-1] >= REFORM:
        raise ValueError('sessions must be ordered, unique and pre-reform')
    if any(d.weekday() >= 5 for d in ds):
        raise ValueError('weekend cannot be a regular US equity session')
    if type(closures) not in (tuple, list, set):
        raise ValueError('closures must be a collection')
    cs = [parse(x) for x in closures]
    if len(set(cs)) != len(cs) or any(d.weekday() >= 5 for d in cs):
        raise ValueError('invalid closure roster')
    if any(ds[0] <= d <= ds[-1] and d in ds for d in cs):
        raise ValueError('closure also appears as a session')
    observed, closed = set(ds), set(cs)
    gaps = []
    d = ds[0]
    while d <= ds[-1]:
        if d.weekday() < 5 and d not in observed and d not in closed:
            gaps.append(d.isoformat())
        d += timedelta(days=1)
    if gaps:
        raise ValueError('unexplained missing weekdays: ' + ','.join(gaps))
    return {'first_session': ds[0].isoformat(),
            'last_session': ds[-1].isoformat(),
            'n_sessions': len(ds), 'n_supplied_closures': len(cs),
            'exchange_calendar_authenticated': False,
            'historical_inference_validated': False}
