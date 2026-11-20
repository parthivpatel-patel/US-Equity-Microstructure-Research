"""Auditable decomposition of treatment/control date-support attrition.

Synthetic-fixture tested. Coverage diagnostics, not execution outcomes or causal effects.
"""
from datetime import date


def _date(s):
    if not isinstance(s, str) or len(s) != 10:
        raise ValueError('noncanonical date')
    try:
        d = date.fromisoformat(s)
    except ValueError as exc:
        raise ValueError('invalid date') from exc
    if d.isoformat() != s:
        raise ValueError('noncanonical date')
    return d


def support_attrition(rows, cutoff='2025-11-03'):
    """Return date counts and coverage for full versus common-group support.

    One row per exchange/date; count fields are nonnegative integers, observed <=
    eligible. Caller must independently authenticate the source and calendar.
    A common date requires both groups eligible, not necessarily observed.
    """
    threshold = _date(cutoff)
    seen = set()
    groups = {}
    for r in rows:
        if not isinstance(r, dict):
            raise ValueError('invalid row')
        try:
            exchange, raw = r['exchange'], r['date']
            counts = tuple(r[k] for k in ('treated_eligible','treated_observed','control_eligible','control_observed'))
        except KeyError as exc:
            raise ValueError('missing field') from exc
        day = _date(raw)
        if not isinstance(exchange, str) or not exchange.strip():
            raise ValueError('invalid exchange')
        if (exchange, day) in seen:
            raise ValueError('duplicate exchange-date')
        seen.add((exchange, day))
        te, to, ce, co = counts
        if any(type(v) is not int or v < 0 for v in counts) or to > te or co > ce or te + ce == 0:
            raise ValueError('invalid counts')
        if 'period' in r and r['period'] != ('pre' if day < threshold else 'post'):
            raise ValueError('mislabeled period')
        groups.setdefault((exchange, 'pre' if day < threshold else 'post'), []).append(counts)
    if not groups:
        raise ValueError('empty input')
    out = []
    for (exchange, period), cells in sorted(groups.items()):
        common = [c for c in cells if c[0] and c[2]]
        excluded = [c for c in cells if not (c[0] and c[2])]
        def coverage(subset, ei, oi):
            denom = sum(c[ei] for c in subset)
            return sum(c[oi] for c in subset) / denom if denom else None
        out.append({
            'exchange': exchange, 'period': period,
            'all_dates': len(cells), 'common_dates': len(common),
            'one_group_only_dates': len(excluded),
            'common_date_fraction': len(common) / len(cells),
            'treated_coverage_all': coverage(cells, 0, 1),
            'control_coverage_all': coverage(cells, 2, 3),
            'treated_coverage_common': coverage(common, 0, 1),
            'control_coverage_common': coverage(common, 2, 3),
            'treated_eligible_excluded': sum(c[0] for c in excluded),
            'control_eligible_excluded': sum(c[2] for c in excluded),
            'treated_observed_excluded': sum(c[1] for c in excluded),
            'control_observed_excluded': sum(c[3] for c in excluded),
        })
    return out
