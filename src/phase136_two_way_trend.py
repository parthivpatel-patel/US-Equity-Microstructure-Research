"""Exploratory group-cluster plus common-date HAC uncertainty for linear pretrends.
Input: recovered Phase 131 daily_group_contrasts.csv (NOT yet publicly released).
Run: python src/phase136_two_way_trend.py /path/to/daily_group_contrasts.csv
Requires numpy and pandas. This is not a causal identification procedure.
"""
import sys,hashlib
from pathlib import Path
import numpy as np,pandas as pd
EXPECTED="6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1"
def nw(s,L):
    v=float(s@s)
    for k in range(1,min(L,len(s)-1)+1):
        v+=2*(1-k/(L+1))*float(s[k:]@s[:-k])
    return v
def calc(y,L):
    G,T=y.shape
    x=np.arange(T,dtype=float);x-=x.mean()
    d=y-y.mean(axis=1,keepdims=True)
    den=G*(x@x);b=float((d*x).sum()/den)
    e=d-b*x
    cell=e*x
    sg=cell.sum(axis=1);st=cell.sum(axis=0)
    vg=float(sg@sg)/den**2
    vd=nw(st,L)/den**2
    vc=float((cell**2).sum())/den**2
    v=vg+vd-vc
    return b,np.sqrt(max(0,vd)),np.sqrt(v) if v>=0 else np.nan,v
def main():
    p=Path(sys.argv[1]);assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED
    df=pd.read_csv(p,parse_dates=['date'])
    assert df.shape==(14416,5)
    assert not df.duplicated(['group','date','outcome']).any()
    assert df.contrast.notna().all() and np.isfinite(df.contrast).all()
    assert df.group.nunique()==68 and df.date.nunique()==106
    assert set(df.outcome)=={'count','volume'}
    assert (df.month==df.date.dt.month).all()
    assert df.groupby(['outcome','group']).date.nunique().eq(106).all()
    rows=[]
    for outcome in ['count','volume']:
        for label,end in [('Jul-Oct','2025-11-03'),('Jul-Sep','2025-10-01')]:
            d=df[(df.outcome==outcome)&(df.date<end)]
            w=d.pivot(index='group',columns='date',values='contrast').sort_index().sort_index(axis=1)
            assert w.shape[0]==68 and not w.isna().any().any()
            for lag in [0,3,5,10,15]:
                b,sd,st,v=calc(w.to_numpy(),lag)
                rows.append(dict(outcome=outcome,period=label,dates=w.shape[1],groups=68,hac_lag=lag,slope_pp_per_trading_day=b,date_hac_se=sd,two_way_se=st,two_way_variance=v,two_way_ci_low=b-1.96*st,two_way_ci_high=b+1.96*st))
    out=Path('results/phase136_trend_uncertainty.csv');out.parent.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(out,index=False,float_format='%.12g')
    print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':main()
