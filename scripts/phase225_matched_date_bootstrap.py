"""Matched-pair daily contrasts and circular date-block bootstrap (descriptive only)."""
from datetime import date
from math import isfinite
from random import Random

def matched_daily(rows, pairs, sessions, exchanges):
    if not pairs or not sessions or not exchanges: raise ValueError('nonempty inputs required')
    if len(set(sessions)) != len(sessions) or list(sessions) != sorted(sessions): raise ValueError('invalid sessions')
    if any(date.fromisoformat(d).isoformat() != d or d >= '2025-11-03' for d in sessions): raise ValueError('invalid dates')
    if len(set(exchanges)) != len(exchanges): raise ValueError('duplicate exchanges')
    if any(len(p) != 2 or p[0] == p[1] for p in pairs): raise ValueError('invalid pair')
    treated=[p[0] for p in pairs]; controls=[p[1] for p in pairs]
    if len(set(treated)) != len(treated) or len(set(controls)) != len(controls) or set(treated)&set(controls): raise ValueError('non-disjoint one-to-one matching required')
    allowed={(d,s,e) for d in sessions for p in pairs for s in p for e in exchanges}
    lookup={}
    for r in rows:
        if set(r) != {'date','security','exchange','hidden_count','total_count'}: raise ValueError('invalid schema')
        k=(r['date'],r['security'],r['exchange'])
        if k not in allowed or k in lookup: raise ValueError('unknown or duplicate key')
        h,n=r['hidden_count'],r['total_count']
        if type(h) is not int or type(n) is not int or not 0 <= h <= n or n == 0: raise ValueError('invalid counts')
        lookup[k]=h/n
    if set(lookup) != allowed: raise ValueError('incomplete matched panel')
    return [{'date':d,'matched_contrast':sum(lookup[d,t,e]-lookup[d,c,e] for t,c in pairs for e in exchanges)/(len(pairs)*len(exchanges))} for d in sessions]

def circular_block_window_bootstrap(daily, early_dates, late_dates, block_length, replicates, seed=0):
    if type(block_length) is not int or block_length < 1 or type(replicates) is not int or replicates < 2 or type(seed) is not int: raise ValueError('invalid parameters')
    dates=list(early_dates)+list(late_dates)
    if not early_dates or not late_dates or len(set(dates)) != len(dates) or dates != sorted(dates): raise ValueError('invalid windows')
    if [r['date'] for r in daily] != dates: raise ValueError('date mismatch')
    a=[r['matched_contrast'] for r in daily[:len(early_dates)]]
    b=[r['matched_contrast'] for r in daily[len(early_dates):]]
    if any(type(v) not in (int,float) or not isfinite(v) for v in a+b): raise ValueError('nonfinite contrast')
    if block_length > min(len(a),len(b)): raise ValueError('block too long')
    rng=Random(seed)
    def draw(xs):
        n=len(xs); out=[]
        while len(out)<n:
            start=rng.randrange(n)
            out.extend(xs[(start+j)%n] for j in range(block_length))
        return sum(out[:n])/n
    observed=sum(b)/len(b)-sum(a)/len(a)
    reps=sorted(draw(b)-draw(a) for _ in range(replicates))
    return {'observed_difference':observed,'bootstrap_mean':sum(reps)/replicates,'percentile_025':reps[int(.025*(replicates-1))],'percentile_975':reps[int(.975*(replicates-1))],'replicates':replicates,'block_length':block_length,'seed':seed,'source_authenticated':False,'calendar_authenticated':False,'treatment_authenticated':False,'causal_effect_established':False}
