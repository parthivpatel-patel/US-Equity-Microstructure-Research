"""Fail-closed structural admission for descriptive date-level HAC inputs."""
from datetime import date
from math import isfinite

def audit_hac_input(rows, lags, *, min_sessions=20, max_lag_fraction=0.25):
    """Validate session support and predeclared lag grid; never authenticate data."""
    if type(min_sessions) is not int or min_sessions < 2:
        raise ValueError('invalid minimum sessions')
    if type(max_lag_fraction) not in (int, float) or not (0 < max_lag_fraction < 1):
        raise ValueError('invalid lag fraction')
    rows = list(rows)
    if len(rows) < min_sessions:
        raise ValueError('insufficient sessions')
    ds = []
    for r in rows:
        if type(r.get('date')) is not str:
            raise ValueError('invalid date')
        d = date.fromisoformat(r['date'])
        if d.isoformat() != r['date'] or d.weekday() >= 5:
            raise ValueError('noncanonical or weekend date')
        if type(r.get('contrast')) not in (float, int) or not isfinite(r['contrast']):
            raise ValueError('invalid contrast')
        ds.append(d)
    if ds != sorted(set(ds)):
        raise ValueError('dates not unique and sorted')
    ls = list(lags)
    if not ls or any(type(l) is not int or l < 0 or l > int((len(rows)-1)*max_lag_fraction) for l in ls) or len(set(ls)) != len(ls):
        raise ValueError('lag grid inadmissible')
    return {'admitted':True,'n_sessions':len(rows),'first_date':ds[0].isoformat(),
            'last_date':ds[-1].isoformat(),'lags':ls,'max_lag_fraction':max_lag_fraction,
            'source_authenticated':False,'treatment_authenticated':False,
            'warning':'Admission is a structural check only; calendar coverage, sampling, causal identification and inferential validity are not verified.'}
