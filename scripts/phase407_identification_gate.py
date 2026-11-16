"""Fail-closed structural audit for security-exchange-day reform panels."""
import csv,json,sys
from collections import defaultdict
from datetime import date
REQUIRED=('date','security','exchange','treated','hidden_trades','total_trades','hidden_shares','total_shares','match_group')
def audit(rows):
 rows=list(rows); errors=[]; warnings=[]; seen=set(); dates=set(); groups=defaultdict(set)
 for i,r in enumerate(rows,2):
  missing=[k for k in REQUIRED if k not in r or str(r[k]).strip()=='']
  if missing: errors.append(f'row {i}: missing {missing}'); continue
  try:
   d=date.fromisoformat(r['date']); treated=int(r['treated'])
   v=[float(r[k]) for k in ('hidden_trades','total_trades','hidden_shares','total_shares')]
  except (ValueError,TypeError): errors.append(f'row {i}: invalid date/treatment/count'); continue
  if treated not in (0,1): errors.append(f'row {i}: invalid treatment')
  if any(not (x>=0 and x<float('inf')) for x in v) or v[1]<=0 or v[3]<=0 or v[0]>v[1] or v[2]>v[3]: errors.append(f'row {i}: invalid numerator/denominator')
  key=(r['date'],r['security'],r['exchange'])
  if key in seen: errors.append(f'row {i}: duplicate key')
  seen.add(key);dates.add(d);groups[r['match_group']].add(treated)
  if d.weekday()>=5: warnings.append(f'row {i}: weekend date')
 if not rows: errors.append('empty input')
 mixed=sum(g=={0,1} for g in groups.values())
 if not mixed: errors.append('no matched groups containing both treated and controls')
 september=sum(d.month==9 and d.year==2025 for d in dates)
 october=sum(d.month==10 and d.year==2025 for d in dates)
 post=sum(d>=date(2025,11,3) for d in dates)
 if not september: errors.append('no September 2025 pretrend dates')
 if not october: errors.append('no October 2025 placebo dates')
 if not post: errors.append('no post-reform dates')
 return {'status':'BLOCKED' if errors else 'STRUCTURALLY_ELIGIBLE_NOT_AUTHENTICATED','rows':len(rows),'distinct_dates':len(dates),'september_dates':september,'october_dates':october,'post_dates':post,'mixed_match_groups':mixed,'errors':errors,'warnings':warnings,'authentication':'NOT_VERIFIED','causal_identification':'NOT_ESTABLISHED'}
def main(path):
 with open(path,newline='',encoding='utf-8-sig') as f: result=audit(csv.DictReader(f))
 print(json.dumps(result,indent=2,sort_keys=True))
 return 0 if not result['errors'] else 2
if __name__=='__main__': sys.exit(main(sys.argv[1]))
