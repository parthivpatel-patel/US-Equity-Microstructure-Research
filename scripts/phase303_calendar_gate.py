"""Strict date/calendar audit for provisional SEC daily panels; no source authentication."""
from datetime import date

def audit_calendar(rows, expected_dates):
    """Check consistency only; upstream calendar authenticity is NOT established."""
    if not isinstance(rows, list) or not isinstance(expected_dates, list) or not expected_dates:
        raise ValueError('nonempty list inputs required')
    def parse(s):
        if type(s) is not str:
            raise ValueError('date must be string')
        try:
            d = date.fromisoformat(s)
        except ValueError as e:
            raise ValueError('invalid ISO date') from e
        if d.isoformat() != s or d.weekday() >= 5:
            raise ValueError('noncanonical date or weekend')
        return d
    expected = [parse(x) for x in expected_dates]
    if expected != sorted(set(expected)):
        raise ValueError('expected dates unordered or duplicate')
    actual = []
    for row in rows:
        if not isinstance(row, dict) or 'date' not in row:
            raise ValueError('row missing date')
        actual.append(parse(row['date']))
    if actual != sorted(set(actual)):
        raise ValueError('row dates unordered or duplicate')
    missing = sorted(set(expected)-set(actual))
    extra = sorted(set(actual)-set(expected))
    return {'calendar_consistent': not missing and not extra,
            'missing_dates': [x.isoformat() for x in missing],
            'extra_dates': [x.isoformat() for x in extra],
            'n_rows': len(actual), 'n_expected': len(expected),
            'calendar_authenticated': False, 'source_authenticated': False,
            'causal_inference_authorized': False}
