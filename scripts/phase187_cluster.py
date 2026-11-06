"""Balanced matched-group by date two-way CR1 variance. Descriptive only."""
import csv, json, math, sys
from collections import defaultdict
from datetime import date
FIELDS=('matched_group_id','placebo_date','contrast_pp')
def audit(rows):
    values={}; groups=set(); dates=set()
    for row in rows:
        if set(row)!=set(FIELDS): raise ValueError('schema mismatch')
        g,d=row['matched_group_id'],row['placebo_date']
        if not isinstance(g,str) or not g or g.strip()!=g: raise ValueError('invalid matched group')
        if not isinstance(d,str) or len(d)!=10: raise ValueError('invalid date')
        try:
            if date.fromisoformat(d).isoformat()!=d: raise ValueError('noncanonical date')
        except ValueError as exc: raise ValueError('invalid date') from exc
        try: y=float(row['contrast_pp'])
        except (ValueError,TypeError) as exc: raise ValueError('invalid contrast') from exc
        if not math.isfinite(y): raise ValueError('nonfinite contrast')
        if (g,d) in values: raise ValueError('duplicate group/date')
        values[g,d]=y; groups.add(g); dates.add(d)
    G,T=len(groups),len(dates)
    if G<2 or T<2: raise ValueError('at least two groups and two dates required')
    if len(values)!=G*T: raise ValueError('unbalanced panel')
    mu=math.fsum(values.values())/(G*T)
    by_group=defaultdict(list); by_date=defaultdict(list); sq=[]
    for (g,d),y in values.items():
        e=y-mu; by_group[g].append(e); by_date[d].append(e); sq.append(e*e)
    sg=math.fsum(math.fsum(v)**2 for v in by_group.values())
    st=math.fsum(math.fsum(v)**2 for v in by_date.values())
    si=math.fsum(sq)
    vg=(G/(G-1))*sg/(G*T)**2
    vt=(T/(T-1))*st/(G*T)**2
    vi=((G*T)/(G*T-1))*si/(G*T)**2
    v=vg+vt-vi
    return dict(groups=G,dates=T,observations=len(values),mean_pp=mu,variance_pp2=v,
        group_component_pp2=vg,date_component_pp2=vt,intersection_component_pp2=vi,
        standard_error_pp=math.sqrt(v) if v>=0 else None,
        warning=('Negative two-way cluster variance; SE undefined' if v<0 else
                 'Descriptive CR1 standard error only; not causal inference'))
def load(path):
    with open(path,newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ())!=FIELDS: raise ValueError('CSV header mismatch')
        return audit(list(reader))
if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/phase187_cluster.py group_date_contrasts.csv')
    print(json.dumps(load(sys.argv[1]),indent=2))
