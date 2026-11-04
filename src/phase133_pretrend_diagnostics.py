"""Descriptive pre-event and leave-one-group-out checks; not causal inference.
Usage: python src/phase133_pretrend_diagnostics.py path/to/daily_group_contrasts.csv
"""
import sys, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
source=Path(sys.argv[1])
df=pd.read_csv(source,parse_dates=["date"])
assert len(df)==14416 and not df.duplicated(["group","date","outcome"]).any()
assert df.groupby(["outcome","date"]).size().eq(68).all()
assert set(df.outcome)=={"count","volume"}
assert df.contrast.notna().all() and np.isfinite(df.contrast).all()
rows=[]; diag=[]
for outcome in ["count","volume"]:
 d=df[df.outcome==outcome].pivot(index="date",columns="group",values="contrast").sort_index()
 assert d.shape==(106,68) and d.notna().all().all()
 for date in ["2025-10-06","2025-11-03"]:
  i=d.index.get_loc(pd.Timestamp(date))
  assert i>=5 and i+5<=len(d)
  pre=d.iloc[i-5:i]; post=d.iloc[i:i+5]
  change=post.mean()-pre.mean()
  loo=(change.sum()-change)/67
  diag.append(dict(outcome=outcome,event=date,estimate_pp=change.mean(),median_group_pp=change.median(),positive_groups=int((change>0).sum()),negative_groups=int((change<0).sum()),min_leave_one_out_pp=loo.min(),max_leave_one_out_pp=loo.max(),pre_start=str(pre.index[0].date()),post_end=str(post.index[-1].date())))
 for month,grp in d.groupby(d.index.to_period("M")):
  avg=grp.mean(axis=0)
  rows.append(dict(outcome=outcome,month=str(month),days=len(grp),mean_group_contrast_pp=avg.mean(),median_group_contrast_pp=avg.median(),cross_group_sd_pp=avg.std(ddof=1)))
 aug=d[d.index.month==8].mean(axis=0); sep=d[d.index.month==9].mean(axis=0)
 ch=sep-aug; loo=(ch.sum()-ch)/67
 diag.append(dict(outcome=outcome,event="September minus August",estimate_pp=ch.mean(),median_group_pp=ch.median(),positive_groups=int((ch>0).sum()),negative_groups=int((ch<0).sum()),min_leave_one_out_pp=loo.min(),max_leave_one_out_pp=loo.max(),pre_start="",post_end=""))
out=Path(".")
pd.DataFrame(rows).to_csv(out/"monthly_diagnostics.csv",index=False,float_format="%.12g")
pd.DataFrame(diag).to_csv(out/"event_group_diagnostics.csv",index=False,float_format="%.12g")
manifest={"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"source_rows":len(df),"source_unique_groups":df.group.nunique(),"source_dates":df.date.nunique(),"source_outcomes":sorted(df.outcome.unique()),"files":{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [out/"monthly_diagnostics.csv",out/"event_group_diagnostics.csv"]}}
(out/"phase133_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(pd.DataFrame(rows).to_string(index=False))
print(pd.DataFrame(diag).to_string(index=False))
