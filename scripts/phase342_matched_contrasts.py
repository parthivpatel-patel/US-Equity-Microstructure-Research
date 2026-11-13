#!/usr/bin/env python3
"""Descriptive matched-group/date/exchange contrasts; not causal inference."""
import csv, json, math, sys
from collections import defaultdict
from datetime import date

REQUIRED={'security','date','exchange','treated','match_group','numerator','denominator'}

def analyze(rows):
    strata=defaultdict(lambda:{'0':[],'1':[]})
    seen=set()
    assignments={}
    for line,row in enumerate(rows,2):
        if not REQUIRED.issubset(row): raise ValueError(f'line {line}: missing columns')
        sec,ex,group,day,arm=(row[k].strip() for k in ('security','exchange','match_group','date','treated'))
        if not sec or not ex or not group or arm not in ('0','1'): raise ValueError(f'line {line}: invalid identifier/treatment')
        try:
            d=date.fromisoformat(day)
            if d.isoformat()!=day: raise ValueError()
            n,den=float(row['numerator']),float(row['denominator'])
        except (TypeError,ValueError): raise ValueError(f'line {line}: invalid date/quantity')
        if not math.isfinite(n) or not math.isfinite(den) or den<=0 or n<0 or n>den:
            raise ValueError(f'line {line}: invalid numerator/denominator')
        key=(sec,day,ex)
        if key in seen: raise ValueError(f'line {line}: duplicate observation')
        seen.add(key)
        if sec in assignments and assignments[sec]!=(group,arm): raise ValueError(f'line {line}: assignment drift')
        assignments[sec]=(group,arm)
        strata[(group,day,ex)][arm].append((n,den))
    if not seen: raise ValueError('empty panel')
    group_values=defaultdict(list)
    paired=unpaired=0
    for (group,day,ex),arms in sorted(strata.items()):
        if not arms['0'] or not arms['1']:
            unpaired+=1
            continue
        ratios={a:sum(n for n,d in arms[a])/sum(d for n,d in arms[a]) for a in ('0','1')}
        group_values[group].append(100*(ratios['1']-ratios['0']))
        paired+=1
    means={g:sum(v)/len(v) for g,v in sorted(group_values.items())}
    return {'status':'DESCRIPTIVE_ONLY_NOT_CAUSAL','source_authenticated':False,
        'input_rows':len(seen),'paired_strata':paired,'unpaired_strata':unpaired,
        'supported_groups':len(means),'equal_group_mean_difference_pp':sum(means.values())/len(means) if means else None,
        'group_mean_differences_pp':means,
        'inference':'NOT_COMPUTED: date, exchange, group and serial dependence unresolved'}

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: phase342_matched_contrasts.py AUTHORIZED_PANEL.csv')
    with open(sys.argv[1],newline='',encoding='utf-8') as f:
        print(json.dumps(analyze(csv.DictReader(f)),indent=2,sort_keys=True))
