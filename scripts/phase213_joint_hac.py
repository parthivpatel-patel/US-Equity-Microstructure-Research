"""Joint-window HAC for descriptive pre-reform contrasts; no causal inference."""
from datetime import date
from math import isfinite, sqrt

REFORM = '2025-11-03'

def joint_window_hac(observations, early, late, lags=(0, 1, 3), min_per_window=5):
    rows = list(observations)
    if not rows or type(min_per_window) is not int or min_per_window < 2:
        raise ValueError('empty series or invalid minimum')
    dates, ys = [], []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'date', 'contrast'}:
            raise ValueError('invalid observation')
        d, y = row['date'], row['contrast']
        if type(d) is not str or date.fromisoformat(d).isoformat() != d or type(y) not in (int, float) or not isfinite(y):
            raise ValueError('invalid observation value')
        dates.append(d)
        ys.append(float(y))
    if dates != sorted(set(dates)) or dates[-1] >= REFORM:
        raise ValueError('dates must be unique, sorted, pre-reform')
    def indices(window):
        if not isinstance(window, (tuple, list)) or len(window) != 2:
            raise ValueError('invalid window')
        a, b = window
        if a not in dates or b not in dates or a > b:
            raise ValueError('window boundary not observed')
        result = list(range(dates.index(a), dates.index(b) + 1))
        if len(result) < min_per_window:
            raise ValueError('insufficient observations')
        return result
    e, l = indices(early), indices(late)
    if e[-1] >= l[0]:
        raise ValueError('windows overlap or reversed')
    if not isinstance(lags, (tuple, list)) or not lags or any(type(k) is not int or k < 0 or k >= len(rows) for k in lags):
        raise ValueError('invalid lags')
    me = sum(ys[i] for i in e) / len(e)
    ml = sum(ys[i] for i in l) / len(l)
    scores = [0.0] * len(rows)
    for i in e:
        scores[i] = -(ys[i] - me) / len(e)
    for i in l:
        scores[i] = (ys[i] - ml) / len(l)
    results = {}
    for lag in lags:
        variance = sum(s*s for s in scores)
        for k in range(1, lag + 1):
            variance += 2*(1-k/(lag+1))*sum(scores[t]*scores[t-k] for t in range(k, len(scores)))
        if variance < -1e-10:
            raise ValueError('negative HAC variance')
        results[lag] = sqrt(max(0.0, variance))
    return {'early_mean': me, 'late_mean': ml, 'late_minus_early': ml-me,
            'early_n': len(e), 'late_n': len(l), 'hac_standard_errors': results,
            'source_authenticated': False, 'treatment_authenticated': False,
            'causal_effect_established': False}
