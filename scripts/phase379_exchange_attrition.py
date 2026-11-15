"""Audit exchange-stratified matched-pair complete-case attrition; no imputation."""
from fractions import Fraction

def audit_attrition(rows, pre_dates, post_dates):
    """Rows: (pair,date,exchange,arm,hidden,total); exact counts only."""
    pre, post = tuple(pre_dates), tuple(post_dates)
    if not pre or not post or len(set(pre)) != len(pre) or len(set(post)) != len(post) or set(pre) & set(post):
        raise ValueError('invalid windows')
    dates = set(pre) | set(post)
    observed, pairs, exchanges = set(), set(), set()
    for pair, date, exchange, arm, hidden, total in rows:
        if not isinstance(pair,str) or not pair or not isinstance(exchange,str) or not exchange or date not in dates or arm not in ('T','C'):
            raise ValueError('invalid keys')
        if type(hidden) is not int or type(total) is not int or total <= 0 or not 0 <= hidden <= total:
            raise ValueError('invalid counts')
        key = (pair,date,exchange,arm)
        if key in observed:
            raise ValueError('duplicate observation')
        observed.add(key)
        pairs.add(pair)
        exchanges.add(exchange)
    if not observed:
        raise ValueError('empty panel')
    by_exchange, missing, complete_cells = {}, [], []
    for e in sorted(exchanges):
        complete = 0
        for p in sorted(pairs):
            expected = {(p,d,e,a) for d in dates for a in ('T','C')}
            absent = expected - observed
            missing.extend(sorted(absent))
            if not absent:
                complete += 1
                complete_cells.append((p,e))
        by_exchange[e] = {'complete_pairs':complete,'candidate_pairs':len(pairs),
                          'retention':Fraction(complete,len(pairs))}
    return {'pairs':len(pairs),'exchanges':len(exchanges),'observed_rows':len(observed),
            'expected_rows':len(pairs)*len(exchanges)*len(dates)*2,
            'complete_pair_exchanges':tuple(complete_cells),'missing_keys':tuple(missing),
            'by_exchange':by_exchange,'source_authenticated':False,'treatment_authenticated':False}
