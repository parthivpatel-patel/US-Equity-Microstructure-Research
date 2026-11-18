"""Descriptive pre-reform matched-group placebo and pretrend checks; unauthenticated inputs."""
from collections import defaultdict
from datetime import date
from math import isfinite

def diagnostics(rows, placebo="2025-10-01", reform="2025-11-03", min_dates=2):
    p,r=date.fromisoformat(placebo),date.fromisoformat(reform)
    if not p<r or type(min_dates) is not int or min_dates<2: raise ValueError("invalid boundaries")
    seen,assignment,totals=set(),{},defaultdict(lambda:[0.,0])
    for z in rows:
        s,e,g=(z[k] for k in ("security","exchange","matched_group"))
        if not all(isinstance(v,str) and v.strip() for v in (s,e,g)): raise ValueError("invalid identifier")
        d=date.fromisoformat(z["date"]); t=z["treated"]; y=z["outcome"]
        if type(t) is not bool or type(y) not in (int,float) or not isfinite(y): raise ValueError("invalid outcome or treatment")
        if (s,e,d) in seen: raise ValueError("duplicate observation")
        seen.add((s,e,d))
        if s in assignment and assignment[s]!=t: raise ValueError("cross-exchange treatment conflict")
        assignment[s]=t
        if d<r:
            a=totals[(e,g,d,t)]; a[0]+=y; a[1]+=1
    paired={}
    for e,g,d,_ in totals:
        a,b=totals.get((e,g,d,True)),totals.get((e,g,d,False))
        if a and b: paired[(e,g,d)]=a[0]/a[1]-b[0]/b[1]
    groups=sorted({(e,g) for e,g,d in paired})
    out=[]
    for e,g in groups:
        dates=sorted(d for ee,gg,d in paired if (ee,gg)==(e,g))
        pre=[d for d in dates if d<p]; post=[d for d in dates if p<=d<r]
        rec={"exchange":e,"matched_group":g,"pre_dates":len(pre),"placebo_post_dates":len(post),"placebo_effect":None,"pretrend_slope_per_day":None}
        if len(pre)>=min_dates and len(post)>=min_dates:
            y=[paired[(e,g,d)] for d in pre]
            x=[(d-pre[0]).days for d in pre]
            xm=sum(x)/len(x); ym=sum(y)/len(y)
            den=sum((v-xm)**2 for v in x)
            rec["pretrend_slope_per_day"]=sum((v-xm)*(w-ym) for v,w in zip(x,y))/den if den else None
            rec["placebo_effect"]=sum(paired[(e,g,d)] for d in post)/len(post)-ym
        out.append(rec)
    eligible=[z["placebo_effect"] for z in out if z["placebo_effect"] is not None]
    return {"groups":out,"eligible_groups":len(eligible),"total_paired_groups":len(groups),"equal_group_placebo_mean":sum(eligible)/len(eligible) if eligible else None,"source_authenticated":False,"treatment_authenticated":False,"serial_dependence_inference_performed":False}
