"""Uncorrected equal-group-weighted two-way cluster covariance diagnostic."""
from collections import Counter, defaultdict
from datetime import date
from math import isfinite

def weighted_components(rows):
    rows=list(rows)
    if not rows: raise ValueError('empty input')
    seen=set(); counts=Counter()
    for group,day,value in rows:
        if not isinstance(group,str) or not group.strip(): raise ValueError('invalid group')
        if not isinstance(day,str) or date.fromisoformat(day).isoformat()!=day: raise ValueError('invalid ISO date')
        if not isinstance(value,(float,int)) or not isfinite(value): raise ValueError('invalid contrast')
        if (group,day) in seen: raise ValueError('duplicate group-date; aggregate exchanges first')
        seen.add((group,day)); counts[group]+=1
    G=len(counts); D=len({d for _,d,_ in rows})
    if G<2 or D<2: raise ValueError('requires at least two groups and two dates')
    weights=[(g,d,1/(G*counts[g]),float(y)) for g,d,y in rows]
    mean=sum(w*y for _,_,w,y in weights)
    scores=[(g,d,w*(y-mean)) for g,d,w,y in weights]
    def meat(kind):
        sums=defaultdict(float)
        for g,d,s in scores:
            key=g if kind=='group' else d if kind=='date' else (g,d)
            sums[key]+=s
        return sum(s*s for s in sums.values())
    vg,vd,vi=(meat(k) for k in ('group','date','intersection'))
    return dict(groups=G,dates=D,cells=len(rows),equal_group_mean_pp=mean,
                group_component=vg,date_component=vd,intersection_component=vi,
                two_way_raw_variance=vg+vd-vi,nonnegative_variance_certified=vg+vd-vi>=0,
                status='UNCORRECTED_DESCRIPTIVE_DIAGNOSTIC_NO_CI')
