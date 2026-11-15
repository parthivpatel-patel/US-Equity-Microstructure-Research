"""Exact balanced matched-pair/date contrast; no inference or causal interpretation."""
from fractions import Fraction

def contrast(rows, pre_dates, post_dates):
    """Rows: (pair_id, date, arm, numerator, denominator), arm T or C."""
    pre, post = tuple(pre_dates), tuple(post_dates)
    if not pre or not post or len(set(pre)) != len(pre) or len(set(post)) != len(post):
        raise ValueError('invalid date window')
    if set(pre) & set(post):
        raise ValueError('overlapping windows')
    dates = set(pre) | set(post)
    panel = {}
    pairs = set()
    for pair, date, arm, num, den in rows:
        if not isinstance(pair, str) or not pair or date not in dates or arm not in ('T', 'C'):
            raise ValueError('invalid key')
        if type(num) is not int or type(den) is not int or den <= 0 or not 0 <= num <= den:
            raise ValueError('invalid numerator/denominator')
        key = (pair, date, arm)
        if key in panel:
            raise ValueError('duplicate observation')
        panel[key] = Fraction(num, den)
        pairs.add(pair)
    if not pairs:
        raise ValueError('empty panel')
    if len(panel) != len(pairs) * len(dates) * 2:
        raise ValueError('unbalanced panel')
    for pair in pairs:
        for date in dates:
            if (pair, date, 'T') not in panel or (pair, date, 'C') not in panel:
                raise ValueError('missing matched observation')
    per_pair = {}
    for pair in sorted(pairs):
        def mean_gap(window):
            return sum((panel[pair, d, 'T'] - panel[pair, d, 'C'] for d in window), Fraction()) / len(window)
        per_pair[pair] = mean_gap(post) - mean_gap(pre)
    estimate = sum(per_pair.values(), Fraction()) / len(per_pair)
    return {'estimate': estimate, 'per_pair': per_pair, 'pairs': len(pairs),
            'pre_dates': len(pre), 'post_dates': len(post),
            'source_authenticated': False, 'treatment_authenticated': False}
