"""Fail-closed security-date-exchange panel and treatment roster integrity audit.

No source authentication or causal inference is performed here.
"""
from collections import Counter
from datetime import date


def canonical_day(value):
    if not isinstance(value, str) or len(value) != 10:
        raise ValueError('noncanonical date')
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('invalid date') from exc
    if parsed.isoformat() != value:
        raise ValueError('noncanonical date')
    return parsed


def audit_panel(rows, roster, *, allowed_dates=None, allowed_exchanges=None):
    """Audit unique keys, roster membership, stable group labels, and optional allowlists.

    rows: dicts with security/date/exchange/group. roster: mapping security ->
    treated/control. The roster is supplied externally and NOT authenticated.
    Repeated security-date on distinct exchanges is valid. Duplicate exact
    security-date-exchange keys are invalid. Returns descriptive counts only.
    """
    if not isinstance(roster, dict) or not roster:
        raise ValueError('missing roster')
    for sec, group in roster.items():
        if not isinstance(sec, str) or not sec.strip() or group not in ('treated', 'control'):
            raise ValueError('invalid roster')
    dates = None if allowed_dates is None else {canonical_day(d) for d in allowed_dates}
    exchanges = None if allowed_exchanges is None else set(allowed_exchanges)
    if exchanges is not None and (not exchanges or any(not isinstance(e, str) or not e.strip() for e in exchanges)):
        raise ValueError('invalid exchanges allowlist')
    seen = set()
    observed = Counter()
    daily = Counter()
    n = 0
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('invalid row')
        try:
            sec, day, ex, group = (row[k] for k in ('security', 'date', 'exchange', 'group'))
        except KeyError as exc:
            raise ValueError('missing field') from exc
        day = canonical_day(day)
        if not isinstance(sec, str) or not sec.strip() or sec not in roster:
            raise ValueError('unknown security')
        if not isinstance(ex, str) or not ex.strip():
            raise ValueError('invalid exchange')
        if group != roster[sec]:
            raise ValueError('group mismatch')
        if dates is not None and day not in dates:
            raise ValueError('date not allowed')
        if exchanges is not None and ex not in exchanges:
            raise ValueError('exchange not allowed')
        key = (sec, day, ex)
        if key in seen:
            raise ValueError('duplicate panel key')
        seen.add(key)
        observed[group] += 1
        daily[(day.isoformat(), ex, group)] += 1
        n += 1
    if not n:
        raise ValueError('empty panel')
    return {'rows': n, 'distinct_securities': len({k[0] for k in seen}),
            'distinct_dates': len({k[1] for k in seen}),
            'distinct_exchanges': len({k[2] for k in seen}),
            'treated_rows': observed['treated'], 'control_rows': observed['control'],
            'daily_exchange_group_counts': [
                {'date': d, 'exchange': ex, 'group': group, 'rows': count}
                for (d, ex, group), count in sorted(daily.items())]}
