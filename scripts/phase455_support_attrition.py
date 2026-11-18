"""Audit common-date balanced-panel attrition; descriptive, not causal."""
from collections import defaultdict
from datetime import date
import math

def audit(rows, cutoff="2025-11-03"):
    boundary=date.fromisoformat(cutoff)
    cells=defaultdict(lambda:{True:set(),False:set()})
    seen=set(); assignment={}
    for r in rows:
        s,e,g=(r[k] for k in ("security","exchange","matched_group"))
        if not all(isinstance(v,str) and v.strip() for v in (s,e,g)): raise ValueError("invalid identifier")
        d=date.fromisoformat(r["date"]); t=r["treated"]; y=r["outcome"]
        if type(t) is not bool: raise ValueError("invalid treatment")
        if isinstance(y,bool) or not isinstance(y,(int,float)) or not math.isfinite(y): raise ValueError("invalid outcome")
        if (s,e,d) in seen: raise ValueError("duplicate security-exchange-date")
        seen.add((s,e,d))
        if (s,e) in assignment and assignment[(s,e)]!=(g,t): raise ValueError("unstable assignment")
        assignment[(s,e)]=(g,t)
        cells[(e,g,d)][t].add(s)
    if not cells: raise ValueError("empty input")
    strata={(e,g) for e,g,_ in cells}
    complete={(e,g):{d for ee,gg,d in cells if (ee,gg)==(e,g) and all(cells[(ee,gg,d)][t] for t in (True,False))} for e,g in strata}
    common=set.intersection(*complete.values())
    out={"strata":len(strata),"all_calendar_dates":len({d for _,_,d in cells}),"fully_balanced_calendar_dates":len(common),"periods":{}}
    for label,pred in (("pre",lambda d:d<boundary),("post",lambda d:d>=boundary)):
        dates={d for _,_,d in cells if pred(d)}
        balanced={d for d in common if pred(d)}
        candidate=sum(1 for e,g,d in cells if pred(d))
        paired=sum(1 for e,g,d in cells if pred(d) and d in complete[(e,g)])
        retained=sum(1 for e,g,d in cells if d in balanced)
        out["periods"][label]={"observed_dates":len(dates),"balanced_dates":len(balanced),"observed_stratum_date_cells":candidate,"paired_stratum_date_cells":paired,"globally_retained_stratum_date_cells":retained,"excluded_stratum_date_cells":candidate-retained,"retained_fraction":retained/candidate if candidate else None}
    out["source_authenticated"]=False
    out["causal_identification_established"]=False
    return out
