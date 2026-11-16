import pandas as pd,numpy as np,zipfile
from pathlib import Path
import statsmodels.api as sm
P=Path('/mnt/data')
a=pd.read_csv(P/'nasdaq_october_2025.csv');b=pd.read_csv(P/'nasdaq_november_2025.csv(1).csv')
for x in [a,b]:
 x.drop(x.index[~x['Round Lot Size'].isin([1,10,40,100]) | x.Symbol.isna()],inplace=True)
 x.drop_duplicates('Symbol',inplace=True)
m=a[['Symbol','Round Lot Size']].merge(b[['Symbol','Round Lot Size']],on='Symbol',suffixes=('_oct','_nov'))
m=m[m['Round Lot Size_oct']==m['Round Lot Size_nov']].copy();m['treated']=(m['Round Lot Size_oct']<100).astype(int)
with zipfile.ZipFile(P/'individual_security_2025_q4.zip') as z:
 df=pd.read_csv(z.open('q4_2025_all.csv'),low_memory=False)
print('input',len(df),'columns',df.columns.tolist(),flush=True)
df=df[(df.Security=='Stock') & df.Date.between(20251001,20251128)].merge(m,left_on='Ticker',right_on='Symbol',how='inner')
df=df[(df.TradesForHidden>0)&(df["TradeVolForHidden('000)"]>0)].copy()
df['rate']=df.Hidden/df.TradesForHidden;df['vrate']=df["HiddenVol('000)"]/df["TradeVolForHidden('000)"]
df['period']=np.where(df.Date<20251103,'pre','post')
# equal-stock comparison: each security's period-level weighted rate, then difference
agg=df.groupby(['Ticker','treated','period'],as_index=False).agg(hidden=('Hidden','sum'),trades=('TradesForHidden','sum'),hv=("HiddenVol('000)",'sum'),tv=("TradeVolForHidden('000)",'sum'),days=('Date','nunique'))
agg['r']=agg.hidden/agg.trades;agg['v']=agg.hv/agg.tv
wide=agg.pivot(index=['Ticker','treated'],columns='period',values=['r','v','days','trades']).dropna()
wide.columns=['_'.join(c) for c in wide.columns];wide=wide.reset_index()
wide=wide[(wide.days_pre>=10)&(wide.days_post>=10)].copy();wide['dr']=wide.r_post-wide.r_pre;wide['dv']=wide.v_post-wide.v_pre
print('matched securities',len(wide),'treated',wide.treated.sum(),flush=True)
def fit(data,y,controls=[]):
 X=sm.add_constant(data[['treated']+controls]);return sm.OLS(data[y],X).fit(cov_type='HC3')
rows=[]
for y in ['dr','dv']:
 for model,controls in [('unadjusted',[]),('baseline_adjusted',['r_pre','v_pre'])]:
  f=fit(wide,y,controls);ci=f.conf_int().loc['treated'];rows.append({'outcome':y,'specification':model,'n_securities':len(wide),'n_treated':int(wide.treated.sum()),'effect':f.params['treated'],'se_HC3':f.bse['treated'],'p':f.pvalues['treated'],'ci_low':ci.iloc[0],'ci_high':ci.iloc[1]})
# Oct-only placebo split: October 1-15 vs 16-31
place=df[df.Date<20251101].copy();place['period']=np.where(place.Date<=20251015,'early','late')
p=place.groupby(['Ticker','treated','period'],as_index=False).agg(h=('Hidden','sum'),t=('TradesForHidden','sum'),days=('Date','nunique'))
p['r']=p.h/p.t;w=p.pivot(index=['Ticker','treated'],columns='period',values=['r','days']).dropna();w.columns=['_'.join(c) for c in w.columns];w=w.reset_index();w=w[(w.days_early>=7)&(w.days_late>=7)];w['dr']=w.r_late-w.r_early
f=fit(w,'dr');ci=f.conf_int().loc['treated'];rows.append({'outcome':'October placebo trade rate','specification':'unadjusted','n_securities':len(w),'n_treated':int(w.treated.sum()),'effect':f.params['treated'],'se_HC3':f.bse['treated'],'p':f.pvalues['treated'],'ci_low':ci.iloc[0],'ci_high':ci.iloc[1]})
res=pd.DataFrame(rows);res.to_csv(P/'roundlot_phase2_inference.csv',index=False);wide.to_csv(P/'roundlot_phase2_security_panel.csv',index=False)
print(res.to_string(index=False),flush=True)