"""Fail-closed session-calendar preflight for Phase 451 inference.

The supplied calendar MUST be authenticated independently; this module does not
fetch or certify trading calendars or source observations.
"""
from datetime import date

def _parse_unique(values, label):
    if isinstance(values, (str, bytes)):
        raise ValueError(f'{label} must be a sequence')
    try:
        parsed = [date.fromisoformat(x) for x in values]
    except (TypeError, ValueError) as exc:
        raise ValueError(f'invalid {label} date') from exc
    if len(parsed) != len(set(parsed)):
        raise ValueError(f'duplicate {label} date')
    return set(parsed)

def preflight(observed_dates, exchange_sessions, cutoff='2025-11-03',
              block_length=5, calendar_authenticated=False):
    """Check fully balanced observed dates against an independently supplied calendar.

    Missing sessions within the covered pre/post spans are a hard failure;
    missing sessions outside observed spans are not considered.
    """
    if type(block_length) is not int or block_length < 1:
        raise ValueError('invalid block length')
    if type(calendar_authenticated) is not bool:
        raise ValueError('invalid authentication flag')
    boundary = date.fromisoformat(cutoff)
    observed = _parse_unique(observed_dates, 'observed')
    sessions = _parse_unique(exchange_sessions, 'session')
    unknown = sorted(observed - sessions)
    periods = {}
    for label, predicate in [('pre', lambda d: d < boundary),
                             ('post', lambda d: d >= boundary)]:
        dates = sorted(d for d in observed if predicate(d))
        covered = sorted(d for d in sessions if dates and dates[0] <= d <= dates[-1])
        missing = sorted(set(covered) - set(dates))
        periods[label] = {
            'observed_dates': len(dates), 'covered_sessions': len(covered),
            'missing_sessions': [d.isoformat() for d in missing],
            'sufficient_for_blocks': len(dates) >= 2 * block_length,
            'contiguous_sessions': bool(dates) and not missing,
        }
    structural_pass = (not unknown and all(v['contiguous_sessions'] and
                       v['sufficient_for_blocks'] for v in periods.values()))
    return {
        'passes_structural_screen': structural_pass,
        'passes_authenticated_preflight': structural_pass and calendar_authenticated,
        'calendar_authenticated_by_caller': calendar_authenticated,
        'observations_outside_calendar': [d.isoformat() for d in unknown],
        'pre': periods['pre'], 'post': periods['post'],
        'warning': 'Caller authentication flag is an assertion, not proof. Verify calendar provenance and source SHA-256 separately. Circular blocks still wrap at period boundaries.'
    }
