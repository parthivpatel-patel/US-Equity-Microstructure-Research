"""Pilot contrast leave-one-date-out stability; descriptive only, no causal inference."""
import argparse, json
import numpy as np
import pandas as pd
METRICS={'trade':('Hidden','TradesForHidden'),'volume':("HiddenVol('000)","TradeVolForHidden('000)")}
def analyze(df):
    required={'Date','lot',*sum((list(x) for x in METRICS.values()),[])}
    if not required.issubset(df.columns): raise ValueError('missing fields')
    d=df.copy();d['Date']=pd.to_numeric(d.Date,errors='raise').astype(int);d['lot']=pd.to_numeric(d.lot,errors='raise').astype(int)
    if d.duplicated(['Date','lot']).any() or d.groupby('Date').lot.apply(lambda x:set(x)!={10,40,100}).any():raise ValueError('incomplete or duplicate date tiers')
    for n,den in METRICS.values():
        if not np.isfinite(d[[n,den]].to_numpy(float)).all() or (d[n]<0).any() or (d[den]<=0).any() or (d[n]>d[den]).any():raise ValueError('invalid counts')
    periods={'early_oct':d.Date.between(20251001,20251015),'late_oct':d.Date.between(20251016,20251031),'nov':d.Date.between(20251103,20251130)}
    if sum(periods.values()).ne(1).any():raise ValueError('unassigned dates')
    def rate(x,n,den):
        a=x.loc[x.lot.isin([10,40])];b=x.loc[x.lot.eq(100)]
        return a[n].sum()/a[den].sum()-b[n].sum()/b[den].sum()
    result=[]
    for metric,(n,den) in METRICS.items():
        for name,left,right in [('oct_placebo','early_oct','late_oct'),('nov_vs_late_oct','late_oct','nov')]:
            a=d.loc[periods[left]];b=d.loc[periods[right]]
            if a.empty or b.empty:raise ValueError('empty period')
            point=100*(rate(b,n,den)-rate(a,n,den))
            vals=[]
            for date in sorted(set(a.Date)|set(b.Date)):
                aa=a.loc[a.Date.ne(date)];bb=b.loc[b.Date.ne(date)]
                if aa.empty or bb.empty:raise ValueError('too few dates')
                vals.append((int(date),100*(rate(bb,n,den)-rate(aa,n,den))))
            biggest=max(vals,key=lambda z:abs(z[1]-point))
            result.append({'metric':metric,'comparison':name,'estimate_pp':round(float(point),6),'n_left_dates':int(a.Date.nunique()),'n_right_dates':int(b.Date.nunique()),'leave_one_date_min_pp':round(min(v for _,v in vals),6),'leave_one_date_max_pp':round(max(v for _,v in vals),6),'largest_influence_date':biggest[0],'largest_abs_shift_pp':round(abs(biggest[1]-point),6),'sign_flips':int(sum(np.sign(v)!=np.sign(point) for _,v in vals))})
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');args=p.parse_args();print(json.dumps(analyze(pd.read_csv(args.csv)),indent=2))
