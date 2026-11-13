#!/usr/bin/env python3
"""Aggregate-only nested-slope covariance tipping points. No causal inference."""
import csv, sys, json
from decimal import Decimal
def audit(rows, threshold=Decimal('1.96')):
    cells={}
    for r in rows:
        key=(r['outcome'],r['period'],int(r['hac_lag']))
        if key in cells or key[0] not in ('count','volume') or key[1] not in ('Jul-Sep','Jul-Oct') or key[2] not in (0,3,5,10,15):
            raise ValueError('duplicate/unexpected cell')
        slope=Decimal(r['slope_pp_per_trading_day']); se=Decimal(r['two_way_se'])
        if not slope.is_finite() or not se.is_finite() or se<=0: raise ValueError('invalid estimate')
        cells[key]=(slope,se,int(r['dates']),int(r['groups']))
    if len(cells)!=20: raise ValueError('incomplete grid')
    output=[]
    for outcome in ('count','volume'):
        for lag in (0,3,5,10,15):
            a,sa,na,ga=cells[outcome,'Jul-Sep',lag]; b,sb,nb,gb=cells[outcome,'Jul-Oct',lag]
            if (na,nb,ga,gb)!=(64,87,68,68): raise ValueError('unexpected sample metadata')
            if any(cells[outcome,p,k][0] != cells[outcome,p,lag][0] for p in ('Jul-Sep','Jul-Oct') for k in (0,3,5,10,15)): raise ValueError('slope varies with lag')
            delta=b-a
            tipping=(sa*sa+sb*sb-(delta/threshold)**2)/(2*sa*sb)
            output.append({'outcome':outcome,'lag':lag,'delta_pp_per_day':str(delta),
                'rho_tipping':str(round(tipping,6)),
                'classification': 'all admissible correlations' if tipping < -1 else ('no admissible correlations' if tipping >= 1 else 'depends on unknown correlation')})
    return output
if __name__=='__main__':
    with open(sys.argv[1],newline='',encoding='utf-8') as f: print(json.dumps(audit(csv.DictReader(f)),indent=2))
