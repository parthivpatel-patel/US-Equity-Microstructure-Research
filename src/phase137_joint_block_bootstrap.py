"""Exploratory matched-group and shared-calendar moving-block residual bootstrap.
Input: archived, not source-authenticated processed group/date contrast panel.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
EXPECTED_SHA='6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1'
def slope_by_date(mat):
    y=mat.mean(axis=1); x=np.arange(len(y),dtype=float); xc=x-x.mean()
    return float(xc@y/(xc@xc))
def bootstrap(mat,block,draws,seed):
    t,g=mat.shape;x=np.arange(t,dtype=float);xc=x-x.mean()
    beta=slope_by_date(mat)
    resid=mat-mat.mean(axis=0)[None,:]-beta*xc[:,None]
    rng=np.random.default_rng(seed);slopes=np.empty(draws)
    for b in range(draws):
        groups=rng.integers(0,g,size=g)
        starts=rng.integers(0,t,size=(t+block-1)//block)
        dates=(starts[:,None]+np.arange(block)[None,:]).reshape(-1)[:t]%t
        y=beta*xc+resid[dates][:,groups].mean(axis=1)
        slopes[b]=float(xc@y/(xc@xc))
    low,high=np.quantile(slopes,[.025,.975])
    p=float(np.mean(np.abs(slopes-beta)>=abs(beta)))
    return beta,float(low),float(high),p
def run(src,out,draws=2000):
    actual=hashlib.sha256(src.read_bytes()).hexdigest()
    if actual!=EXPECTED_SHA:raise ValueError('Input SHA-256 mismatch; refuse unverified input')
    df=pd.read_csv(src,parse_dates=['date'])
    assert len(df)==14416 and df.groupby(['date','group','outcome']).size().eq(1).all()
    assert df.contrast.notna().all() and df.group.nunique()==68 and df.date.nunique()==106
    rows=[]
    for outcome in ('count','volume'):
        for period,cutoff in [('July-September','2025-10-01'),('July-October','2025-11-01')]:
            sub=df[(df.outcome==outcome)&(df.date<cutoff)]
            mat=sub.pivot(index='date',columns='group',values='contrast').sort_index()
            assert mat.shape[1]==68 and not mat.isna().any().any()
            for block in (3,5,10,15):
                seed=137000+(0 if outcome=='count' else 100)+(0 if period=='July-September' else 10)+block
                beta,low,high,p=bootstrap(mat.to_numpy(),block,draws,seed)
                rows.append(dict(outcome=outcome,period=period,dates=len(mat),groups=68,block_days=block,draws=draws,slope_pp_per_day=beta,bootstrap_95_low=low,bootstrap_95_high=high,centered_null_tail_fraction_exploratory=p,seed=seed))
    out.mkdir(parents=True,exist_ok=True)
    tab=pd.DataFrame(rows)
    tab.to_csv(out/'phase137_block_bootstrap.csv',index=False,float_format='%.12g')
    manifest=dict(input_sha256=actual,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),output_sha256=hashlib.sha256((out/'phase137_block_bootstrap.csv').read_bytes()).hexdigest(),draws_per_specification=draws,note='Processed data not authenticated; bootstrap is descriptive and not a causal identification test.')
    (out/'phase137_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(tab.to_string(index=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('output',type=Path);ap.add_argument('--draws',type=int,default=2000)
    a=ap.parse_args();run(a.input,a.output,a.draws)
