#!/usr/bin/env python3
"""Compare published date-HAC and two-way standard errors, not raw-panel inference."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation

OUTCOMES=('count','volume')
PERIODS=('Jul-Sep','Jul-Oct')
LAGS=(0,3,5,10,15)
EXPECTED={(o,p,l) for o in OUTCOMES for p in PERIODS for l in LAGS}

def audit(rows):
    cells={}
    for row in rows:
        try:
            key=(row['outcome'],row['period'],int(row['hac_lag']))
            slope=Decimal(row['slope_pp_per_trading_day'])
            date_se=Decimal(row['date_hac_se'])
            two_se=Decimal(row['two_way_se'])
            dates=int(row['dates']);groups=int(row['groups'])
        except (KeyError,ValueError,InvalidOperation) as exc:
            raise ValueError('invalid row') from exc
        if key not in EXPECTED or key in cells:
            raise ValueError('unexpected or duplicate grid cell')
        if not all(v.is_finite() for v in (slope,date_se,two_se)) or min(date_se,two_se)<=0 or dates<2 or groups<2:
            raise ValueError('nonfinite or invalid numeric input')
        cells[key]=(slope,date_se,two_se,dates,groups)
    if set(cells)!=EXPECTED: raise ValueError('incomplete grid')
    report=[]
    for o in OUTCOMES:
        for p in PERIODS:
            group=[cells[o,p,l] for l in LAGS]
            if len({(v[0],v[3],v[4]) for v in group})!=1:
                raise ValueError('slope or sample count changes across covariance lags')
            ratios=[v[2]/v[1] for v in group]
            reversals=[]
            for lag,v in zip(LAGS,group):
                date_flag=abs(v[0])/v[1]>Decimal('1.96')
                two_flag=abs(v[0])/v[2]>Decimal('1.96')
                if date_flag!=two_flag: reversals.append(lag)
            report.append({'outcome':o,'period':p,'dates':group[0][3],'groups':group[0][4],
                'min_two_way_over_date_hac_se':str(round(min(ratios),6)),
                'max_two_way_over_date_hac_se':str(round(max(ratios),6)),
                'lags_two_way_se_smaller_than_date_hac':[lag for lag,r in zip(LAGS,ratios) if r<1],
                'lags_disagreeing_at_illustrative_1_96':reversals,
                'all_date_hac_ratios_above_1_96':all(abs(v[0])/v[1]>Decimal('1.96') for v in group),
                'all_two_way_ratios_above_1_96':all(abs(v[0])/v[2]>Decimal('1.96') for v in group)})
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_path');a=p.parse_args()
    with open(a.csv_path,encoding='utf-8',newline='') as f:
        print(json.dumps(audit(csv.DictReader(f)),indent=2))
