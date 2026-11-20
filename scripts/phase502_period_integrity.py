"""Validate date/period integrity before descriptive coverage aggregation.

This module does not authenticate SEC source data or estimate treatment effects.
"""
from datetime import date


def canonical_day(value):
    if not isinstance(value, str) or len(value) != 10:
        raise ValueError('date must use YYYY-MM-DD')
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('invalid calendar date') from exc
    if parsed.isoformat() != value:
        raise ValueError('date must use YYYY-MM-DD')
    return parsed


def audit_periods(rows, cutoff='2025-11-03', excluded_dates=()):
    """Return validated copies; reject mislabeled periods and excluded dates.

    Cutoff belongs to post; excluded dates must be supplied from a verified
    trading calendar if needed. This is not a market-calendar validator.
    """
    threshold = canonical_day(cutoff)
    exclusions = {canonical_day(x) for x in excluded_dates}
    output = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('invalid row')
        day = canonical_day(row.get('date'))
        if day in exclusions:
            raise ValueError('excluded date present')
        expected = 'pre' if day < threshold else 'post'
        if row.get('period') != expected:
            raise ValueError('period disagrees with cutoff')
        output.append(dict(row))
    if not output:
        raise ValueError('empty rows')
    return output
