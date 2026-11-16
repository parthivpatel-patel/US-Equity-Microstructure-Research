"""Read-only numerical audit of recovered Phase 2 security panel; no raw-data export."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

REQUIRED=('Ticker','treated','r_post','r_pre','v_post','v_pre','days_post','days_pre','trades_post','trades_pre','dr','dv')
def audit(path):
    path=Path(path); d=pd.read_csv(path)
    if any(c not in d for c in REQUIRED): raise ValueError('Missing columns')
    if d.empty or d.Ticker.isna().any() or d.Ticker.duplicated().any(): raise ValueError('Ticker integrity failure')
    if set(d.treated.unique())!={0,1}: raise ValueError('Treatment groups invalid')
    if not np.isfinite(d[list(REQUIRED[2:])].to_numpy(dtype=float)).all(): raise ValueError('Nonfinite')
    if any(not d[c].between(0,1).all() for c in ('r_pre','r_post','v_pre','v_post')): raise ValueError('Rate out of range')
    if (d[['days_pre','days_post','trades_pre','trades_post']]<=0).any().any(): raise ValueError('Nonpositive exposure')
    for c,post,pre in (('dr','r_post','r_pre'),('dv','v_post','v_pre')):
        if not np.allclose(d[c],d[post]-d[pre],atol=1e-10,rtol=0): raise ValueError('Difference mismatch')
    out={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rows':len(d),'treated':int(d.treated.sum()),'controls':int((d.treated==0).sum()),'warning':'Unmatched, descriptive, not causal or treatment-authenticated'}
    for y in ('dr','dv'):
        a=d.loc[d.treated==1,y].to_numpy();b=d.loc[d.treated==0,y].to_numpy()
        va=a.var(ddof=1)/len(a);vb=b.var(ddof=1)/len(b);se=float(np.sqrt(va+vb))
        if not np.isfinite(se) or se<=0: raise ValueError('Undefined Welch variance')
        df=(va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1))
        delta=float(a.mean()-b.mean());crit=student_t.ppf(.975,df)
        weighted=lambda g:float(np.average(g[y],weights=g.trades_pre))
        out[y]={'treated_mean':float(a.mean()),'control_mean':float(b.mean()),'difference':delta,'welch_se':se,'welch_ci95':[float(delta-crit*se),float(delta+crit*se)],'welch_p':float(2*student_t.sf(abs(delta/se),df)),'pretrade_weighted_difference':weighted(d[d.treated==1])-weighted(d[d.treated==0])}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');a=p.parse_args()
    print(json.dumps(audit(a.csv),indent=2,sort_keys=True))
