#!/usr/bin/env python3
"""Matched support attrition and leave-one-cluster-out descriptive diagnostics.

Input is NOT authenticated by this program. No inferential or causal claims.
"""
import csv, json, sys, math
from collections import defaultdict
from datetime import date

REQUIRED={'security','date','exchange','treated','match_group','numerator','denominator'}

def analyze(rows):
    cells=defaultdict(lambda:{'0':[0.,0.],'1':[0.,0.]})
    seen=set(); assignments={}; n=0
    for line,row in enumerate(rows,2):
        if not REQUIRED.issubset(row): raise ValueError(f'line {line}: missing columns')
        sec,day,ex,arm,group=(row[k].strip() for k in ('security','date','exchange','treated','match_group'))
        if not all((sec,day,ex,group)) or arm not in ('0','1'): raise ValueError(f'line {line}: invalid identifiers')
        try:
            if date.fromisoformat(day).isoformat()!=day: raise ValueError('noncanonical date')
            num,den=float(row['numerator']),float(row['denominator'])
        except (TypeError,ValueError) as err: raise ValueError(f'line {line}: invalid date or quantity') from err
        if not all(map(math.isfinite,(num,den))) or not (0<=num<=den) or den<=0:
            raise ValueError(f'line {line}: invalid numerator/denominator')
        key=(sec,day,ex)
        if key in seen: raise ValueError(f'line {line}: duplicate observation')
        seen.add(key)
        if sec in assignments and assignments[sec]!=(arm,group): raise ValueError(f'line {line}: assignment drift')
        assignments[sec]=(arm,group)
        sums=cells[(group,day,ex)][arm]; sums[0]+=num; sums[1]+=den; n+=1
    if not n: raise ValueError('empty panel')
    paired=[]; unsupported={'treated_only':0,'control_only':0}
    for (group,day,ex),arms in sorted(cells.items()):
        if arms['0'][1] and arms['1'][1]:
            diff=100*(arms['1'][0]/arms['1'][1]-arms['0'][0]/arms['0'][1])
            paired.append((group,day,ex,diff))
        else:
            unsupported['treated_only' if arms['1'][1] else 'control_only']+=1
    def estimate(items):
        groups=defaultdict(list)
        for group,day,ex,diff in items: groups[group].append(diff)
        return sum(sum(v)/len(v) for v in groups.values())/len(groups) if groups else None
    base=estimate(paired)
    groups=sorted({p[0] for p in paired}); dates=sorted({p[1] for p in paired})
    def summarize(values):
        valid=[v for v in values if v is not None]
        return {'defined':len(valid),'undefined':len(values)-len(valid),
                'min_pp':min(valid) if valid else None,'max_pp':max(valid) if valid else None,
                'sign_reversals':sum((v>0)!=(base>0) for v in valid) if base is not None and base!=0 else None}
    return {'status':'DESCRIPTIVE_ONLY','source_authenticated':False,'input_rows':n,
            'total_cells':len(cells),'paired_cells':len(paired),'unsupported_cells':unsupported,
            'paired_fraction':len(paired)/len(cells),'supported_groups':len(groups),
            'supported_dates':len(dates),'equal_group_pp':base,
            'leave_one_group_out':summarize([estimate([p for p in paired if p[0]!=g]) for g in groups]),
            'leave_one_date_out':summarize([estimate([p for p in paired if p[1]!=d]) for d in dates]),
            'inference':'NOT_COMPUTED: descriptive influence checks only'}

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: phase344_support_attrition.py AUTHORIZED_PANEL.csv')
    with open(sys.argv[1],newline='',encoding='utf-8') as f:
        print(json.dumps(analyze(csv.DictReader(f)),indent=2,sort_keys=True))
