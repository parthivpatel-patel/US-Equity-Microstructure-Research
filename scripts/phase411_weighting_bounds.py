"""Structural matched-cell weighting diagnostic. No source/treatment authentication."""
import csv,json,sys
from collections import defaultdict
from datetime import date

def audit(rows):
    cells=defaultdict(lambda:{0:[0,0],1:[0,0]}); seen=set(); errors=[]; count=0
    required=('date','match_group','exchange','treated','security','hidden_trades','total_trades')
    for count,r in enumerate(rows,1):
        try:
            if any(not str(r.get(k,'')).strip() for k in required): raise ValueError('missing field')
            d=date.fromisoformat(r['date']).isoformat()
            t=int(r['treated']); h=int(r['hidden_trades']); n=int(r['total_trades'])
            if t not in (0,1) or n<=0 or not 0<=h<=n: raise ValueError('invalid counts/treatment')
            g,e,s=(str(r[k]).strip() for k in ('match_group','exchange','security'))
            if (d,s,e) in seen: raise ValueError('duplicate security-exchange-date')
            seen.add((d,s,e)); v=cells[(d,g,e)][t]; v[0]+=h; v[1]+=n
        except (ValueError,TypeError,KeyError) as exc: errors.append(f'row {count}: {exc}')
    if errors or not cells: return dict(status='BLOCKED',errors=errors or ['empty input'])
    paired=[(k,v) for k,v in sorted(cells.items()) if v[0][1] and v[1][1]]
    if not paired: return dict(status='BLOCKED',errors=['no paired same-exchange group-date cells'])
    gaps=[v[1][0]/v[1][1]-v[0][0]/v[0][1] for _,v in paired]
    dates=defaultdict(list)
    for (d,_,_),v in paired: dates[d].append(v[1][0]/v[1][1]-v[0][0]/v[0][1])
    ht=sum(v[1][0] for _,v in paired); nt=sum(v[1][1] for _,v in paired)
    hc=sum(v[0][0] for _,v in paired); nc=sum(v[0][1] for _,v in paired)
    return dict(status='STRUCTURE_ONLY_NOT_AUTHENTICATED',paired_cells=len(paired),
        paired_dates=len(dates),all_exchange_group_date_cells=len(cells),
        equal_cell_gap_pp=100*sum(gaps)/len(gaps),
        date_balanced_gap_pp=100*sum(sum(v)/len(v) for v in dates.values())/len(dates),
        pooled_denominator_gap_pp=100*(ht/nt-hc/nc),
        source_authenticated=False,treatment_authenticated=False)
if __name__=='__main__':
    with open(sys.argv[1],newline='',encoding='utf-8-sig') as f: out=audit(csv.DictReader(f))
    print(json.dumps(out,indent=2,sort_keys=True))
    sys.exit(2 if out['status']=='BLOCKED' else 0)
