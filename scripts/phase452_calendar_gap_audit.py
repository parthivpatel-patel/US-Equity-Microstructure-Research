"""Audit whether Phase 451's date blocks correspond to consecutive trading sessions.

No historical inference or authentication is performed.
"""
from datetime import date

def audit(dates, cutoff='2025-11-03', max_calendar_gap=4):
    if type(max_calendar_gap) is not int or max_calendar_gap < 1:
        raise ValueError('invalid max_calendar_gap')
    boundary = date.fromisoformat(cutoff)
    parsed = [date.fromisoformat(x) for x in dates]
    if len(set(parsed)) != len(parsed):
        raise ValueError('duplicate dates')
    result = {}
    for label, period in [('pre', sorted(d for d in parsed if d < boundary)),
                          ('post', sorted(d for d in parsed if d >= boundary))]:
        gaps = [(a.isoformat(), b.isoformat(), (b-a).days)
                for a,b in zip(period, period[1:]) if (b-a).days > max_calendar_gap]
        result[label] = {'dates':len(period), 'large_gaps':gaps,
                         'calendar_span_days':(period[-1]-period[0]).days if period else 0}
    result['passes_gap_screen'] = bool(result['pre']['dates'] and result['post']['dates'] and
                                       not result['pre']['large_gaps'] and not result['post']['large_gaps'])
    result['caveat'] = ('A calendar-gap screen cannot authenticate exchange trading sessions; '
                        'holiday schedules and missing exchange-specific sessions require verified calendars.')
    return result
