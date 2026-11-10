"""Phase 277: fixed security/exchange roster composition audit. Descriptive only."""
import datetime as dt
import math
from collections import defaultdict

def audit_panel(rows, expected_dates, expected_pairs):
    dates=tuple(expected_dates)
    roster=tuple(expected_pairs)
    if not dates or not roster or len(set(dates))!=len(dates) or len(set(roster))!=len(roster):
        raise ValueError("empty or duplicate calendar/roster")
    if tuple(sorted(dates))!=dates or any(type(d) is not dt.date for d in dates):
        raise ValueError("invalid calendar")
    if any(not isinstance(p,str) or not p or not isinstance(e,str) or not e for p,e in roster):
        raise ValueError("invalid pair/exchange")
    if len({p for p,e in roster})!=len(roster):
        raise ValueError("pair assigned to multiple exchanges")
    seen={}
    for r in rows:
        d=dt.date.fromisoformat(r["date"])
        key=(str(r["pair"]),str(r["exchange"]))
        if d not in dates or key not in roster or (d,key) in seen:
            raise ValueError("unexpected or duplicate date/pair/exchange")
        a,b=float(r["treated"]),float(r["control"])
        if not math.isfinite(a) or not math.isfinite(b):
            raise ValueError("nonfinite outcome")
        seen[(d,key)]=a-b
    if len(seen)!=len(dates)*len(roster):
        raise ValueError("incomplete fixed roster")
    exchanges=sorted({e for _,e in roster})
    counts={e:sum(ex==e for _,ex in roster) for e in exchanges}
    results=[]
    for d in dates:
        by_exchange={e:sum(seen[(d,(p,ex))] for p,ex in roster if ex==e)/counts[e] for e in exchanges}
        results.append({"date":d.isoformat(),
                        "pair_weighted":sum(by_exchange[e]*counts[e] for e in exchanges)/len(roster),
                        "exchange_equal":sum(by_exchange.values())/len(exchanges),
                        "by_exchange":by_exchange})
    return {"dates":results,"pair_counts_by_exchange":counts,
            "expected_observations":len(dates)*len(roster),
            "source_authenticated":False,"calendar_authenticated":False,
            "treatment_authenticated":False,"historical_inference_authorized":False}
