"""Phase 139: paired piecewise residual bootstrap; processed panel, not SEC-authenticated."""
import argparse, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
EXPECTED = "6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1"
def slope(a):
    x=np.arange(len(a),dtype=float); x-=x.mean()
    return float(x@a.mean(axis=1)/(x@x))
def run(src,out,draws=2000):
    if hashlib.sha256(src.read_bytes()).hexdigest()!=EXPECTED:
        raise ValueError("Processed input hash mismatch")
    df=pd.read_csv(src,parse_dates=["date"])
    assert len(df)==14416 and df.groupby(["date","group","outcome"]).size().eq(1).all()
    rows=[]
    for outcome in ("count","volume"):
        tab=df[(df.outcome==outcome)&(df.date<"2025-11-01")].pivot(index="date",columns="group",values="contrast").sort_index()
        a=tab.to_numpy();t,g=a.shape;n0=int((tab.index<"2025-10-01").sum())
        assert (t,g,n0)==(87,68,64) and np.isfinite(a).all()
        fit=np.empty_like(a)
        for s,e in ((0,n0),(n0,t)):
            x=np.arange(e-s,dtype=float);xc=x-x.mean()
            avg=a[s:e].mean(axis=0)
            beta=(xc[:,None]*(a[s:e]-avg)).sum(axis=0)/(xc@xc)
            fit[s:e]=avg[None,:]+xc[:,None]*beta[None,:]
        residual=a-fit
        b0=slope(a[:n0]);b1=slope(a[n0:]);delta=b1-b0
        for block in (3,5,10,15):
            seed=139000+(100 if outcome=="volume" else 0)+block
            rng=np.random.default_rng(seed);vals=np.empty(draws)
            for i in range(draws):
                gi=rng.integers(g,size=g)
                starts=rng.integers(t,size=(t+block-1)//block)
                ti=((starts[:,None]+np.arange(block)[None,:]).reshape(-1)[:t])%t
                synth=fit[:,gi]+residual[ti][:,gi]
                vals[i]=slope(synth[n0:])-slope(synth[:n0])
            lo,hi=np.quantile(vals,[.025,.975])
            rows.append(dict(outcome=outcome,days_jul_sep=n0,days_oct=t-n0,groups=g,block_days=block,draws=draws,jul_sep_slope_pp_day=b0,oct_slope_pp_day=b1,oct_minus_jul_sep_slope_pp_day=delta,bootstrap_95_low=float(lo),bootstrap_95_high=float(hi),bootstrap_sd=float(vals.std(ddof=1)),seed=seed))
    out.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out,index=False,float_format="%.12g")
    print(pd.DataFrame(rows).to_string(index=False))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path);p.add_argument("output",type=Path)
    p.add_argument("--draws",type=int,default=2000)
    a=p.parse_args();run(a.input,a.output,a.draws)
