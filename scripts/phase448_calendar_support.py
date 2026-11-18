"""Fail-closed common-date support audit. Does not authenticate SEC provenance."""
from collections import defaultdict
from datetime import date

def audit(rows, *, reform_date='2025-11-03', placebo_date='2025-10-01', min_pre_dates=2, min_post_dates=2):
    reform, placebo = date.fromisoformat(reform_date), date.fromisoformat(placebo_date)
    if not placebo < reform or min_pre_dates < 1 or min_post_dates < 1:
        raise ValueError('invalid calendar parameters')
    seen = set()
    cells = defaultdict(lambda: defaultdict(set))
    n = 0
    for row in rows:
        n += 1
        d = date.fromisoformat(row['date'])
        security, exchange, group = (row[k] for k in ('security', 'exchange', 'matched_group'))
        if not all(isinstance(v, str) and v.strip() for v in (security, exchange, group)):
            raise ValueError('empty or invalid identifier')
        treated = row['treated']
        if type(treated) is not bool:
            raise ValueError('treated must be Boolean')
        key = (d, security, exchange)
        if key in seen:
            raise ValueError('duplicate security-date-exchange')
        seen.add(key)
        cells[(exchange, group)][d].add(treated)
    if not n:
        raise ValueError('empty input')
    result = []
    for (exchange, group), days in sorted(cells.items()):
        common = sorted(d for d, arms in days.items() if arms == {True, False})
        sep = sum(d.month == 9 and d.year == 2025 for d in common)
        octo = sum(d.month == 10 and d.year == 2025 for d in common)
        placebo_pre = sum(d < placebo for d in common)
        placebo_post = sum(placebo <= d < reform for d in common)
        reform_pre = sum(d < reform for d in common)
        reform_post = sum(d >= reform for d in common)
        result.append({'exchange': exchange, 'matched_group': group,
                       'common_dates': len(common), 'september_common_dates': sep,
                       'october_common_dates': octo,
                       'placebo_pre_common_dates': placebo_pre,
                       'placebo_post_common_dates': placebo_post,
                       'reform_pre_common_dates': reform_pre,
                       'reform_post_common_dates': reform_post,
                       'placebo_supported': placebo_pre >= min_pre_dates and placebo_post >= min_post_dates,
                       'reform_supported': reform_pre >= min_pre_dates and reform_post >= min_post_dates})
    return {'observation_count': n, 'strata': result,
            'all_strata_placebo_supported': all(x['placebo_supported'] for x in result),
            'all_strata_reform_supported': all(x['reform_supported'] for x in result),
            'source_authenticated': False, 'effect_estimated': False}
