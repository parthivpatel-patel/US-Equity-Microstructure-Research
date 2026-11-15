"""Calendar-aware placebo eligibility audit; does not authenticate market data."""
from datetime import date

def audit_placebo_calendar(observed_dates, placebo_dates, pre_sessions, post_sessions, forbidden_dates=()):
    """Audit exact session coverage around proposed placebo boundaries."""
    if type(pre_sessions) is not int or type(post_sessions) is not int or min(pre_sessions, post_sessions) <= 0:
        raise ValueError('session windows must be positive integers')
    observed, candidates, forbidden_seq = tuple(observed_dates), tuple(placebo_dates), tuple(forbidden_dates)
    forbidden = set(forbidden_seq)
    for seq in (observed, candidates, forbidden_seq):
        if any(type(d) is not date for d in seq):
            raise ValueError('dates must be datetime.date objects')
    if not observed or len(set(observed)) != len(observed) or len(set(candidates)) != len(candidates):
        raise ValueError('empty/duplicate observed dates or duplicate placebo dates')
    sessions = sorted(observed)
    results = []
    for boundary in candidates:
        pre = [d for d in sessions if d < boundary][-pre_sessions:]
        post = [d for d in sessions if d >= boundary][:post_sessions]
        reason = []
        if len(pre) != pre_sessions or len(post) != post_sessions:
            reason.append('insufficient_sessions')
        if any(d in forbidden for d in pre + post):
            reason.append('forbidden_session')
        results.append({'boundary': boundary.isoformat(), 'eligible': not reason,
                        'pre': tuple(d.isoformat() for d in pre),
                        'post': tuple(d.isoformat() for d in post),
                        'reasons': tuple(reason)})
    return {'candidates': len(results), 'eligible': sum(r['eligible'] for r in results),
            'results': tuple(results), 'source_authenticated': False,
            'treatment_authenticated': False}
