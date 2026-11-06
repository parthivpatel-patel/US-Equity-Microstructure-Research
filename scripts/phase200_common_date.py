"""Descriptive common-date matched-group contrasts. No causal inference."""
from collections import defaultdict
from math import isfinite

def common_date_contrasts(rows):
    rows=list(rows)
    if not rows: raise ValueError("empty panel")
    cells=defaultdict(list); groups=set(); date_outcomes=set()
    for r in rows:
        d,g,t,o=(r[k] for k in ("date","group","treatment","outcome"))
        v=float(r["value"])
        if any(not isinstance(x,str) or not x for x in (d,g,o)): raise ValueError("invalid identifier")
        if type(t) is not int or t not in (0,1) or not isfinite(v): raise ValueError("invalid treatment/value")
        cells[d,o,g,t].append(v); groups.add(g); date_outcomes.add((d,o))
    admitted=[]; rejected=[]
    for d,o in sorted(date_outcomes):
        missing=[(g,t) for g in sorted(groups) for t in (0,1) if (d,o,g,t) not in cells]
        if missing:
            rejected.append({"date":d,"outcome":o,"missing_cells":len(missing)}); continue
        contrasts=[]
        for g in sorted(groups):
            a=cells[d,o,g,1]; b=cells[d,o,g,0]
            contrasts.append(sum(a)/len(a)-sum(b)/len(b))
        admitted.append({"date":d,"outcome":o,"groups":len(groups),"contrast":sum(contrasts)/len(contrasts)})
    return {"date_contrasts":admitted,"rejected_dates":rejected,"group_count":len(groups),
            "warning":"Descriptive only; source authentication, pretrends, dependence-aware uncertainty and causal identification absent."}
