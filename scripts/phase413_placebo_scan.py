"""Descriptive October matched-cell placebo scan; no authentication or causal claims."""
import csv,json,math,sys
from collections import defaultdict
from datetime import date
START,END=date(2025,10,1),date(2025,11,3)
def scan(rows,cutoffs=('2025-10-08','2025-10-15','2025-10-22'),lag=3):
    if not isinstance(lag,int) or lag<0:return {'status':'BLOCKED','errors':['invalid lag']}
    cells=defaultdict(lambda:[[0,0],[0,0]]);seen=set();errors=[]
    for i,r in enumerate(rows,1):
        try:
            d=date.fromisoformat(r['date'])
            if not START<=d<END:continue
            s,g,e=(str(r[k]).strip() for k in ('security','match_group','exchange'))
            t,h,n=(int(r[k]) for k in ('treated','hidden_trades','total_trades'))
            if not s or not g or not e or t not in (0,1) or n<=0 or not 0<=h<=n:raise ValueError('invalid identity or counts')
            key=(d,s,e)
            if key in seen:raise ValueError('duplicate security-exchange-date')
            seen.add(key);v=cells[(d,g,e)][t];v[0]+=h;v[1]+=n
        except (KeyError,ValueError,TypeError) as exc:errors.append(f'row {i}: {exc}')
    if errors:return {'status':'BLOCKED','errors':errors[:25],'error_count':len(errors)}
    daily=defaultdict(list)
    for (d,g,e),v in cells.items():
        if v[0][1] and v[1][1]:daily[d].append(100*(v[1][0]/v[1][1]-v[0][0]/v[0][1]))
    series=sorted((d,sum(v)/len(v)) for d,v in daily.items())
    if not series:return {'status':'BLOCKED','errors':['no paired October cells']}
    results=[]
    for raw in cutoffs:
        try:cut=date.fromisoformat(raw)
        except (ValueError,TypeError):return {'status':'BLOCKED','errors':['invalid cutoff']}
        if not START<cut<END:return {'status':'BLOCKED','errors':['cutoff outside October']}
        pre=[v for d,v in series if d<cut];post=[v for d,v in series if d>=cut]
        if min(len(pre),len(post))<2:
            results.append({'cutoff':raw,'status':'INSUFFICIENT_DATES','pre_dates':len(pre),'post_dates':len(post)});continue
        a,b=sum(pre)/len(pre),sum(post)/len(post);n=len(series);p=len(post)/n
        scores=[((0 if d<cut else 1)-p)*(y-(a if d<cut else b)) for d,y in series]
        denom=sum(((0 if d<cut else 1)-p)**2 for d,y in series)
        bw=min(lag,n-1);lr=sum(z*z for z in scores)
        for k in range(1,bw+1):
            lr+=2*(1-k/(bw+1))*sum(scores[j]*scores[j-k] for j in range(k,n))
        results.append({'cutoff':raw,'status':'DESCRIPTIVE_ONLY','pre_dates':len(pre),'post_dates':len(post),'difference_pp':b-a,'hac_se_pp':math.sqrt(max(0,lr))/denom,'hac_lag':bw})
    return {'status':'STRUCTURE_ONLY_NOT_AUTHENTICATED','october_dates':len(series),'matched_group_exchange_date_cells':sum(map(len,daily.values())),'cutoffs':results,'source_authenticated':False,'treatment_authenticated':False,'causal_inference':False,'warning':'Fixed-cutoff HAC is not multiplicity adjusted; no p-values or causal claims.'}
if __name__=='__main__':
    with open(sys.argv[1],newline='',encoding='utf-8-sig') as f:r=scan(csv.DictReader(f))
    print(json.dumps(r,indent=2,sort_keys=True));sys.exit(2 if r['status']=='BLOCKED' else 0)
