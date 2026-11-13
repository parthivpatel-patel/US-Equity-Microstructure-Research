#!/usr/bin/env python3
"""Sensitivity of published pretrend slope/SE ratios to reference cutoffs.
Not a replacement for cluster-robust finite-sample inference.
"""
import argparse
import csv
import json
import math

EXPECTED={(o,p,l) for o in ('count','volume') for p in ('Jul-Sep','Jul-Oct') for l in (0,3,5,10,15)}

def audit(rows, cutoffs=(1.96,2.0,2.1,2.2)):
    seen=set(); groups={}
    for row in rows:
        key=(row['outcome'],row['period'],int(row['hac_lag']))
        if key in seen: raise ValueError('duplicate grid cell')
        seen.add(key)
        slope=float(row['slope_pp_per_trading_day']); se=float(row['two_way_se'])
        n_dates=int(row['dates']); n_groups=int(row['groups'])
        if not all(math.isfinite(x) for x in (slope,se)) or se<=0 or n_dates<2 or n_groups<2:
            raise ValueError('invalid numeric value or count')
        g=groups.setdefault(key[:2],{'t':{},'dates':n_dates,'groups':n_groups})
        if g['dates']!=n_dates or g['groups']!=n_groups: raise ValueError('inconsistent cluster counts')
        g['t'][key[2]]=abs(slope)/se
    if seen!=EXPECTED: raise ValueError('missing/unexpected grid cell')
    out=[]
    for (outcome,period),g in sorted(groups.items()):
        t=g['t']; minimum=min(t.values()); weakest=min(t,key=t.get)
        out.append({'outcome':outcome,'period':period,'dates':g['dates'],'groups':g['groups'],
                    'minimum_abs_slope_over_se':round(minimum,6),'weakest_lag':weakest,
                    'all_lags_exceed':{str(c):all(v>c for v in t.values()) for c in cutoffs}})
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_path');a=p.parse_args()
    with open(a.csv_path,newline='',encoding='utf-8') as f:
        print(json.dumps(audit(csv.DictReader(f)),indent=2))
