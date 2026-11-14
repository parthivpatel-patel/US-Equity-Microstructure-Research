"""Trading-date lag score diagnostic for equal-group-weighted contrasts; no CI."""
from collections import Counter, defaultdict
from datetime import date
from math import isfinite

def date_lag_diagnostic(rows, max_lag=5):
    rows=list(rows)
    if not isinstance(max_lag,int) or isinstance(max_lag,bool) or max_lag<0: raise ValueError('invalid lag')
    if not rows: raise ValueError('empty rows')
    counts=Counter(); seen=set()
    for group,day,value in rows:
        if not isinstance(group,str) or not group.strip(): raise ValueError('invalid group')
        if not isinstance(day,str) or date.fromisoformat(day).isoformat()!=day: raise ValueError('invalid date')
        if not isinstance(value,(int,float)) or isinstance(value,bool) or not isfinite(value): raise ValueError('invalid value')
        if (group,day) in seen: raise ValueError('duplicate group-date')
        seen.add((group,day)); counts[group]+=1
    days=sorted({d for _,d,_ in rows})
    if len(days)<2 or len(counts)<2: raise ValueError('requires >=2 groups and dates')
    G=len(counts)
    mean=sum(value/(G*counts[group]) for group,day,value in rows)
    scores=defaultdict(float)
    for group,day,value in rows: scores[day]+=(value-mean)/(G*counts[group])
    s=[scores[d] for d in days]
    gamma=[sum(s[t]*s[t-lag] for t in range(lag,len(s))) for lag in range(min(max_lag,len(s)-1)+1)]
    bartlett=gamma[0]+2*sum((1-lag/(max_lag+1))*gamma[lag] for lag in range(1,len(gamma)))
    return dict(groups=G,dates=len(days),mean_pp=mean,date_scores=dict(zip(days,s)),lag_products=gamma,bartlett_date_component=bartlett,status='DESCRIPTIVE_DATE_SCORE_DIAGNOSTIC_NOT_TWO_WAY_CI')
