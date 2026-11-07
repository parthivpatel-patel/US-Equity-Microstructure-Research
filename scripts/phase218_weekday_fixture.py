"""Construct a weekend-free pre-reform synthetic fixture; NOT an exchange calendar."""
from datetime import date, timedelta


def weekday_fixture(start='2025-09-02', count=24):
    if type(count) is not int or count < 12:
        raise ValueError('at least 12 sessions required')
    first = date.fromisoformat(start)
    if first >= date(2025, 11, 3):
        raise ValueError('must begin before reform')
    days = []
    current = first
    while len(days) < count:
        if current >= date(2025, 11, 3):
            raise ValueError('fixture would cross reform')
        if current.weekday() < 5:
            days.append(current.isoformat())
        current += timedelta(days=1)
    rows = [{'date': day, 'contrast': float(i % 4 + 3 * (i >= count // 2))}
            for i, day in enumerate(days)]
    early = (days[0], days[9])
    late = (days[-10], days[-1])
    return rows, days, early, late
