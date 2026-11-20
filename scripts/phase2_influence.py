#!/usr/bin/env python3
"""Security-level influence and pre-period liquidity overlap on archived processed panel.
No raw SEC verification, serial-dependence inference, or causal identification.
"""
import argparse, csv, hashlib, json, math
from pathlib import Path

def compute(path):
    b=Path(path).read_bytes(); h=hashlib.sha256(b).hexdigest()
    with Path(path).open(newline='') as f:
        rows=list(csv.DictReader(f))
    if not rows or len(set(x['Ticker'] for x in rows))!=len(rows): raise ValueError('duplicate or empty tickers')
    for x in rows:
        if x['treated'] not in ('0','1'):raise ValueError('bad treatment')
        for k in ('dr','dv','trades_pre','r_pre','v_pre'):
            x[k]=float(x[k])
            if not math.isfinite(x[k]):raise ValueError('nonfinite')
        if x['trades_pre']<=0:raise ValueError('bad trades')
    t=[x for x in rows if x['treated']=='1']; c=[x for x in rows if x['treated']=='0']
    if len(t)<2 or len(c)<2:raise ValueError('insufficient groups')
    def avg(a,k,w=False):
        return math.fsum(x[k]*(x['trades_pre'] if w else 1) for x in a)/math.fsum(x['trades_pre'] if w else 1 for x in a)
    out={'input_sha256':h,'n_treated':len(t),'n_control':len(c),'scope':'archived processed security panel; not source authenticated or causal'}
    for k in ('dr','dv'):
        base=100*(avg(t,k)-avg(c,k)); weighted=100*(avg(t,k,True)-avg(c,k,True))
        t_loo=[100*(avg([z for z in t if z is not x],k)-avg(c,k)) for x in t]
        c_loo=[100*(avg(t,k)-avg([z for z in c if z is not x],k)) for x in c]
        t_weight_loo=[100*(avg([z for z in t if z is not x],k,True)-avg(c,k,True)) for x in t]
        influence=sorted(((abs(v-weighted),x['Ticker'],v) for x,v in zip(t,t_weight_loo)),reverse=True)
        out[k]={'equal_security_gap_pp':base,'pretrade_weighted_gap_pp':weighted,
                'treated_leave_one_out_equal_pp_range':[min(t_loo),max(t_loo)],
                'control_leave_one_out_equal_pp_range':[min(c_loo),max(c_loo)],
                'treated_leave_one_out_weighted_pp_range':[min(t_weight_loo),max(t_weight_loo)],
                'top_5_treated_weight_influence': [{'ticker':ticker,'abs_change_pp':delta,'leave_one_out_gap_pp':v} for delta,ticker,v in influence[:5]]}
    wt=sorted(t,key=lambda x:x['trades_pre'],reverse=True)
    wc=sorted(c,key=lambda x:x['trades_pre'],reverse=True)
    for name,a in [('treated',wt),('control',wc)]:
        total=math.fsum(x['trades_pre'] for x in a)
        out[name+'_pretrade_weight_concentration']={'top1_share':a[0]['trades_pre']/total,
           'top5_share':math.fsum(x['trades_pre'] for x in a[:5])/total}
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('panel');a=p.parse_args()
    print(json.dumps(compute(a.panel),indent=2,sort_keys=True))
