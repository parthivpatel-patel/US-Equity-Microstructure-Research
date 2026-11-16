"""Descriptive October 2025 pre-reform daily trend; not a causal estimator."""
import argparse
import csv
import numpy as np
import statsmodels.api as sm

FIELDS = [('Hidden','TradesForHidden','trade'), ("HiddenVol('000)","TradeVolForHidden('000)",'volume')]

def analyze(path):
    with open(path, newline='') as handle:
        rows=list(csv.DictReader(handle))
    days={}
    for r in rows:
        date=r['Date']; lot=int(float(r['lot']))
        if date[:6]!='202510': continue
        if (date,lot) in days: raise ValueError('duplicate date/lot')
        days[date,lot]=r
        for n,d,_ in FIELDS:
            if not (0<=float(r[n])<=float(r[d]) and float(r[d])>0):raise ValueError('invalid rate')
    dates=sorted({d for d,l in days})
    if any(set(l for d,l in days if d==date)!={10,40,100} for date in dates):raise ValueError('incomplete date')
    if len(dates)<8:raise ValueError('too few dates')
    result={}
    for n,d,name in FIELDS:
        diffs=[]
        for date in dates:
            small=[days[date,l] for l in (10,40)]
            a=sum(float(r[n]) for r in small)/sum(float(r[d]) for r in small)
            b=float(days[date,100][n])/float(days[date,100][d])
            diffs.append(a-b)
        x=np.arange(len(dates),dtype=float)
        model=sm.OLS(diffs,sm.add_constant(x)).fit(cov_type='HAC',cov_kwds={'maxlags':5})
        result[name]={'n_dates':len(dates),'start_pp':100*diffs[0],'end_pp':100*diffs[-1], 'slope_pp_per_session':100*float(model.params[1]), 'hac_se_pp':100*float(model.bse[1]),'hac_p':float(model.pvalues[1]),'min_pp':100*min(diffs),'max_pp':100*max(diffs)}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');a=p.parse_args()
    import json
    print(json.dumps(analyze(a.csv),indent=2))
