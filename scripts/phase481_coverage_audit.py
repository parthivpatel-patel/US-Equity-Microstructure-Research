"""Security-date-exchange coverage audit; no imputation or bundled data."""
import argparse
import collections
import csv
import datetime
import json
import math

def audit(path):
    seen=set(); dates=set(); units=set(); counts=collections.Counter(); sources=set(); zeros=0; rows=0
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        required={"security","date","exchange","value"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("missing columns: "+",".join(sorted(required-set(reader.fieldnames or []))))
        for line,r in enumerate(reader,2):
            s=r["security"].strip(); e=r["exchange"].strip(); d=r["date"].strip()
            if not s or not e: raise ValueError(f"blank key at line {line}")
            try: datetime.date.fromisoformat(d)
            except ValueError: raise ValueError(f"invalid date at line {line}")
            try: v=float(r["value"])
            except ValueError: raise ValueError(f"invalid value at line {line}")
            if not math.isfinite(v): raise ValueError(f"nonfinite value at line {line}")
            key=(s,d,e)
            if key in seen: raise ValueError(f"duplicate security-date-exchange at line {line}")
            seen.add(key); dates.add(d); units.add((s,e)); counts[(d,e)]+=1
            zeros+=v==0; rows+=1
            if "source_id" in r and r["source_id"].strip(): sources.add(r["source_id"].strip())
    if not rows: raise ValueError("empty panel")
    exchanges=sorted({e for _,e in units}); daylist=sorted(dates)
    return {
      "input_rows":rows,"observed_zero_rows":zeros,"unique_dates":len(dates),
      "unique_security_exchange_units":len(units),
      "complete_units_across_observed_dates":sum(all((s,d,e) in seen for d in daylist) for s,e in units),
      "union_units_by_exchange":{e:sum(x==e for _,x in units) for e in exchanges},
      "daily":[{"date":d,"observed_rows":sum(counts[d,e] for e in exchanges),
       "coverage_fraction_of_union":sum(counts[d,e] for e in exchanges)/len(units)} for d in daylist],
      "source_ids_present":sorted(sources),
      "caveat":"Absent rows are unknown, not zero; observed dates do not establish a trading calendar or source authenticity."
    }

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("panel");p.add_argument("--output");a=p.parse_args()
    result=json.dumps(audit(a.panel),indent=2,sort_keys=True)+"\n"
    if a.output:
        with open(a.output,"w",encoding="utf-8") as f:f.write(result)
    else: print(result,end="")
