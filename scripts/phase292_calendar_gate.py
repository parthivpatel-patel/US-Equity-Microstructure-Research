"""Fail-closed calendar admission wrapper for Phase 289; not source authentication."""
from datetime import date

def canonical_day(value):
    if type(value) is not str or len(value) != 10 or value[4] != '-' or value[7] != '-':
        raise ValueError('noncanonical session date')
    digits = value[:4] + value[5:7] + value[8:]
    if not digits.isascii() or not digits.isdigit():
        raise ValueError('noncanonical session date')
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError('noncanonical session date')
    return parsed

def admit_calendar(admitted, expected_sessions):
    if not isinstance(admitted, dict) or admitted.get('source_authenticated') is not False:
        raise ValueError('unauthenticated descriptive panel required')
    if not isinstance(expected_sessions, (list, tuple)) or not expected_sessions:
        raise ValueError('nonempty calendar required')
    expected = [canonical_day(x) for x in expected_sessions]
    if expected != sorted(set(expected)):
        raise ValueError('calendar must be unique and sorted')
    rows = admitted.get('dates')
    if not isinstance(rows, list) or any(not isinstance(row, dict) or 'date' not in row for row in rows):
        raise ValueError('invalid observations')
    observed = [canonical_day(row['date']) for row in rows]
    if observed != expected:
        raise ValueError('observed sessions differ from supplied calendar')
    return admitted

def calendar_gated_bootstrap(admitted, expected_sessions, **kwargs):
    """Calendar checks first; then delegate to Phase 289's original estimator."""
    from phase289_common_date_block_bootstrap import bootstrap_common_dates
    return bootstrap_common_dates(admit_calendar(admitted, expected_sessions), **kwargs)
