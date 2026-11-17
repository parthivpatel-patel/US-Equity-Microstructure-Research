"""Audit date-by-date matched support and security continuity; no source data bundled."""
import csv,datetime as dt,json,argparse
from collections import defaultdict
CUTOFF=dt.date(2025,11,3)
REQUIRED={'date','security','exchange','match_group','treated','hidden_count','total_count'}
def audit(rows):
    seen=set(); membership=defaultdict(set); cells=defaultdict(set); dates=defaultdict(set); n=0
    for i,r in enumerate(rows,2):
        if not REQUIRED.issubset(r): raise ValueError(f'line {i}: missing columns')
        try: d=dt.date.fromisoformat(r['date']); h,t=int(r['hidden_count']),int(r['total_count'])
        except (ValueError,TypeError) as exc: raise ValueError(f'line {i}: invalid date/count') from exc
        if d.weekday()>=5 or t<=0 or not 0<=h<=t: raise ValueError(f'line {i}: invalid day/count bounds')
        if r['treated'] not in ('0','1'): raise ValueError(f'line {i}: invalid arm')
        s,e,g=(r[k].strip() for k in ('security','exchange','match_group'))
        if not all((s,e,g)): raise ValueError(f'line {i}: blank identifier')
        if (d,s,e) in seen: raise ValueError(f'line {i}: duplicate')
        seen.add((d,s,e)); a=int(r['treated']); p='pre' if d<CUTOFF else 'post'
        membership[s].add((g,a)); cells[(g,e,p,a,d)].add(s); dates[(g,e,p)].add(d); n+=1
    if not n: raise ValueError('empty panel')
    out=[]
    for g,e in sorted({(g,e) for g,e,p in dates}):
        fixed={}
        counts={}
        for p in ('pre','post'):
            ds=sorted(dates[(g,e,p)])
            paired=[d for d in ds if cells[(g,e,p,0,d)] and cells[(g,e,p,1,d)]]
            counts[p]=(len(ds),len(paired))
            for a in (0,1):
                fixed[p,a]=set.intersection(*(cells[(g,e,p,a,d)] for d in paired)) if paired else set()
        common={a:fixed['pre',a]&fixed['post',a] for a in (0,1)}
        strict=all(counts[p][0]>0 and counts[p][0]==counts[p][1] for p in ('pre','post')) and all(common.values())
        out.append({'match_group':g,'exchange':e,'pre_dates':counts['pre'][0],'pre_paired_dates':counts['pre'][1],
                    'post_dates':counts['post'][0],'post_paired_dates':counts['post'][1],
                    'fixed_control_n':len(common[0]),'fixed_treated_n':len(common[1]),'strict_support':bool(strict)})
    unstable=sorted(s for s,v in membership.items() if len(v)>1)
    return {'observations':n,'group_exchange_units':len(out),'strict_support_units':sum(x['strict_support'] for x in out),
            'unstable_security_membership':unstable,'by_group_exchange':out,
            'warning':'Structural support only; no authentication, estimation, or dependence-aware inference.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('input_csv');p.add_argument('--output',required=True);a=p.parse_args()
    with open(a.input_csv,encoding='utf-8',newline='') as f: result=audit(csv.DictReader(f))
    with open(a.output,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,sort_keys=True)
    if result['unstable_security_membership'] or not result['strict_support_units']: raise SystemExit(2)
if __name__=='__main__': main()
