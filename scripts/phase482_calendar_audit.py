"""Calendar-anchored security-exchange coverage; no imputation or bundled data."""
import csv, datetime as dt, json, math, argparse
from collections import defaultdict

def audit(panel, calendar, cutoff):
    with open(calendar, newline="", encoding="utf-8-sig") as f:
        r=csv.DictReader(f)
        if not r.fieldnames or "date" not in r.fieldnames: raise ValueError("calendar requires date")
        dates=[x["date"].strip() for x in r]
    if not dates or dates!=sorted(set(dates)) or any(dt.date.fromisoformat(x).isoformat()!=x for x in dates):
        raise ValueError("invalid, duplicate, or unsorted calendar")
    if cutoff not in dates or cutoff==dates[0]: raise ValueError("cutoff must be interior")
    before={x for x in dates if x<cutoff}; after=set(dates)-before
    seen=set(); units=defaultdict(set); zeros=0
    with open(panel, newline="", encoding="utf-8-sig") as f:
        r=csv.DictReader(f)
        if not {"security","date","exchange","value"}.issubset(r.fieldnames or []): raise ValueError("missing panel columns")
        for row in r:
            s,d,e=[row[k].strip() for k in ("security","date","exchange")]
            if not s or not e or d not in dates: raise ValueError("blank key or off-calendar date")
            key=s,d,e
            if key in seen: raise ValueError("duplicate security-date-exchange")
            v=float(row["value"])
            if not math.isfinite(v): raise ValueError("nonfinite value")
            seen.add(key); units[s,e].add(d); zeros+=v==0
    if not seen: raise ValueError("empty panel")
    cats=dict.fromkeys(("complete_both","complete_pre_only","complete_post_only","incomplete_both"),0)
    for days in units.values():
        a,b=before.issubset(days),after.issubset(days)
        cats["complete_both" if a and b else "complete_pre_only" if a else "complete_post_only" if b else "incomplete_both"]+=1
    return {"calendar_dates":len(dates),"pre_dates":len(before),"post_dates":len(after),"observed_rows":len(seen),"observed_zeros":zeros,"union_units":len(units),"expected_union_grid_rows":len(units)*len(dates),"absent_union_grid_rows":len(units)*len(dates)-len(seen),"coverage_categories":cats,"warning":"Supplied calendar and observed union are not independently authenticated; absent is not zero."}

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("panel"); p.add_argument("calendar"); p.add_argument("cutoff"); a=p.parse_args()
    print(json.dumps(audit(a.panel,a.calendar,a.cutoff),indent=2,sort_keys=True))
