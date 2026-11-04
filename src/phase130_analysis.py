import pandas as pd,numpy as np,hashlib,json
from pathlib import Path
p=Path(__file__).parent
src=p/'daily_group_contrasts.csv'
df=pd.read_csv(src,parse_dates=['date'])
assert len(df)==14416 and df.group.nunique()==68 and df.outcome.nunique()==2
assert not df.duplicated(['group','date','outcome']).any()
dates=sorted(df.date.unique()); groups=sorted(df.group.unique()); outputs=[]; pergroup=[]
for outcome in ['count','volume']:
 d=df[df.outcome==outcome].pivot(index='date',columns='group',values='contrast').reindex(index=dates,columns=groups)
 assert d.notna().all().all()
 for i in range(5,len(d)-4):
  date=pd.Timestamp(d.index[i]); pre=d.iloc[i-5:i].mean(axis=0); post=d.iloc[i:i+5].mean(axis=0)
  changes=(post-pre); val=changes.mean()
  outputs.append(dict(outcome=outcome,event_date=date.date().isoformat(),estimate_pp=val,groups=len(changes),pre_start=pd.Timestamp(d.index[i-5]).date().isoformat(),post_end=pd.Timestamp(d.index[i+4]).date().isoformat(),is_prereform_placebo=bool(pd.Timestamp(d.index[i+4])<pd.Timestamp('2025-11-03'))))
  if date in [pd.Timestamp('2025-10-06'),pd.Timestamp('2025-11-03')]:
   pergroup.extend(dict(outcome=outcome,event_date=date.date().isoformat(),group=g,change_pp=float(v)) for g,v in changes.items())
scan=pd.DataFrame(outputs);scan.to_csv(p/'event_scan.csv',index=False)
g=pd.DataFrame(pergroup);g.to_csv(p/'oct_nov_group_changes.csv',index=False)
summary=[]
for outcome in ['count','volume']:
 s=scan[scan.outcome==outcome]; pre=s[s.is_prereform_placebo]; nov=s[s.event_date=='2025-11-03']; octo=s[s.event_date=='2025-10-06']
 assert len(nov)==len(octo)==1
 nv=float(nov.estimate_pp.iloc[0]); oc=float(octo.estimate_pp.iloc[0]);
 summary.append(dict(outcome=outcome,november_pp=nv,october_pp=oc,nov_minus_oct_pp=nv-oc,pre_placebo_n=len(pre),pre_placebo_at_least_as_negative=int((pre.estimate_pp<=nv).sum()),pre_placebo_at_least_as_extreme_absolute=int((pre.estimate_pp.abs()>=abs(nv)).sum()),pre_placebo_min_pp=float(pre.estimate_pp.min()),pre_placebo_max_pp=float(pre.estimate_pp.max())))
pd.DataFrame(summary).to_csv(p/'summary.csv',index=False)
manifest={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':len(df),'groups':len(groups),'dates':len(dates),'event_window_trading_days':5,'pre_reform_placebo_requires_post_window_before':'2025-11-03','outputs':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [p/'event_scan.csv',p/'oct_nov_group_changes.csv',p/'summary.csv']}}
(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(pd.DataFrame(summary).to_string(index=False));print('event rows',len(scan),'placebo per outcome',len(scan[(scan.outcome=='count')&scan.is_prereform_placebo]))
# Exploratory matched-group bootstrap; does not preserve date-level uncertainty.
rng=np.random.default_rng(1302026); rows=[]
for outcome in ['count','volume']:
 sub=g[g.outcome==outcome].pivot(index='group',columns='event_date',values='change_pp').reindex(groups)
 diff=(sub['2025-11-03']-sub['2025-10-06']).to_numpy(); B=10000
 indices=rng.integers(0,len(diff),size=(B,len(diff)))
 boot=diff[indices].mean(axis=1)
 loo=(diff.sum()-diff)/(len(diff)-1)
 rows.append(dict(outcome=outcome,difference_pp=diff.mean(),group_bootstrap_ci_low=np.quantile(boot,.025),group_bootstrap_ci_high=np.quantile(boot,.975),leave_one_group_out_min=loo.min(),leave_one_group_out_max=loo.max(),draws=B))
pd.DataFrame(rows).to_csv(p/'group_sensitivity.csv',index=False)
manifest['outputs']['group_sensitivity.csv']=hashlib.sha256((p/'group_sensitivity.csv').read_bytes()).hexdigest()
(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(pd.DataFrame(rows).to_string(index=False))
