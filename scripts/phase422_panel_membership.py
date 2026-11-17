"""Pre-reform membership audit; standard-library only, no historical data bundled."""
import argparse,csv,datetime as dt,json
from collections import defaultdict
NEEDED={'date','security','exchange','match_group','treated','hidden_count','total_count'}
def audit(rows):
    seen=set(); memberships=defaultdict(set); arms=defaultdict(lambda:{'0':set(),'1':set()}); dates=set(); count=0
    for i,r in enumerate(rows,2):
        if not NEEDED.issubset(r): raise ValueError(f'line {i}: missing columns')
        d=dt.date.fromisoformat(r['date'])
        if not dt.date(2025,9,1)<=d<dt.date(2025,11,3): raise ValueError(f'line {i}: date outside window')
        if d.weekday()>4: raise ValueError(f'line {i}: weekend date')
        if r['treated'] not in ('0','1'): raise ValueError(f'line {i}: treatment')
        if any(not r[k] or not r[k].strip() for k in ('security','exchange','match_group')): raise ValueError(f'line {i}: empty identifier')
        h,n=int(r['hidden_count']),int(r['total_count'])
        if n<=0 or not 0<=h<=n: raise ValueError(f'line {i}: counts')
        s,e,g,t=(r[k].strip() for k in ('security','exchange','match_group','treated'))
        if (d,s,e) in seen: raise ValueError(f'line {i}: duplicate')
        seen.add((d,s,e)); memberships[s].add((g,t)); arms[g][t].add(s); dates.add(d); count+=1
    if not count: raise ValueError('empty input')
    unstable=sorted(s for s,v in memberships.items() if len(v)>1)
    unpaired=sorted(g for g,a in arms.items() if not a['0'] or not a['1'])
    return {'observations':count,'securities':len(memberships),'observed_weekdays':len(dates),'groups':len(arms),'unstable_security_membership':unstable,'groups_missing_arm':unpaired,'structural_pass':not unstable and not unpaired,'warning':'No source authentication, exchange holiday validation, contemporaneous treatment verification, or causal inference.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('input_csv');p.add_argument('--output',required=True);a=p.parse_args()
    with open(a.input_csv,newline='',encoding='utf-8') as f: result=audit(csv.DictReader(f))
    with open(a.output,'w',encoding='utf-8') as f: json.dump(result,f,indent=2,sort_keys=True)
    if not result['structural_pass']: raise SystemExit(2)
if __name__=='__main__':main()
