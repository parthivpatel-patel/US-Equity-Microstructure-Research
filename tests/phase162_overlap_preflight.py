"""Phase 162: baseline overlap and weight concentration admission checks.
Usage: python tests/phase162_overlap_preflight.py /path/to/archived_panel.csv
No market data distributed.
"""
import sys, math, json
import pandas as pd
def run(path):
    p=pd.read_csv(path)
    cols=['Ticker','treated','r_pre','r_post','v_pre','v_post','dr','dv','trades_pre','trades_post']
    if any(c not in p for c in cols): raise ValueError('missing required columns')
    if p.empty or p[cols].isna().any().any() or not p.Ticker.is_unique: raise ValueError('invalid rows or duplicate tickers')
    if not p.treated.isin([0,1]).all() or set(p.treated.unique())!={0,1}: raise ValueError('treatment groups invalid')
    for c in cols[2:]:
        if not pd.api.types.is_numeric_dtype(p[c]) or not p[c].map(math.isfinite).all(): raise ValueError('nonfinite or nonnumeric '+c)
    for c in ['r_pre','r_post','v_pre','v_post']:
        if not p[c].between(0,1).all(): raise ValueError('invalid rate '+c)
    if not (p[['trades_pre','trades_post']]>0).all().all(): raise ValueError('invalid weights')
    if not ((p.dr-(p.r_post-p.r_pre)).abs()<=1e-9).all(): raise ValueError('dr inconsistent')
    if not ((p.dv-(p.v_post-p.v_pre)).abs()<=1e-9).all(): raise ValueError('dv inconsistent')
    a=p[p.treated==1];b=p[p.treated==0]
    out={'n':len(p),'treated':len(a),'comparison':len(b),'baseline_support':{},'weight_concentration':{}}
    for c in ['r_pre','v_pre']:
        lo=max(a[c].min(),b[c].min());hi=min(a[c].max(),b[c].max())
        out['baseline_support'][c]={'overlap':bool(lo<=hi),'common_min':float(lo) if lo<=hi else None,'common_max':float(hi) if lo<=hi else None,'treated_outside':int((~a[c].between(lo,hi)).sum()) if lo<=hi else len(a),'comparison_outside':int((~b[c].between(lo,hi)).sum()) if lo<=hi else len(b)}
    for label,g in [('treated',a),('comparison',b)]:
        w=g[['trades_pre','trades_post']].min(axis=1).to_numpy(dtype=float);z=w/w.max();s=math.fsum(z);sq=math.fsum(x*x for x in z)
        out['weight_concentration'][label]={'n':len(g),'ess':s*s/sq,'largest_share':1/s}
    return out
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Pass archived panel CSV path')
    print(json.dumps(run(sys.argv[1]),indent=2,sort_keys=True))
