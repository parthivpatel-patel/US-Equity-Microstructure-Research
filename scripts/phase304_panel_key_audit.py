"""Structural audit of security-date-exchange keys; no source authentication."""
from collections import Counter
from datetime import date

def audit_panel_keys(rows, expected_dates=None):
    if not isinstance(rows, list) or not rows:
        raise ValueError('rows must be a nonempty list')
    if expected_dates is not None and (not isinstance(expected_dates, list) or not expected_dates):
        raise ValueError('expected_dates must be a nonempty list when supplied')
    def parse_date(value):
        if type(value) is not str:
            raise ValueError('date must be a canonical ISO string')
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError('invalid date') from exc
        if parsed.isoformat() != value or parsed.weekday() >= 5:
            raise ValueError('noncanonical date or weekend')
        return value
    calendar = None
    if expected_dates is not None:
        calendar = [parse_date(x) for x in expected_dates]
        if calendar != sorted(set(calendar)):
            raise ValueError('expected calendar must be unique and sorted')
    keys = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('row must be a mapping')
        d = parse_date(row.get('date'))
        identifiers = []
        for field in ('security', 'exchange'):
            value = row.get(field)
            if type(value) is not str or not value or value != value.strip():
                raise ValueError(f'{field} must be a nonblank canonical string')
            identifiers.append(value)
        keys.append((identifiers[0], d, identifiers[1]))
    counts = Counter(keys)
    duplicates = sorted([{'security': s, 'date': d, 'exchange': e, 'count': n}
                         for (s, d, e), n in counts.items() if n > 1],
                        key=lambda x: (x['security'], x['date'], x['exchange']))
    by_pair = {}
    for security, d, exchange in counts:
        by_pair.setdefault((security, exchange), set()).add(d)
    missing = []
    extra = []
    if calendar is not None:
        expected = set(calendar)
        for (security, exchange), dates in sorted(by_pair.items()):
            for d in sorted(expected - dates):
                missing.append({'security': security, 'exchange': exchange, 'date': d})
            for d in sorted(dates - expected):
                extra.append({'security': security, 'exchange': exchange, 'date': d})
    return {
        'n_rows': len(rows), 'n_unique_keys': len(counts),
        'n_security_exchange_pairs': len(by_pair),
        'duplicate_keys': duplicates, 'missing_pair_dates': missing,
        'unexpected_pair_dates': extra,
        'structurally_consistent': not duplicates and not missing and not extra,
        'calendar_authenticated': False, 'source_authenticated': False,
        'panel_universe_authenticated': False, 'causal_inference_authorized': False,
        'coverage_scope': 'observed_security_exchange_pairs_only',
    }
