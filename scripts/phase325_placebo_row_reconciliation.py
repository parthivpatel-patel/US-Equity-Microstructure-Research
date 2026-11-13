"""Fail-closed reconstruction of Phase 130 summary from dated placebo windows."""
import csv, datetime as dt, json, sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
REQUIRED={'outcome','window_id','start_date','end_date','placebo_pp'}
def dec(x):
    v=Decimal(x)
    if not v.is_finite(): raise ValueError('nonfinite')
    return v
def reconcile(summaries,raw):
    groups=defaultdict(list); seen=set()
    for r in raw:
        if not REQUIRED.issubset(r): raise ValueError('missing columns')
        key=(r['outcome'],r['window_id'])
        if not all(key) or key in seen: raise ValueError('duplicate or empty window identity')
        seen.add(key)
        a=dt.date.fromisoformat(r['start_date']); b=dt.date.fromisoformat(r['end_date'])
        if a>b: raise ValueError('reversed dates')
        groups[key[0]].append(dec(r['placebo_pp']))
    expected={r['outcome']:r for r in summaries}
    if len(expected)!=len(summaries) or set(expected)!=set(groups): raise ValueError('outcome mismatch')
    result={}
    for name,r in expected.items():
        v=groups[name]; d=dec(r['nov_minus_oct_pp'])
        n=int(r['pre_placebo_n'])
        if n<1 or len(v)!=n: raise ValueError('window count mismatch')
        observed={'pre_placebo_n':len(v),
          'pre_placebo_at_least_as_negative':sum(x<=d for x in v),
          'pre_placebo_at_least_as_extreme_absolute':sum(abs(x)>=abs(d) for x in v),
          'pre_placebo_min_pp':min(v),'pre_placebo_max_pp':max(v)}
        mismatch={}
        for k,x in observed.items():
            published=int(r[k]) if k in ('pre_placebo_n','pre_placebo_at_least_as_negative','pre_placebo_at_least_as_extreme_absolute') else dec(r[k])
            if published!=x: mismatch[k]={'published':str(published),'reconstructed':str(x)}
        result[name]={'matches':not mismatch,'mismatches':mismatch,
          'ties_at_event':sum(x==d for x in v),'ties_at_opposite':sum(x==-d for x in v),
          'right_tail_ge_event':sum(x>=d for x in v)}
    return result
def main(path):
    with Path('results/phase130_summary.csv').open(newline='') as f: s=list(csv.DictReader(f))
    with Path(path).open(newline='') as f: r=list(csv.DictReader(f))
    out=reconcile(s,r); print(json.dumps(out,indent=2))
    return 0 if all(x['matches'] for x in out.values()) else 2
if __name__=='__main__':
    if len(sys.argv)!=2: sys.exit('usage: python scripts/phase325_placebo_row_reconciliation.py dated_windows.csv')
    sys.exit(main(sys.argv[1]))
