"""Eligibility interval coverage; structural validation only, not authenticated SEC evidence."""
from collections import Counter
from datetime import date

def day(s):
    if not isinstance(s,str):
        raise ValueError("ISO date required")
    try: d=date.fromisoformat(s)
    except ValueError as e: raise ValueError("invalid date") from e
    if d.isoformat()!=s: raise ValueError("noncanonical date")
    return d

def audit(observations, intervals, sessions):
    """Rows (security,exchange,date); intervals (security,exchange,start,end), inclusive."""
    calendar=[day(s) for s in sessions]
    if calendar!=sorted(set(calendar)) or any(d.weekday()>=5 for d in calendar):
        raise ValueError("calendar not ordered, unique weekdays")
    spans={}
    for sec,ex,start,end in intervals:
        if not sec or not ex: raise ValueError("empty identifier")
        a,b=day(start),day(end)
        if a>b: raise ValueError("reversed interval")
        spans.setdefault((sec,ex),[]).append((a,b))
    for ranges in spans.values():
        ordered=sorted(ranges)
        if any(a2<=b1 for (_,b1),(a2,_) in zip(ordered,ordered[1:])):
            raise ValueError("overlapping intervals")
    expected={(sec,ex,d.isoformat()) for (sec,ex),ranges in spans.items()
              for a,b in ranges for d in calendar if a<=d<=b}
    empty=sorted((sec,ex,a.isoformat(),b.isoformat()) for (sec,ex),ranges in spans.items()
                 for a,b in ranges if not any(a<=d<=b for d in calendar))
    rows=[(sec,ex,day(dt).isoformat()) for sec,ex,dt in observations]
    if any(not sec or not ex for sec,ex,_ in rows): raise ValueError("empty identifier")
    counts=Counter(rows)
    actual=set(counts)
    return dict(missing=sorted(expected-actual),unexpected=sorted(actual-expected),
                duplicates=sorted(k for k,v in counts.items() if v>1),
                empty_intervals=empty,expected_cells=len(expected),observed_rows=len(rows),
                source_authenticated=False,eligibility_authenticated=False,
                calendar_authenticated=False,causal_inference_authorized=False)
