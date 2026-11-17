"""Fixed-security support gate for matched security/exchange panel; no source data bundled."""
import argparse,csv,datetime as dt,json
from collections import defaultdict
FIELDS={'date','security','exchange','match_group','treated','hidden_count','total_count'}
CUTOFF=dt.date(2025,11,3)
def audit(rows):
    seen=set(); membership=defaultdict(set); cells=defaultdict(set); count=0
    for i,r in enumerate(rows,2):
        if not FIELDS.issubset(r): raise ValueError(f'line {i}: missing columns')
        try:
            d=dt.date.fromisoformat(r['date'])
            h,n=int(r['hidden_count']),int(r['total_count'])
        except (ValueError,TypeError) as exc: raise ValueError(f'line {i}: invalid date/count') from exc
        if d.weekday()>=5: raise ValueError(f'line {i}: weekend')
        if n<=0 or not 0<=h<=n: raise ValueError(f'line {i}: count bounds')
        if r['treated'] not in ('0','1'): raise ValueError(f'line {i}: arm')
        s,e,g=(r[k].strip() for k in ('security','exchange','match_group'))
        if not all((s,e,g)): raise ValueError(f'line {i}: blank identifier')
        if (d,s,e) in seen: raise ValueError(f'line {i}: duplicate security-exchange-date')
        seen.add((d,s,e)); arm=int(r['treated'])
        membership[s].add((g,arm))
        cells[(g,e,'pre' if d<CUTOFF else 'post',arm)].add(s)
        count+=1
    if not count: raise ValueError('empty panel')
    unstable=sorted(s for s,v in membership.items() if len(v)>1)
    units=sorted({(g,e) for g,e,_,_ in cells})
    out=[]
    for g,e in units:
        p0,p1=cells[(g,e,'pre',0)],cells[(g,e,'pre',1)]
        q0,q1=cells[(g,e,'post',0)],cells[(g,e,'post',1)]
        f0,f1=p0&q0,p1&q1
        out.append({'match_group':g,'exchange':e,
          'pre_paired':bool(p0 and p1),'post_paired':bool(q0 and q1),
          'fixed_paired':bool(f0 and f1),
          'pre_control_n':len(p0),'pre_treated_n':len(p1),
          'post_control_n':len(q0),'post_treated_n':len(q1),
          'fixed_control_n':len(f0),'fixed_treated_n':len(f1)})
    return {'observations':count,'units':len(units),
      'pre_post_paired_units':sum(x['pre_paired'] and x['post_paired'] for x in out),
      'fixed_security_paired_units':sum(x['fixed_paired'] for x in out),
      'unstable_security_membership':unstable,'by_group_exchange':out,
      'estimation_ready':bool(not unstable and any(x['fixed_paired'] for x in out)),
      'warning':'Structural audit only: not source authentication, daily balance, or causal inference.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('input_csv');p.add_argument('--output',required=True);a=p.parse_args()
    with open(a.input_csv,encoding='utf-8',newline='') as f: result=audit(csv.DictReader(f))
    with open(a.output,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,sort_keys=True)
    if not result['estimation_ready']: raise SystemExit(2)
if __name__=='__main__': main()
