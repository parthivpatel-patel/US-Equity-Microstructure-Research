"""Fail-closed fixed-roster common-date contrasts and date-level HAC; descriptive only."""
from collections import defaultdict
from datetime import date
from math import isfinite, sqrt

def analyze(rows, sessions, outcome, lags=(0, 1), min_sessions=20):
    rows, sessions = list(rows), list(sessions)
    if not rows or not sessions or len(set(sessions)) != len(sessions) or sessions != sorted(sessions):
        raise ValueError("invalid panel/calendar")
    if any(type(d) is not str or date.fromisoformat(d).isoformat() != d for d in sessions):
        raise ValueError("invalid calendar date")
    if type(outcome) is not str or not outcome or type(min_sessions) is not int or min_sessions < 2 or len(sessions) < min_sessions:
        raise ValueError("invalid outcome or insufficient sessions")
    if not lags or len(set(lags)) != len(lags) or any(type(l) is not int or l < 0 or l >= len(sessions) for l in lags):
        raise ValueError("invalid HAC lags")
    roster, cells, groups = {}, {}, defaultdict(set)
    for r in rows:
        if not isinstance(r, dict) or any(k not in r for k in ("date","security","exchange","group","treatment","outcome","value")):
            raise ValueError("malformed observation")
        d,s,e,g,t,o = (r[k] for k in ("date","security","exchange","group","treatment","outcome"))
        v = r["value"]
        if any(type(x) is not str or not x for x in (d,s,e,g,o)) or type(t) is not int or t not in (0,1) or type(v) not in (int,float) or not isfinite(v):
            raise ValueError("invalid observation")
        if d not in sessions or o != outcome:
            raise ValueError("unexpected date/outcome")
        ident, assignment = (s,e), (g,t)
        if ident in roster and roster[ident] != assignment:
            raise ValueError("assignment switch")
        roster[ident] = assignment
        groups[g].add(t)
        key = (d,s,e)
        if key in cells:
            raise ValueError("duplicate observation")
        cells[key] = float(v)
    if any(arms != {0,1} for arms in groups.values()):
        raise ValueError("unmatched group")
    if len(cells) != len(sessions)*len(roster):
        raise ValueError("incomplete fixed roster")
    by_group = defaultdict(list)
    for d in sessions:
        for (s,e),(g,t) in roster.items():
            if (d,s,e) not in cells:
                raise ValueError("missing fixed-roster cell")
            by_group[d,g,t].append(cells[d,s,e])
    contrasts = []
    for d in sessions:
        differences = []
        for g in sorted(groups):
            a,b = by_group[d,g,1],by_group[d,g,0]
            differences.append(sum(a)/len(a)-sum(b)/len(b))
        contrasts.append(sum(differences)/len(differences))
    n = len(contrasts)
    mean = sum(contrasts)/n
    residual = [x-mean for x in contrasts]
    sensitivity = []
    for lag in lags:
        lr = sum(x*x for x in residual)/n
        for h in range(1,lag+1):
            lr += 2*(1-h/(lag+1))*sum(residual[i]*residual[i-h] for i in range(h,n))/n
        sensitivity.append({"lag":lag,"mean":mean,"hac_se":sqrt(max(0,lr)/n)})
    return {"n_dates":n,"n_security_exchange":len(roster),"n_groups":len(groups),"outcome":outcome,
            "date_contrasts":[{"date":d,"contrast":x} for d,x in zip(sessions,contrasts)],
            "hac_sensitivity":sensitivity,"source_authenticated":False,
            "treatment_authenticated":False,"causal_effect_established":False}
