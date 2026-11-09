"""Fixed-roster daily matched-contrast pretrend audit. Descriptive, not causal inference."""
from datetime import date
from math import isfinite

def audit(rows, cutoff, min_pre=4):
    """Rows: date ISO, pair_id, treated, control. Equal pair weights."""
    cut = date.fromisoformat(cutoff)
    if type(min_pre) is not int or min_pre < 4:
        raise ValueError('min_pre must be integer >=4')
    by_date = {}
    seen = set()
    for row in rows:
        d = date.fromisoformat(row['date'])
        pair = row['pair_id']
        if not isinstance(pair, str) or not pair:
            raise ValueError('invalid pair id')
        key = (d, pair)
        if key in seen:
            raise ValueError('duplicate date-pair')
        seen.add(key)
        t, c = row['treated'], row['control']
        if any(type(v) not in (int, float) or not isfinite(v) for v in (t,c)):
            raise ValueError('nonfinite/non-numeric outcomes')
        by_date.setdefault(d, {})[pair] = t-c
    dates = sorted(by_date)
    pre = [d for d in dates if d < cut]
    post = [d for d in dates if d >= cut]
    if len(pre) < min_pre or not post:
        raise ValueError('insufficient pre/post dates')
    roster = set(by_date[dates[0]])
    if not roster or any(set(by_date[d]) != roster for d in dates):
        raise ValueError('unbalanced or changing pair roster')
    if any(d.weekday() >= 5 for d in dates):
        raise ValueError('weekend date: authenticate trading calendar')
    daily = [sum(by_date[d].values())/len(roster) for d in dates]
    pre_y = daily[:len(pre)]
    x = list(range(len(pre)))
    mx = sum(x)/len(x)
    my = sum(pre_y)/len(pre_y)
    slope = sum((a-mx)*(b-my) for a,b in zip(x,pre_y))/sum((a-mx)**2 for a in x)
    mid = len(pre)//2
    drift = sum(pre_y[mid:])/len(pre_y[mid:])-sum(pre_y[:mid])/mid
    post_mean = sum(daily[len(pre):])/len(post)
    return {'n_pairs':len(roster),'n_pre_dates':len(pre),'n_post_dates':len(post),
            'pre_slope_per_observed_session':slope,
            'pre_late_minus_early':drift,
            'post_minus_pre':post_mean-my,
            'daily':[{'date':d.isoformat(),'mean_pair_contrast':v} for d,v in zip(dates,daily)],
            'interpretation':'descriptive only; no source authentication, calendar authentication or valid inference'}
