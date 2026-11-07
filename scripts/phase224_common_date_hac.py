"""Descriptive common-date early/late contrasts with full-series Bartlett HAC.

Requires daily contrasts from an admitted fixed-roster panel; does not authenticate
the underlying calendar, SEC observations, or treatment classification.
"""
from math import sqrt, isfinite

def common_date_hac(daily, early_dates, late_dates, bandwidth):
    if type(bandwidth) is not int or bandwidth < 0:
        raise ValueError('invalid bandwidth')
    if not isinstance(daily, list) or not daily:
        raise ValueError('nonempty daily records required')
    if not isinstance(early_dates, (list, tuple)) or not isinstance(late_dates, (list, tuple)) or not early_dates or not late_dates:
        raise ValueError('two nonempty date windows required')
    dates = list(early_dates) + list(late_dates)
    if len(set(dates)) != len(dates) or dates != sorted(dates) or [r.get('date') for r in daily] != dates:
        raise ValueError('dates must be unique, ordered, and match supplied records')
    n0, n1 = len(early_dates), len(late_dates)
    n = n0 + n1
    if bandwidth >= n:
        raise ValueError('bandwidth must be smaller than sample')
    out = {'early_n':n0, 'late_n':n1, 'bandwidth':bandwidth,
           'calendar_authenticated':False, 'source_authenticated':False,
           'treatment_authenticated':False, 'causal_effect_established':False}
    for key in ('equal_cell_contrast','pooled_count_contrast'):
        values = []
        for row in daily:
            v = row.get(key)
            if type(v) not in (int,float) or not isfinite(v):
                raise ValueError('invalid daily contrast')
            values.append(float(v))
        a = sum(values[:n0])/n0
        b = sum(values[n0:])/n1
        residuals = [v-a for v in values[:n0]] + [v-b for v in values[n0:]]
        scores = [-u/n0 for u in residuals[:n0]] + [u/n1 for u in residuals[n0:]]
        variance = sum(s*s for s in scores)
        for lag in range(1,bandwidth+1):
            variance += 2*(1-lag/(bandwidth+1))*sum(scores[t]*scores[t-lag] for t in range(lag,n))
        if variance < -1e-12:
            raise ArithmeticError('negative HAC variance')
        out[key] = {'early_mean':a, 'late_mean':b, 'difference':b-a,
                    'hac_variance':max(0.0,variance),
                    'hac_se':sqrt(max(0.0,variance))}
    out['interpretation']='descriptive pre-reform window comparison; no causal identification'
    return out
