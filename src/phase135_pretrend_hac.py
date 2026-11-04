from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd

P=Path(__file__).resolve().parent
source=P/'phase131'/'daily_group_contrasts.csv'
df=pd.read_csv(source,parse_dates=['date'])
assert hashlib.sha256(source.read_bytes()).hexdigest()=='6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1'
assert len(df)==14416 and df.group.nunique()==68 and df.date.nunique()==106
assert not df.duplicated(['group','date','outcome']).any()
assert set(df.outcome)=={'count','volume'}
assert df.contrast.notna().all()
pre=df[df.date<pd.Timestamp('2025-11-03')]
assert pre.groupby(['date','outcome']).group.nunique().eq(68).all()
# For each pre-reform date, first aggregate across the same 68 matched groups.
# Newey-West covariance for an intercept and linear time trend, Bartlett lag 5.
def hac_fit(y,lag=5,t=None):
 n=len(y); t=np.arange(n,dtype=float) if t is None else np.asarray(t,dtype=float); X=np.column_stack([np.ones(n),t]); beta=np.linalg.lstsq(X,y,rcond=None)[0]; u=y-X@beta
 xx=np.linalg.inv(X.T@X)
 score=X*u[:,None]
 S=score.T@score
 for k in range(1,min(lag,n-1)+1):
  gamma=score[k:].T@score[:-k]
  S+=(1-k/(lag+1))*(gamma+gamma.T)
 cov=xx@S@xx*n/(n-2)
 se=np.sqrt(np.diag(cov))
 return beta,se
rows=[]; daily=pre.groupby(['date','outcome'],as_index=False).contrast.mean()
for outcome in ['count','volume']:
 d=daily[daily.outcome==outcome].sort_values('date')
 y=d.contrast.to_numpy(); beta,se=hac_fit(y)
 # Within pre-event dates: leave out each calendar month, recalculate trend.
 loo={}
 for month in sorted(d.date.dt.month.unique()):
  keep=(d.date.dt.month!=month).to_numpy()
  loo[str(month)]=float(hac_fit(y[keep],t=np.arange(len(y))[keep])[0][1])
 rows.append({'outcome':outcome,'pre_days':len(y),'pre_start':str(d.date.min().date()),'pre_end':str(d.date.max().date()),'daily_slope_pp':float(beta[1]),'hac5_se_pp':float(se[1]),'hac5_95ci_low_pp':float(beta[1]-1.96*se[1]),'hac5_95ci_high_pp':float(beta[1]+1.96*se[1]),'slope_20_days_pp':float(beta[1]*20),'leave_month_out_slopes_pp_per_day':json.dumps(loo,sort_keys=True)})
result=pd.DataFrame(rows)
result.to_csv(P/'phase135_pretrend_hac.csv',index=False,float_format='%.12g')
print(result.to_string(index=False))
print('source SHA256',hashlib.sha256(source.read_bytes()).hexdigest())
