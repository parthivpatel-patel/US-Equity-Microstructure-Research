"""Pre-reform matched-cell daily series and September slope diagnostic.

Input CSV columns: date,security,exchange,match_group,treated,hidden_count,total_count.
No historical observations are bundled. Dates before 2025-11-03 only.
"""
import argparse
import csv
import datetime as dt
import json
from collections import defaultdict

COLUMNS = {'date','security','exchange','match_group','treated','hidden_count','total_count'}

def analyze(rows):
    cells = defaultdict(lambda: {0: [0,0], 1: [0,0]})
    seen = set()
    for r in rows:
        if not COLUMNS.issubset(r):
            raise ValueError('missing required columns')
        day = dt.date.fromisoformat(r['date'])
        if not (dt.date(2025,9,1) <= day < dt.date(2025,11,3)):
            raise ValueError('date outside September-October pre-reform window')
        t = r['treated']
        if t not in ('0','1'):
            raise ValueError('treated must be 0 or 1')
        key = (day,r['security'],r['exchange'])
        if key in seen:
            raise ValueError('duplicate security-exchange-date')
        seen.add(key)
        n,h = int(r['total_count']),int(r['hidden_count'])
        if n <= 0 or not 0 <= h <= n:
            raise ValueError('invalid counts')
        if not all(r[k].strip() for k in ('security','exchange','match_group')):
            raise ValueError('empty identifier')
        a = cells[(day,r['match_group'],r['exchange'])][int(t)]
        a[0] += h; a[1] += n
    by_day = defaultdict(list)
    for (day,group,exchange), arms in cells.items():
        if arms[0][1] and arms[1][1]:
            by_day[day].append(arms[1][0]/arms[1][1] - arms[0][0]/arms[0][1])
    series = [(day,sum(vals)/len(vals),len(vals)) for day,vals in sorted(by_day.items())]
    september = [(day,y) for day,y,_ in series if day.month == 9]
    if len(september) < 3:
        raise ValueError('at least three September paired trading dates required')
    x = [(d-september[0][0]).days for d,_ in september]
    y = [v for _,v in september]
    mx,my = sum(x)/len(x),sum(y)/len(y)
    den = sum((v-mx)**2 for v in x)
    slope = sum((a-mx)*(b-my) for a,b in zip(x,y))/den
    return {'september_slope_per_calendar_day':slope,
            'september_paired_dates':len(september),
            'total_paired_dates':len(series),
            'daily': [{'date':d.isoformat(),'matched_cell_mean_difference':v,'paired_cells':n} for d,v,n in series],
            'interpretation':'Descriptive only; no standard error, placebo correction or causal identification.'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('input_csv');p.add_argument('--output',required=True)
    a=p.parse_args()
    with open(a.input_csv,newline='') as f: result=analyze(csv.DictReader(f))
    with open(a.output,'w') as f: json.dump(result,f,indent=2)

if __name__=='__main__':main()
