"""Roster-anchored attrition audit; inputs are not authenticated."""
from fractions import Fraction

def audit_roster_attrition(rows, roster, pre_dates, post_dates):
    pre, post = tuple(pre_dates), tuple(post_dates)
    if not pre or not post or len(set(pre)) != len(pre) or len(set(post)) != len(post) or set(pre) & set(post):
        raise ValueError('invalid dates')
    dates = set(pre) | set(post)
    roster = tuple(roster)
    if not roster or len(set(roster)) != len(roster):
        raise ValueError('empty or duplicate roster')
    for entry in roster:
        if not isinstance(entry, tuple) or len(entry) != 2 or any(not isinstance(v, str) or not v for v in entry):
            raise ValueError('invalid roster entry')
    expected = {(p, d, e, arm) for p, e in roster for d in dates for arm in ('T', 'C')}
    observed = set()
    for p, d, e, arm, hidden, total in rows:
        key = (p, d, e, arm)
        if key not in expected or key in observed:
            raise ValueError('unexpected or duplicate observation')
        if type(hidden) is not int or type(total) is not int or total <= 0 or not 0 <= hidden <= total:
            raise ValueError('invalid counts')
        observed.add(key)
    missing = expected - observed
    by_exchange = {}
    for e in sorted({e for _, e in roster}):
        entries = [(p, e) for p, ex in roster if ex == e]
        complete = sum(all((p, d, e, arm) in observed for d in dates for arm in ('T', 'C')) for p, _ in entries)
        by_exchange[e] = {'candidate_pair_exchanges': len(entries), 'complete_pair_exchanges': complete,
                          'retention': Fraction(complete, len(entries))}
    return {'expected_rows': len(expected), 'observed_rows': len(observed),
            'missing_keys': tuple(sorted(missing)), 'by_exchange': by_exchange,
            'source_authenticated': False, 'roster_authenticated': False,
            'treatment_authenticated': False}
