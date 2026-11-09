"""Strict descriptive two-window pretrend diagnostic; not source authentication."""
from datetime import date
from math import isfinite

def evaluate(calendar, observations, early, late):
    """Calendar is a complete, independently supplied sequence of ISO dates.

    Observations are (ISO date, fixed-roster daily matched contrast) pairs.
    Windows are inclusive (start, end) ISO date pairs.
    """
    sessions = list(calendar)
    if len(sessions) < 4 or len(set(sessions)) != len(sessions):
        raise ValueError('calendar must have >=4 distinct sessions')
    try:
        days = [date.fromisoformat(s) for s in sessions]
    except (TypeError, ValueError) as exc:
        raise ValueError('invalid calendar date') from exc
    if any(a >= b for a, b in zip(days, days[1:])):
        raise ValueError('calendar not strictly increasing')
    rows = list(observations)
    if len(rows) != len(sessions):
        raise ValueError('incomplete or extra observations')
    seen = {}
    for d, y in rows:
        if not isinstance(d, str) or d in seen or d not in sessions:
            raise ValueError('duplicate or unexpected observation date')
        if isinstance(y, bool) or not isinstance(y, (float, int)) or not isfinite(y):
            raise ValueError('nonfinite or invalid outcome')
        seen[d] = float(y)
    if set(seen) != set(sessions):
        raise ValueError('missing calendar sessions')
    try:
        a, b = (date.fromisoformat(s) for s in early)
        c, d = (date.fromisoformat(s) for s in late)
    except (ValueError, TypeError) as exc:
        raise ValueError('invalid windows') from exc
    if not (a <= b < c <= d):
        raise ValueError('windows must be ordered and disjoint')

    def summarize(start, end):
        sample = [(day.toordinal(), seen[s]) for s, day in zip(sessions, days) if start <= day <= end]
        if len(sample) < 2:
            raise ValueError('each window needs at least two calendar sessions')
        x0 = sample[0][0]
        xs = [x-x0 for x, _ in sample]
        ys = [y for _, y in sample]
        xm, ym = sum(xs)/len(xs), sum(ys)/len(ys)
        denom = sum((x-xm)**2 for x in xs)
        slope = sum((x-xm)*(y-ym) for x, y in zip(xs, ys))/denom
        return {'n': len(xs), 'mean': ym, 'slope_per_calendar_day': slope}

    e, l = summarize(a, b), summarize(c, d)
    return {'early': e, 'late': l, 'late_minus_early_mean': l['mean']-e['mean'],
            'source_authenticated': False, 'treatment_authenticated': False,
            'causal_inference_authorized': False}
