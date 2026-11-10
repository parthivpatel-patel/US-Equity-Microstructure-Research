"""Strict common-date exchange-panel admission; descriptive only."""
from datetime import date
from math import isfinite

def admit_exchange_panel(rows, sessions, pair_counts):
    sessions, rows = list(sessions), list(rows)
    if not sessions or not pair_counts:
        raise ValueError("empty calendar or roster")
    if len(set(sessions)) != len(sessions) or sessions != sorted(sessions):
        raise ValueError("unordered or duplicate sessions")
    if any(not isinstance(s,str) or date.fromisoformat(s).isoformat()!=s for s in sessions):
        raise ValueError("invalid session date")
    if any(not isinstance(e,str) or not e or type(n) is not int or n<=0 for e,n in pair_counts.items()):
        raise ValueError("invalid fixed roster")
    expected={(s,e) for s in sessions for e in pair_counts}
    found={}
    for r in rows:
        if not isinstance(r,dict) or set(r)!={"date","exchange","contrast"}:
            raise ValueError("invalid row schema")
        key=(r["date"],r["exchange"])
        if key not in expected or key in found:
            raise ValueError("unexpected or duplicate observation")
        v=r["contrast"]
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not isfinite(v):
            raise ValueError("nonfinite or invalid contrast")
        found[key]=float(v)
    if set(found)!=expected:
        raise ValueError("incomplete common-date panel")
    return {"dates":[{"date":s,"by_exchange":{e:found[(s,e)] for e in sorted(pair_counts)}} for s in sessions],
            "pair_counts_by_exchange":dict(pair_counts),
            "source_authenticated":False,"historical_inference_authorized":False,
            "calendar_authentication_required":True,"treatment_authentication_required":True}
