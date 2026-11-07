"""Fail-closed pre-reform security/exchange panel audit; no historical authentication."""
from datetime import date

REFORM = '2025-11-03'

def audit_panel(rows, sessions, treated, controls, exchanges):
    """Require complete security x exchange x session cells; never impute zeros."""
    if not isinstance(rows, (list, tuple)) or not rows:
        raise ValueError('nonempty panel required')
    def unique_nonempty(items, label):
        if not isinstance(items, (list, tuple)) or not items or any(type(x) is not str or not x.strip() for x in items) or len(set(items)) != len(items):
            raise ValueError('invalid '+label)
        return tuple(items)
    ss = unique_nonempty(sessions, 'sessions')
    if any(date.fromisoformat(d).isoformat() != d for d in ss) or tuple(sorted(ss)) != ss or ss[-1] >= REFORM:
        raise ValueError('invalid pre-reform sessions')
    tt = unique_nonempty(treated, 'treated')
    cc = unique_nonempty(controls, 'controls')
    ee = unique_nonempty(exchanges, 'exchanges')
    if set(tt) & set(cc):
        raise ValueError('treatment/control overlap')
    allowed = {(d,s,e) for d in ss for s in tt+cc for e in ee}
    seen = set()
    for row in rows:
        if type(row) is not dict or set(row) != {'date','security','exchange','hidden_count','total_count'}:
            raise ValueError('unexpected row schema')
        key = (row['date'],row['security'],row['exchange'])
        if key not in allowed or key in seen:
            raise ValueError('unknown or duplicate panel key')
        seen.add(key)
        h,n = row['hidden_count'],row['total_count']
        if type(h) is not int or type(n) is not int or h < 0 or n <= 0 or h > n:
            raise ValueError('invalid count denominators')
    missing = allowed - seen
    if missing:
        raise ValueError(f'incomplete panel: {len(missing)} missing cells')
    return {'sessions':len(ss),'treated':len(tt),'controls':len(cc),'exchanges':len(ee),
            'cells':len(seen),'complete_rectangular_panel':True,
            'calendar_authenticated':False,'source_authenticated':False,
            'treatment_authenticated':False,'causal_effect_established':False}
