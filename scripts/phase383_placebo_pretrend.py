"""Exact matched-pair pretrend and placebo-window diagnostic; not causal inference."""
from fractions import Fraction
from datetime import date


def audit_matched_pretrend(rows, pairs, windows):
    """Compute equal-pair common-date changes and exact pre-window linear trends.

    rows: (pair_id, side in {'T','C'}, ISO date, numerator, denominator).
    windows: (label, pre_dates, post_dates), each an iterable of ISO dates.
    No extrapolation or standard errors. A missing pair-date-side fails closed.
    """
    pairs = tuple(pairs)
    if not pairs or len(set(pairs)) != len(pairs):
        raise ValueError('pairs must be unique and nonempty')
    data = {}
    for pair, side, day, num, den in rows:
        if pair not in pairs or side not in ('T', 'C'):
            raise ValueError('unknown pair or side')
        try:
            if date.fromisoformat(day).isoformat() != day:
                raise ValueError('noncanonical date')
        except (TypeError, ValueError) as exc:
            raise ValueError('invalid date') from exc
        if type(num) is not int or type(den) is not int or den <= 0 or num < 0 or num > den:
            raise ValueError('invalid count')
        key = (pair, side, day)
        if key in data:
            raise ValueError('duplicate row')
        data[key] = Fraction(num, den)
    output = []
    labels = set()
    for label, pre, post in windows:
        pre, post = tuple(pre), tuple(post)
        if label in labels or not pre or not post or len(set(pre + post)) != len(pre) + len(post):
            raise ValueError('invalid window')
        labels.add(label)
        for dates in (pre, post):
            if tuple(sorted(dates)) != dates or len(set(dates)) != len(dates):
                raise ValueError('unordered window dates')
            for day in dates:
                try:
                    if date.fromisoformat(day).isoformat() != day:
                        raise ValueError('invalid date')
                except (TypeError, ValueError) as exc:
                    raise ValueError('invalid window date') from exc
        if pre[-1] >= post[0] or len(pre) < 2:
            raise ValueError('window order or pretrend length invalid')
        pair_effects, pair_slopes = [], []
        for pair in pairs:
            def diff(day):
                try:
                    return data[(pair, 'T', day)] - data[(pair, 'C', day)]
                except KeyError as exc:
                    raise ValueError('missing matched observation') from exc
            before, after = [diff(d) for d in pre], [diff(d) for d in post]
            pair_effects.append(sum(after, Fraction()) / len(after) - sum(before, Fraction()) / len(before))
            x = [(date.fromisoformat(d) - date.fromisoformat(pre[0])).days for d in pre]
            xbar = Fraction(sum(x), len(x))
            ybar = sum(before, Fraction()) / len(before)
            denominator = sum(((Fraction(t) - xbar) ** 2 for t in x), Fraction())
            pair_slopes.append(sum(((Fraction(t) - xbar) * (v - ybar) for t, v in zip(x, before)), Fraction()) / denominator)
        output.append({'label': label, 'pairs': len(pairs), 'contrast': sum(pair_effects, Fraction()) / len(pairs),
                       'pretrend_slope_per_calendar_day': sum(pair_slopes, Fraction()) / len(pairs),
                       'pair_contrasts': tuple(pair_effects), 'pair_slopes': tuple(pair_slopes)})
    return {'windows': tuple(output), 'source_authenticated': False, 'treatment_authenticated': False,
            'causal_identification_established': False, 'inference_performed': False}
