"""Temporal matched-cell support audit; no historical observations bundled."""
import argparse,csv,datetime as dt,json
from collections import defaultdict
REQUIRED={'date','security','exchange','match_group','treated','hidden_count','total_count'}
def audit(rows):
    cells=defaultdict(lambda:{0:set(),1:set()});seen=set();members=defaultdict(set);n=0
    for line,r in enumerate(rows,2):
        if not REQUIRED.issubset(r):raise ValueError(f'line {line}: missing columns')
        d=dt.date.fromisoformat(r['date'])
        if not dt.date(2025,9,1)<=d<dt.date(2025,11,3) or d.weekday()>=5:raise ValueError(f'line {line}: date')
        if r['treated'] not in ('0','1'):raise ValueError(f'line {line}: arm')
        s,e,g=(r[k].strip() for k in ('security','exchange','match_group'))
        if not all((s,e,g)):raise ValueError(f'line {line}: identifier')
        h,tot=int(r['hidden_count']),int(r['total_count'])
        if tot<=0 or not 0<=h<=tot:raise ValueError(f'line {line}: counts')
        if (d,s,e) in seen:raise ValueError(f'line {line}: duplicate')
        seen.add((d,s,e));t=int(r['treated']);cells[(d,g,e)][t].add(s);members[s].add((g,t));n+=1
    if not n:raise ValueError('empty input')
    missing={k:v for k,v in cells.items() if not(v[0] and v[1])}
    by_day=defaultdict(lambda:[0,0])
    for (d,g,e),v in cells.items():
        by_day[d][0]+=1;by_day[d][1]+=int(bool(v[0] and v[1]))
    sep=sum(d.month==9 and v[1]>0 for d,v in by_day.items())
    unstable=sorted(s for s,v in members.items() if len(v)>1)
    return {'observations':n,'total_cells':len(cells),'paired_cells':len(cells)-len(missing),
      'unpaired_cells':len(missing),'paired_fraction':(len(cells)-len(missing))/len(cells),
      'september_dates_with_pairs':sep,
      'dates_without_pairs':sorted(d.isoformat() for d,v in by_day.items() if v[1]==0),
      'unstable_security_membership':unstable,
      'unpaired_by_arm':{'control_only':sum(bool(v[0]) for v in missing.values()),
                         'treated_only':sum(bool(v[1]) for v in missing.values())},
      'paired_cells_by_date':[{'date':d.isoformat(),'total':v[0],'paired':v[1]} for d,v in sorted(by_day.items())],
      'estimation_ready':sep>=3 and not unstable and not missing,
      'warning':'Structural coverage only; no source authentication or causal inference.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('input_csv');p.add_argument('--output',required=True);a=p.parse_args()
    with open(a.input_csv,newline='',encoding='utf-8') as f:result=audit(csv.DictReader(f))
    with open(a.output,'w',encoding='utf-8') as f:json.dump(result,f,indent=2,sort_keys=True)
    if not result['estimation_ready']:raise SystemExit(2)
if __name__=='__main__':main()
