"""Exploratory equal-group two-way score decomposition with serial trading-date lags; NO CI."""
from collections import Counter, defaultdict
from datetime import date
from math import isfinite

def serial_two_way_components(rows, max_lag=1):
    if isinstance(max_lag,bool) or not isinstance(max_lag,int) or max_lag<0: raise ValueError("invalid lag")
    rows=list(rows)
    if not rows: raise ValueError("empty panel")
    seen=set(); counts=Counter()
    for g,d,y in rows:
        if not isinstance(g,str) or not g.strip(): raise ValueError("invalid group")
        if not isinstance(d,str): raise ValueError("invalid date")
        try:
            if date.fromisoformat(d).isoformat()!=d: raise ValueError("noncanonical date")
        except ValueError as exc: raise ValueError("invalid ISO date") from exc
        if isinstance(y,bool) or not isinstance(y,(int,float)) or not isfinite(y): raise ValueError("invalid contrast")
        if (g,d) in seen: raise ValueError("duplicate group-date; aggregate exchanges first")
        seen.add((g,d)); counts[g]+=1
    days=sorted({d for _,d,_ in rows}); G=len(counts)
    if G<2 or len(days)<2: raise ValueError("requires two groups and dates")
    mean=sum(y/(G*counts[g]) for g,d,y in rows)
    gs=defaultdict(float); ds=defaultdict(float); intersection=0.
    for g,d,y in rows:
        s=(y-mean)/(G*counts[g]); gs[g]+=s; ds[d]+=s; intersection+=s*s
    vg=sum(x*x for x in gs.values()); vd=sum(x*x for x in ds.values())
    scores=[ds[d] for d in days]; limit=min(max_lag,len(days)-1)
    gamma=[sum(scores[t]*scores[t-l] for t in range(l,len(days))) for l in range(limit+1)]
    serial=gamma[0]+2*sum((1-l/(max_lag+1))*gamma[l] for l in range(1,len(gamma)))
    raw=vg+vd-intersection; adjusted=vg+serial-intersection
    return dict(groups=G,dates=len(days),cells=len(rows),mean_pp=mean,
                group_component=vg,date_component=vd,intersection_component=intersection,
                lag_products=gamma,max_lag_requested=max_lag,max_lag_observed=limit,
                serial_date_component=serial,two_way_raw_variance=raw,
                serial_adjusted_raw_variance=adjusted,serial_increment=adjusted-raw,
                negative_raw_variance=raw<0,negative_serial_variance=adjusted<0,
                status="DESCRIPTIVE_UNCORRECTED_NO_CI_NO_CAUSAL_CLAIM")
