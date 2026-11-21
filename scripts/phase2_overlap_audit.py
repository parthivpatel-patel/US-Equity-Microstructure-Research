#!/usr/bin/env python3
"""Descriptive overlap diagnostics; archived processed panel only, no causal interpretation."""
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd

COLUMNS=('Ticker','treated','r_pre','v_pre','trades_pre','days_pre','days_post')
def audit(path):
    path=Path(path); digest=hashlib.sha256(path.read_bytes()).hexdigest()
    df=pd.read_csv(path)
    if not set(COLUMNS).issubset(df.columns): raise ValueError('Missing columns')
    if df.Ticker.isna().any() or df.Ticker.duplicated().any() or set(df.treated.unique())!={0,1}: raise ValueError('Invalid identifiers or treatment')
    if not np.isfinite(df[list(COLUMNS[2:])].to_numpy(dtype=float)).all(): raise ValueError('Nonfinite covariates')
    if (df[['r_pre','v_pre']]<0).any().any() or (df[['r_pre','v_pre']]>1).any().any(): raise ValueError('Invalid rate')
    if (df[['trades_pre','days_pre','days_post']]<=0).any().any(): raise ValueError('Invalid denominator')
    t=df[df.treated==1];c=df[df.treated==0]
    out={'source':'archived processed Phase 2 stock panel, not authenticated original SEC records','sha256':digest,'n_treated':len(t),'n_controls':len(c),'covariates':{}}
    for key in ('r_pre','v_pre','trades_pre'):
        a=t[key].to_numpy(dtype=float);b=c[key].to_numpy(dtype=float)
        av=np.log1p(a) if key=='trades_pre' else a
        bv=np.log1p(b) if key=='trades_pre' else b
        denom=math.sqrt((np.var(av,ddof=1)+np.var(bv,ddof=1))/2)
        out['covariates'][key]={
            'treated_median':float(np.median(a)),'control_median':float(np.median(b)),
            'standardized_mean_difference':float((av.mean()-bv.mean())/denom),
            'treated_outside_control_minmax':int(((a<b.min())|(a>b.max())).sum()),
            'controls_inside_treated_minmax':int(((b>=a.min())&(b<=a.max())).sum())}
    out['full_23_pre_19_post_days']={
        'treated':int(((t.days_pre==23)&(t.days_post==19)).sum()),
        'controls':int(((c.days_pre==23)&(c.days_post==19)).sum())}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('panel');p.add_argument('--expect-sha256');args=p.parse_args()
    x=audit(args.panel)
    if args.expect_sha256 and x['sha256']!=args.expect_sha256.lower():raise SystemExit('SHA256 mismatch')
    print(json.dumps(x,indent=2,sort_keys=True))
