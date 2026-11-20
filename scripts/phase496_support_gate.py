"""Admission gate for group/date support; constructed or authenticated rows only."""
from collections import defaultdict
from datetime import date


def support_gate(eligibility, observations, treatment, cutoff, min_common_each_side=1):
    """Inputs: iterable (security, exchange, ISO date); treatment maps security to 0/1.

    Returns coverage and common dates; does not estimate treatment effects.
    """
    try:
        boundary = date.fromisoformat(cutoff)
    except (TypeError, ValueError) as exc:
        raise ValueError('invalid cutoff') from exc
    if not isinstance(min_common_each_side, int) or isinstance(min_common_each_side, bool) or min_common_each_side < 1:
        raise ValueError('invalid minimum support')
    def validate(rows):
        result = set()
        for key in rows:
            if not isinstance(key, (tuple, list)) or len(key) != 3:
                raise ValueError('invalid key')
            sec, ex, day = key
            if not all(isinstance(v, str) and v.strip() for v in key):
                raise ValueError('invalid key')
            try:
                parsed = date.fromisoformat(day)
            except ValueError as exc:
                raise ValueError('invalid date') from exc
            if parsed.isoformat() != day:
                raise ValueError('noncanonical date')
            k = (sec, ex, day)
            if k in result:
                raise ValueError('duplicate key')
            result.add(k)
        return result
    eligible = validate(eligibility)
    observed = validate(observations)
    if not eligible or observed - eligible:
        raise ValueError('empty eligibility or out-of-universe observation')
    units = defaultdict(set)
    seen = defaultdict(set)
    for sec, ex, day in eligible:
        if sec not in treatment or type(treatment[sec]) not in (int, bool) or treatment[sec] not in (0, 1):
            raise ValueError('missing or invalid treatment label')
        units[(sec, ex)].add(day)
    for sec, ex, day in observed:
        seen[(sec, ex)].add(day)
    by_exchange = defaultdict(lambda: {0: [], 1: []})
    for unit, dates in units.items():
        if any(d < cutoff for d in dates) and any(d >= cutoff for d in dates):
            by_exchange[unit[1]][int(treatment[unit[0]])].append(unit)
    details = {}
    for ex, groups in sorted(by_exchange.items()):
        if not groups[0] or not groups[1]:
            details[ex] = {'admitted': False, 'reason': 'missing two-sided eligible treatment/control group'}
            continue
        all_units = groups[0] + groups[1]
        complete = [u for u in all_units if units[u] == seen[u]]
        intersection = set.intersection(*(seen[u] for u in all_units))
        pre = sorted(d for d in intersection if d < cutoff)
        post = sorted(d for d in intersection if d >= cutoff)
        details[ex] = {'admitted': len(complete) == len(all_units) and len(pre) >= min_common_each_side and len(post) >= min_common_each_side,
                       'eligible_units': len(all_units), 'fully_covered_units': len(complete),
                       'common_pre_dates': pre, 'common_post_dates': post,
                       'reason': 'pass' if len(complete) == len(all_units) and len(pre) >= min_common_each_side and len(post) >= min_common_each_side else 'incomplete coverage or common-date support'}
    return {'provenance_status': 'UNAUTHENTICATED_UNLESS_EXTERNALLY_VERIFIED', 'cutoff': boundary.isoformat(),
            'minimum_common_dates_each_side': min_common_each_side, 'exchanges': details,
            'admitted_exchanges': [ex for ex, r in details.items() if r['admitted']]}
