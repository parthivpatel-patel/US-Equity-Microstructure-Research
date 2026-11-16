"""Monthly matched-support attrition audit; structural only."""
import csv, json, sys
from collections import defaultdict
from datetime import date

def audit(rows):
    gd=defaultdict(lambda:{0:set(),1:set()})
    ex=defaultdict(lambda:{0:set(),1:set()})
    roster=defaultdict(lambda:{0:set(),1:set()})
    seen=set(); errors=[]; n=0
    for n,row in enumerate(rows,1):
        if any(not str(row.get(k,'')).strip() for k in ('date','security','exchange','treated','match_group')):
            errors.append(f'row {n}: missing field'); continue
        try:
            d=date.fromisoformat(row['date']).isoformat()
            t=int(row['treated'])
            if t not in (0,1): raise ValueError
        except (ValueError,TypeError):
            errors.append(f'row {n}: invalid date/treatment'); continue
        s,e,g=(str(row[k]).strip() for k in ('security','exchange','match_group'))
        if (d,s,e) in seen:
            errors.append(f'row {n}: duplicate date-security-exchange'); continue
        seen.add((d,s,e))
        gd[(d,g)][t].add(s); ex[(d,g,e)][t].add(s); roster[g][t].add(s)
    common={k for k,v in gd.items() if v[0] and v[1]}
    paired_ex={k for k,v in ex.items() if v[0] and v[1]}
    supported={(d,g) for d,g,e in paired_ex}
    monthly={}
    for month in sorted({d[:7] for d,g in gd}):
        keys={k for k in gd if k[0].startswith(month)}
        paired=keys & common
        same=paired & supported
        monthly[month]=dict(group_dates=len(keys),common_date=len(paired),
            same_exchange=len(same),lost_no_common_date=len(keys-paired),
            lost_no_same_exchange=len(paired-same))
    violations=sorted(g for g,v in roster.items() if len(v[1])!=1 or len(v[0])!=3)
    return dict(status='BLOCKED' if errors or not gd else 'STRUCTURE_ONLY_NOT_AUTHENTICATED',
        rows=n,group_dates=len(gd),common_date_group_dates=len(common),
        same_exchange_group_dates=len(common & supported),
        exchange_cells=len(ex),paired_exchange_cells=len(paired_ex),
        monthly=monthly,assumed_1_to_3_roster_violations=violations,
        errors=errors,source_authenticated=False,treatment_authenticated=False,
        note='1:3 is a diagnostic assumption, not an authenticated match roster')

if __name__=='__main__':
    with open(sys.argv[1],newline='',encoding='utf-8-sig') as f:
        result=audit(csv.DictReader(f))
    print(json.dumps(result,indent=2,sort_keys=True))
    sys.exit(2 if result['status']=='BLOCKED' else 0)
