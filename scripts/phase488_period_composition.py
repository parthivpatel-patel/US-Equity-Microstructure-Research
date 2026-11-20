"""Cutoff-aware eligible versus observed security-exchange-date composition audit."""
import argparse,csv,hashlib,json,math
from collections import Counter
from datetime import date
from pathlib import Path

def read(path, observed=False):
    fields={'security','exchange','date','outcome'} if observed else {'security','exchange','date'}
    out={}
    with open(path,newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames is None or len(reader.fieldnames)!=len(fields) or set(reader.fieldnames)!=fields:
            raise ValueError('invalid schema')
        for row in reader:
            if any(v is None or not v.strip() for v in row.values()): raise ValueError('blank field')
            d=date.fromisoformat(row['date'])
            if d.isoformat()!=row['date']: raise ValueError('noncanonical date')
            key=(row['security'],row['exchange'],row['date'])
            if key in out: raise ValueError('duplicate key')
            if observed:
                value=float(row['outcome'])
                if not math.isfinite(value): raise ValueError('nonfinite outcome')
            else: value=True
            out[key]=value
    return out

def audit(eligibility,panel,cutoff):
    d=date.fromisoformat(cutoff)
    if d.isoformat()!=cutoff: raise ValueError('noncanonical cutoff')
    e=read(eligibility); o=read(panel,True)
    if not e: raise ValueError('empty eligibility')
    if set(o)-set(e): raise ValueError('observation outside eligibility')
    days=sorted({k[2] for k in e})
    if not (days[0]<cutoff<=days[-1]): raise ValueError('cutoff must have eligible dates on both sides')
    result={'cutoff':cutoff,'provenance_status':'UNAUTHENTICATED_INPUTS'}
    for name,pred in [('pre',lambda x:x<cutoff),('post',lambda x:x>=cutoff)]:
        ek={k for k in e if pred(k[2])}; ok={k for k in o if pred(k[2])}
        result[name]={'eligible_cells':len(ek),'observed_cells':len(ok),
                      'missing_eligible_cells':len(ek-ok),'observed_zero_cells':sum(o[k]==0 for k in ok),
                      'eligible_units':{k[:2] for k in ek},'observed_units':{k[:2] for k in ok},
                      'by_exchange':{x:{'eligible':sum(k[1]==x for k in ek),
                                        'observed':sum(k[1]==x for k in ok),
                                        'missing':sum(k[1]==x for k in ek-ok)}
                                     for x in sorted({k[1] for k in ek})}}
    for kind in ('eligible','observed'):
        a=result['pre'][kind+'_units']; b=result['post'][kind+'_units']
        result[kind+'_unit_composition']={'both':len(a&b),'pre_only':len(a-b),'post_only':len(b-a)}
        for period in ('pre','post'): result[period][kind+'_units']=len(result[period][kind+'_units'])
    result['sha256']={n:hashlib.sha256(Path(p).read_bytes()).hexdigest()
                      for n,p in [('eligibility',eligibility),('panel',panel)]}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--eligibility',required=True);p.add_argument('--panel',required=True)
    p.add_argument('--cutoff',required=True);p.add_argument('--output')
    a=p.parse_args()
    payload=json.dumps(audit(a.eligibility,a.panel,a.cutoff),indent=2,sort_keys=True)+'\n'
    if a.output: Path(a.output).write_text(payload,encoding='utf-8')
    else: print(payload,end='')
