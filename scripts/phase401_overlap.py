"""Baseline imbalance and overlap audit for recovered Phase 2 security panel.
Usage: python scripts/phase401_overlap.py local_panel.csv
Requires pandas and numpy. No data bundled.
"""
import sys
import numpy as np
import pandas as pd

def audit(df):
    required={'Ticker','treated','r_pre','v_pre','trades_pre','dr','dv'}
    if not required.issubset(df): raise ValueError('Missing columns: '+str(sorted(required-set(df))))
    if df.Ticker.isna().any() or df.Ticker.duplicated().any(): raise ValueError('Duplicate/missing ticker')
    if not df.treated.isin([0,1]).all() or df.treated.nunique()!=2: raise ValueError('Invalid groups')
    if not np.isfinite(df[['r_pre','v_pre','trades_pre','dr','dv']].to_numpy(dtype=float)).all(): raise ValueError('Nonfinite values')
    if (df.trades_pre<0).any() or ((df[['r_pre','v_pre']]<0)|(df[['r_pre','v_pre']]>1)).any().any(): raise ValueError('Invalid baseline')
    df=df.copy(); df['logtrades']=np.log1p(df.trades_pre)
    results=[]
    for name in ['r_pre','v_pre','logtrades']:
        a=df.loc[df.treated==1,name]; b=df.loc[df.treated==0,name]
        smd=(a.mean()-b.mean())/np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
        results.append(('balance',name,len(a),len(b),float(a.mean()),float(b.mean()),float(smd)))
    for outcome,baseline in [('dr','r_pre'),('dv','v_pre')]:
        df['quartile']=pd.qcut(df[baseline],4,labels=False,duplicates='drop')
        for q,g in df.groupby('quartile'):
            a=g.loc[g.treated==1,outcome];b=g.loc[g.treated==0,outcome]
            results.append(('quartile_'+str(q),outcome,len(a),len(b),float(a.mean()-b.mean()) if len(a) and len(b) else None,None,None))
    return results

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Provide local panel CSV path')
    for row in audit(pd.read_csv(sys.argv[1])): print(','.join('NA' if x is None else str(x) for x in row))
