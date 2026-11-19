"""Date-specific eligible-key coverage audit. Inputs are not source-authenticated."""
import csv,hashlib,json,math,sys
from collections import Counter
from datetime import date
from pathlib import Path

def load(path,columns):
    with open(path,newline='',encoding='utf-8-sig') as f:
        r=csv.DictReader(f)
        if r.fieldnames is None or len(r.fieldnames)!=len(columns) or set(r.fieldnames)!=set(columns):
            raise ValueError('invalid schema')
        rows=list(r)
    out={}
    for row in rows:
        if any(v is None or not v.strip() for v in row.values()): raise ValueError('blank field')
        d=date.fromisoformat(row['date'])
        if d.isoformat()!=row['date']: raise ValueError('invalid date format')
        k=(row['security'],row['exchange'],row['date'])
        if k in out: raise ValueError('duplicate key')
        if 'outcome' in row:
            v=float(row['outcome'])
            if not math.isfinite(v): raise ValueError('nonfinite outcome')
        else: v=True
        out[k]=v
    return out

def audit(eligibility,panel):
    e=load(eligibility,['security','exchange','date'])
    o=load(panel,['security','exchange','date','outcome'])
    if set(o)-set(e): raise ValueError('observation outside eligible universe')
    units={k[:2] for k in e}
    days=sorted({k[2] for k in e})
    return {'eligible':len(e),'observed':len(o),'missing':len(e)-len(o),
      'observed_zero':sum(v==0 for v in o.values()),
      'eligible_units':len(units),
      'complete_eligible_units':sum(all(k in o for k in e if k[:2]==u) for u in units),
      'daily':[{'date':d,'eligible':sum(k[2]==d for k in e),
                'observed':sum(k[2]==d for k in o),
                'missing':sum(k[2]==d for k in e)-sum(k[2]==d for k in o)} for d in days],
      'sha256':{name:hashlib.sha256(Path(path).read_bytes()).hexdigest()
                for name,path in [('eligibility',eligibility),('panel',panel)]},
      'provenance_status':'UNAUTHENTICATED_INPUTS'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--eligibility',required=True);p.add_argument('--panel',required=True)
    p.add_argument('--output')
    a=p.parse_args()
    result=json.dumps(audit(a.eligibility,a.panel),indent=2,sort_keys=True)+'\n'
    if a.output: Path(a.output).write_text(result,encoding='utf-8')
    else: print(result,end='')
