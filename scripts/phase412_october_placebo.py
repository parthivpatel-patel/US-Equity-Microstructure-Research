"""October pre-reform matched-cell placebo. Structural only; no authentication."""
import csv,json,sys
from collections import defaultdict
from datetime import date

def audit(rows,cutoff='2025-10-15'):
    cut=date.fromisoformat(cutoff)
    if not date(2025,10,1)<cut<date(2025,11,3):
        return dict(status='BLOCKED',errors=['cutoff outside October'])
    cells=defaultdict(lambda:{0:[0,0],1:[0,0]});seen=set();errors=[]
    for i,r in enumerate(rows,1):
        try:
            d=date.fromisoformat(r['date'])
            if not date(2025,10,1)<=d<date(2025,11,3):continue
            t=int(r['treated']);h=int(r['hidden_trades']);n=int(r['total_trades'])
            g,e,s=(str(r[k]).strip() for k in ('match_group','exchange','security'))
            if not all((g,e,s)) or t not in (0,1) or n<=0 or not 0<=h<=n:raise ValueError('invalid values')
            key=(d.isoformat(),s,e)
            if key in seen:raise ValueError('duplicate security-exchange-date')
            seen.add(key);v=cells[(d.isoformat(),g,e)][t];v[0]+=h;v[1]+=n
        except (KeyError,ValueError,TypeError) as exc:errors.append(f'row {i}: {exc}')
    if errors:return dict(status='BLOCKED',errors=errors)
    paired=[(date.fromisoformat(k[0]),v) for k,v in cells.items() if v[0][1] and v[1][1]]
    before=[v for d,v in paired if d<cut];after=[v for d,v in paired if d>=cut]
    if not before or not after:return dict(status='BLOCKED',errors=['paired October cells needed on both sides'])
    def mean(vs):
        return 100*sum(v[1][0]/v[1][1]-v[0][0]/v[0][1] for v in vs)/len(vs)
    return dict(status='STRUCTURE_ONLY_NOT_AUTHENTICATED',cutoff=cutoff,
        paired_cells_before=len(before),paired_cells_after=len(after),
        equal_cell_gap_before_pp=mean(before),equal_cell_gap_after_pp=mean(after),
        placebo_change_pp=mean(after)-mean(before),
        source_authenticated=False,treatment_authenticated=False,inference_performed=False)
if __name__=='__main__':
    with open(sys.argv[1],newline='',encoding='utf-8-sig') as f:
        result=audit(csv.DictReader(f),sys.argv[2] if len(sys.argv)>2 else '2025-10-15')
    print(json.dumps(result,indent=2,sort_keys=True))
    sys.exit(2 if result['status']=='BLOCKED' else 0)
