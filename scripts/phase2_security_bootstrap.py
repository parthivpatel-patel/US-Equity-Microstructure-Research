#!/usr/bin/env python3
"""Security-level bootstrap for a processed panel; NOT serial-dependence-aware."""
import argparse,csv,hashlib,json,math,random
from pathlib import Path
SHA='2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb'
FIELDS={'Ticker','treated','r_post','r_pre','v_post','v_pre','days_post','days_pre','trades_post','trades_pre','dr','dv'}
def quantile(x,p):
 a=sorted(x); k=(len(a)-1)*p; i=int(k)
 return a[i]+(k-i)*(a[min(i+1,len(a)-1)]-a[i])
def read(path):
 raw=Path(path).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SHA:raise ValueError('Processed-panel SHA-256 mismatch')
 rs=list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
 if not rs or set(rs[0])!=FIELDS:raise ValueError('Invalid schema')
 arms={0:[],1:[]};seen=set()
 for r in rs:
  if r['Ticker'] in seen or not r['Ticker']:raise ValueError('Duplicate/blank ticker')
  seen.add(r['Ticker'])
  if r['treated'] not in ('0','1'):raise ValueError('Invalid treatment')
  d={k:float(r[k]) for k in ('dr','dv','r_pre','r_post','v_pre','v_post','trades_pre')}
  if not all(math.isfinite(v) for v in d.values()) or d['trades_pre']<=0:raise ValueError('Invalid numeric value')
  if any(not 0<=d[k]<=1 for k in ('r_pre','r_post','v_pre','v_post')):raise ValueError('Invalid rate')
  if abs(d['dr']-d['r_post']+d['r_pre'])>1e-9 or abs(d['dv']-d['v_post']+d['v_pre'])>1e-9:raise ValueError('Invalid change')
  arms[int(r['treated'])].append((r['Ticker'],d))
 if not arms[0] or not arms[1]:raise ValueError('Empty group')
 return arms
def gap(t,c,key,weighted=False):
 def avg(a):
  w=[v['trades_pre'] if weighted else 1 for _,v in a]
  return math.fsum(v[key]*z for (_,v),z in zip(a,w))/math.fsum(w)
 return 100*(avg(t)-avg(c))
def analyze(arms,n=5000,seed=20251103):
 if n<100:raise ValueError('Insufficient bootstrap replicates')
 rng=random.Random(seed); t=arms[1];c=arms[0];out={}
 for key in ('dr','dv'):
  for weighted in (False,True):
   name=('hidden_trade' if key=='dr' else 'hidden_volume')+('_pretrade_weighted' if weighted else '_equal_security')
   point=gap(t,c,key,weighted)
   draws=[gap(rng.choices(t,k=len(t)),rng.choices(c,k=len(c)),key,weighted) for _ in range(n)]
   leave=[gap(t[:i]+t[i+1:],c,key,weighted) for i in range(len(t))]
   out[name]={'point_pp':point,'bootstrap_percentile_95_pp':[quantile(draws,.025),quantile(draws,.975)],
    'largest_treated_leave_one_out_shift_abs_pp':max(abs(x-point) for x in leave)}
 return {'estimands':out,'replicates':n,'seed':seed,'n_treated':len(t),'n_control':len(c),
 'processed_input_sha256':SHA,'method':'independent security resampling, not serial-dependence-aware'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--replicates',type=int,default=5000);p.add_argument('--seed',type=int,default=20251103);a=p.parse_args()
 print(json.dumps(analyze(read(a.csv),a.replicates,a.seed),indent=2,sort_keys=True))
