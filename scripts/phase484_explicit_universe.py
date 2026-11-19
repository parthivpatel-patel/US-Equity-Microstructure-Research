"""Audit panel coverage against separately supplied fixed security-exchange universe.

No historical data bundled. A fixed universe is not proof of date-specific eligibility.
"""
import csv, hashlib, json, math, datetime
from collections import Counter

def rows(path, fields):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or len(reader.fieldnames) != len(fields) or set(reader.fieldnames) != set(fields):
            raise ValueError("unexpected CSV schema")
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError("ragged CSV row")
            yield {k:v.strip() for k,v in row.items()}

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1048576),b""):
            h.update(chunk)
    return h.hexdigest()

def audit(panel, calendar, universe):
    dates=[r["date"] for r in rows(calendar,["date"])]
    if not dates or dates != sorted(set(dates)) or any(datetime.date.fromisoformat(d).isoformat()!=d for d in dates):
        raise ValueError("invalid calendar")
    units=[(r["security"],r["exchange"]) for r in rows(universe,["security","exchange"])]
    if not units or len(set(units))!=len(units) or any(not s or not e for s,e in units):
        raise ValueError("invalid universe")
    unit_set,date_set=set(units),set(dates)
    seen=set(); zeros=0
    for r in rows(panel,["security","date","exchange","value"]):
        u=(r["security"],r["exchange"]); d=r["date"]
        if u not in unit_set or d not in date_set:
            raise ValueError("outside universe/calendar")
        if (u,d) in seen:
            raise ValueError("duplicate observation")
        v=float(r["value"])
        if not math.isfinite(v):
            raise ValueError("nonfinite outcome")
        seen.add((u,d)); zeros+=v==0
    by_date={d:sum((u,d) in seen for u in units) for d in dates}
    by_unit={s+"|"+e:sum(((s,e),d) in seen for d in dates) for s,e in units}
    return {
        "sha256":{"panel":sha256(panel),"calendar":sha256(calendar),"universe":sha256(universe)},
        "expected_units":len(units),"calendar_dates":len(dates),
        "expected_cells":len(units)*len(dates),"observed_cells":len(seen),
        "missing_cells":len(units)*len(dates)-len(seen),
        "observed_zero_cells":zeros,
        "complete_units":sum(n==len(dates) for n in by_unit.values()),
        "daily_observed_cells":by_date,"unit_observed_date_counts":by_unit,
        "source_authentication":"UNVERIFIED: hashes do not authenticate SEC origin",
        "warning":"Missing is not zero; fixed universe may include ineligible unit-dates."
    }

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("panel");p.add_argument("calendar");p.add_argument("universe")
    a=p.parse_args()
    print(json.dumps(audit(a.panel,a.calendar,a.universe),indent=2,sort_keys=True))
