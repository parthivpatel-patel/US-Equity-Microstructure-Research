"""Balanced matched-pair/date/exchange contrast; descriptive, not causal."""
from fractions import Fraction

def exchange_contrast(rows, pre_dates, post_dates):
    """Rows: (pair, date, exchange, arm, hidden, total); exact integer counts."""
    pre, post = tuple(pre_dates), tuple(post_dates)
    if not pre or not post or len(pre) != len(set(pre)) or len(post) != len(set(post)) or set(pre) & set(post):
        raise ValueError('invalid windows')
    dates = set(pre) | set(post)
    panel = {}
    pairs, exchanges = set(), set()
    for pair, date, exchange, arm, hidden, total in rows:
        if not isinstance(pair, str) or not pair or not isinstance(exchange, str) or not exchange or date not in dates or arm not in ('T', 'C'):
            raise ValueError('invalid keys')
        if type(hidden) is not int or type(total) is not int or total <= 0 or not 0 <= hidden <= total:
            raise ValueError('invalid counts')
        key = (pair, date, exchange, arm)
        if key in panel:
            raise ValueError('duplicate')
        panel[key] = Fraction(hidden, total)
        pairs.add(pair)
        exchanges.add(exchange)
    if not pairs or not exchanges:
        raise ValueError('empty panel')
    if len(panel) != len(pairs) * len(dates) * len(exchanges) * 2:
        raise ValueError('unbalanced panel')
    for p in pairs:
        for d in dates:
            for e in exchanges:
                if (p,d,e,'T') not in panel or (p,d,e,'C') not in panel:
                    raise ValueError('missing arm')
    by_exchange = {}
    by_pair_exchange = {}
    for e in sorted(exchanges):
        effects = []
        for p in sorted(pairs):
            def gap(window):
                return sum((panel[p,d,e,'T'] - panel[p,d,e,'C'] for d in window), Fraction()) / len(window)
            effect = gap(post) - gap(pre)
            by_pair_exchange[(p,e)] = effect
            effects.append(effect)
        by_exchange[e] = sum(effects, Fraction()) / len(effects)
    overall = sum(by_exchange.values(), Fraction()) / len(by_exchange)
    return {'estimate':overall, 'by_exchange':by_exchange, 'by_pair_exchange':by_pair_exchange,
            'pairs':len(pairs), 'exchanges':len(exchanges), 'source_authenticated':False,
            'treatment_authenticated':False}
