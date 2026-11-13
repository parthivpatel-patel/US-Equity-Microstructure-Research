#!/usr/bin/env python3
"""Fail-closed security-date-exchange panel integrity audit; no causal estimation.

CSV required: security,date,exchange,hidden_count,trade_count,hidden_shares,total_shares,
 treated,match_group. Optional: source_id. All numeric observations are nonnegative
 integers, hidden quantities cannot exceed denominators. Dates ISO 8601.
"""
import csv
import datetime as dt
import json
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation

FIELDS=('security','date','exchange','hidden_count','trade_count','hidden_shares','total_shares','treated','match_group')
COUNTS=('hidden_count','trade_count','hidden_shares','total_shares')

def audit(rows):
    seen=set(); assignments={}; groups=defaultdict(set); dates=defaultdict(set)
    exchanges=set(); source_ids=set(); n=0
    for line,r in enumerate(rows,2):
        if not all(k in r for k in FIELDS): raise ValueError(f'line {line}: missing required columns')
        sec=r['security'].strip(); exc=r['exchange'].strip(); group=r['match_group'].strip()
        if not sec or not exc or not group: raise ValueError(f'line {line}: blank identifier')
        try:
            date=dt.date.fromisoformat(r['date'])
            if date.isoformat()!=r['date']: raise ValueError()
        except (ValueError,TypeError): raise ValueError(f'line {line}: invalid ISO date')
        key=(sec,date,exc)
        if key in seen: raise ValueError(f'line {line}: duplicate security-date-exchange')
        seen.add(key)
        if r['treated'] not in ('0','1'): raise ValueError(f'line {line}: treatment not binary')
        assignment=(r['treated'],group)
        if sec in assignments and assignments[sec]!=assignment:
            raise ValueError(f'line {line}: security treatment/match-group drift')
        assignments[sec]=assignment
        vals={}
        for k in COUNTS:
            try: v=Decimal(r[k])
            except (InvalidOperation,KeyError,TypeError): raise ValueError(f'line {line}: invalid {k}')
            if not v.is_finite() or v<0 or v!=v.to_integral_value():
                raise ValueError(f'line {line}: invalid {k}')
            vals[k]=v
        if vals['hidden_count']>vals['trade_count'] or vals['hidden_shares']>vals['total_shares']:
            raise ValueError(f'line {line}: hidden numerator exceeds denominator')
        if r.get('source_id','').strip(): source_ids.add(r['source_id'].strip())
        groups[group].add(r['treated']); dates[date].add(sec); exchanges.add(exc); n+=1
    if not n: raise ValueError('empty panel')
    incomplete=sorted(g for g,s in groups.items() if s!={'0','1'})
    return {'rows':n,'securities':len(assignments),'dates':len(dates),
            'exchanges':len(exchanges),'match_groups':len(groups),
            'incomplete_match_groups':incomplete,
            'source_ids_supplied':len(source_ids),
            'status':'BLOCK' if incomplete else 'STRUCTURAL_CHECKS_PASS',
            'authentication':'NOT_ESTABLISHED',
            'inference':'NOT_ESTABLISHED'}

if __name__=='__main__':
    with open(sys.argv[1],newline='',encoding='utf-8') as f:
        result=audit(csv.DictReader(f))
    print(json.dumps(result,indent=2))
    sys.exit(1 if result['status']=='BLOCK' else 0)
