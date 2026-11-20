"""Fail-closed composition of Phase 502 date validation and Phase 501 coverage.

Descriptive audit only; does not authenticate SEC records or infer reform effects.
"""
from datetime import date
from collections import defaultdict


def _day(value):
    if not isinstance(value, str) or len(value) != 10:
        raise ValueError('noncanonical date')
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('invalid date') from exc
    if parsed.isoformat() != value:
        raise ValueError('noncanonical date')
    return parsed


def validated_coverage(rows, cutoff='2025-11-03', excluded_dates=()):
    """Aggregate common-date coverage only after validating every input row.

    Cutoff is assigned to post. Exclusions are caller-supplied, not an
    authenticated trading calendar. Returns per-exchange-period diagnostics.
    """
    threshold = _day(cutoff)
    exclusions = {_day(x) for x in excluded_dates}
    groups = defaultdict(list)
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('invalid row')
        try:
            exchange, raw_day, period = (row[k] for k in ('exchange', 'date', 'period'))
            te, to, ce, co = (row[k] for k in ('treated_eligible', 'treated_observed', 'control_eligible', 'control_observed'))
        except KeyError as exc:
            raise ValueError('missing field') from exc
        day = _day(raw_day)
        if day in exclusions:
            raise ValueError('excluded date')
        if period != ('pre' if day < threshold else 'post'):
            raise ValueError('mislabeled period')
        if not isinstance(exchange, str) or not exchange.strip():
            raise ValueError('invalid exchange')
        if (exchange, day) in seen:
            raise ValueError('duplicate exchange-date')
        seen.add((exchange, day))
        if any(type(x) is not int or x < 0 for x in (te, to, ce, co)) or to > te or co > ce or te + ce == 0:
            raise ValueError('invalid counts')
        groups[(exchange, period)].append((te, to, ce, co))
    if not groups:
        raise ValueError('empty input')
    output = []
    for (exchange, period), cells in sorted(groups.items()):
        both = [c for c in cells if c[0] > 0 and c[2] > 0]
        sums = [sum(c[i] for c in cells) for i in range(4)]
        equal_gap = weighted_gap = None
        if both:
            equal_gap = sum(to / te - co / ce for te, to, ce, co in both) / len(both)
            weighted_gap = (sum(c[1] for c in both) / sum(c[0] for c in both)
                            - sum(c[3] for c in both) / sum(c[2] for c in both))
        output.append({'exchange': exchange, 'period': period,
                       'eligible_dates': len(cells), 'common_support_dates': len(both),
                       'excluded_dates': len(cells) - len(both),
                       'treated_coverage_all': sums[1] / sums[0] if sums[0] else None,
                       'control_coverage_all': sums[3] / sums[2] if sums[2] else None,
                       'common_date_equal_weight_gap': equal_gap,
                       'common_date_eligible_weight_gap': weighted_gap,
                       'common_date_gap_weighting_difference': equal_gap - weighted_gap if both else None})
    return output
