"""Calendar-indexed descriptive lag diagnostic. No calibrated confidence intervals."""
from collections import Counter, defaultdict
from datetime import date
from math import isfinite

def calendar_serial_components(rows, sessions, max_lag=1):
    if isinstance(max_lag,bool) or not isinstance(max_lag,int) or max_lag<0: raise ValueError("invalid lag")
    def iso(x):
        if not isinstance(x,str): raise ValueError("invalid date")
        try: d=date.fromisoformat(x)
        except ValueError as exc: raise ValueError("invalid date") from exc
        if d.isoformat()!=x: raise ValueError("noncanonical date")
        return x
    sessions=[iso(s) for s in sessions]
    if len(sessions)<2 or sessions!=sorted(set(sessions)): raise ValueError("invalid calendar")
    index={d:i for i,d in enumerate(sessions)}
    rows=list(rows)
    if not rows: raise ValueError("empty observations")
    counts=Counter(); seen=set(); observed=set()
    for g,d,y in rows:
        if not isinstance(g,str) or not g.strip(): raise ValueError("invalid group")
        d=iso(d)
        if d not in index: raise ValueError("off-calendar observation")
        if isinstance(y,bool) or not isinstance(y,(int,float)) or not isfinite(y): raise ValueError("invalid contrast")
        if (g,d) in seen: raise ValueError("duplicate group-date")
        seen.add((g,d)); counts[g]+=1; observed.add(d)
    if len(counts)<2 or len(observed)<2: raise ValueError("requires two groups and dates")
    G=len(counts); mean=sum(y/(G*counts[g]) for g,d,y in rows)
    if not isfinite(mean): raise ValueError("nonfinite weighted mean")
    gs=defaultdict(float); ds=defaultdict(float); intersection=0.
    for g,d,y in rows:
        s=(y-mean)/(G*counts[g]); gs[g]+=s; ds[d]+=s; intersection+=s*s
    if not all(isfinite(v) for v in gs.values()) or not all(isfinite(v) for v in ds.values()) or not isfinite(intersection):
        raise ValueError("nonfinite covariance score")
    scores=[ds.get(d,0.) for d in sessions]
    limit=min(max_lag,len(sessions)-1)
    gamma=[sum(scores[t]*scores[t-l] for t in range(l,len(scores))) for l in range(limit+1)]
    serial=gamma[0]+2*sum((1-l/(max_lag+1))*gamma[l] for l in range(1,limit+1))
    group=sum(v*v for v in gs.values()); raw=group+gamma[0]-intersection
    adjusted=group+serial-intersection
    if not all(isfinite(v) for v in gamma) or not all(isfinite(v) for v in (serial,group,raw,adjusted)):
        raise ValueError("nonfinite covariance component")
    return dict(mean_pp=mean,groups=G,observed_sessions=len(observed),calendar_sessions=len(sessions),
                missing_sessions=[d for d in sessions if d not in observed],lag_products=gamma,
                group_component=group,date_component=gamma[0],intersection_component=intersection,
                serial_date_component=serial,two_way_raw_variance=raw,
                serial_adjusted_raw_variance=adjusted,negative_serial_variance=adjusted<0,
                status="DESCRIPTIVE_CALENDAR_INDEXED_NO_CI_NO_CAUSAL_CLAIM")
