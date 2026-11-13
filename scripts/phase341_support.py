#!/usr/bin/env python3
"""Matched-group common-date and exchange-support diagnostic; no effect estimation."""
import csv, json, sys
from collections import defaultdict
from datetime import date
REQUIRED={'security','date','exchange','treated','match_group'}
def audit(rows):
    assignments={}; observed=set()
    by_group=defaultdict(lambda:defaultdict(lambda:{'0':set(),'1':set()}))
    exchange_dates=defaultdict(lambda:defaultdict(lambda:{'0':set(),'1':set()}))
    for i,row in enumerate(rows,2):
        if not REQUIRED.issubset(row): raise ValueError(f'line {i}: missing columns')
        sec=row['security'].strip(); group=row['match_group'].strip(); ex=row['exchange'].strip(); t=row['treated']
        if not sec or not group or not ex or t not in ('0','1'): raise ValueError(f'line {i}: invalid identifiers/treatment')
        try:
            d=date.fromisoformat(row['date'])
            if d.isoformat()!=row['date']: raise ValueError()
        except (ValueError, TypeError): raise ValueError(f'line {i}: invalid date')
        key=(sec,d,ex)
        if key in observed: raise ValueError(f'line {i}: duplicate observation')
        observed.add(key)
        if sec in assignments and assignments[sec]!=(group,t): raise ValueError(f'line {i}: drifting group/treatment')
        assignments[sec]=(group,t)
        by_group[group][d][t].add(sec)
        exchange_dates[(group,ex)][d][t].add(sec)
    if not observed: raise ValueError('empty input')
    report=[]
    for group,dates in sorted(by_group.items()):
        paired=sum(bool(x['0']) and bool(x['1']) for x in dates.values())
        treated_only=sum(bool(x['1']) and not x['0'] for x in dates.values())
        control_only=sum(bool(x['0']) and not x['1'] for x in dates.values())
        report.append({'match_group':group,'union_dates':len(dates),'paired_dates':paired,'treated_only_dates':treated_only,'control_only_dates':control_only,'paired_date_fraction':round(paired/len(dates),6)})
    ex_report=[]
    for (group,ex),dates in sorted(exchange_dates.items()):
        ex_report.append({'match_group':group,'exchange':ex,'paired_dates':sum(bool(x['0']) and bool(x['1']) for x in dates.values()),'union_dates':len(dates)})
    return {'status':'SUPPORT_DIAGNOSTIC_ONLY','authentication':'NOT_ESTABLISHED','rows':len(observed),'groups':report,'group_exchange_support':ex_report,'zero_paired_groups':[r['match_group'] for r in report if r['paired_dates']==0]}
if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: phase341_support.py PANEL.csv')
    with open(sys.argv[1],newline='',encoding='utf-8') as f: print(json.dumps(audit(csv.DictReader(f)),indent=2))
