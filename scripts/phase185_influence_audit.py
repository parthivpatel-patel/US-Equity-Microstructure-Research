"""Phase 185: descriptive leave-one-group/date sensitivity on a balanced common-date panel."""
import csv, json, math, sys
from collections import defaultdict
from datetime import date
WINDOWS=(3,5,7,10,15)
OUTCOMES=('count','volume')
FIELDS=('window_days','placebo_date','outcome','matched_group_id','contrast_pp')
def audit(rows):
    values={}; dates=defaultdict(set); rosters=defaultdict(set)
    for r in rows:
        if set(r)!=set(FIELDS): raise ValueError('schema mismatch')
        raw,d,o,g=(r[k] for k in FIELDS[:4])
        if not raw.isascii() or not raw.isdecimal() or int(raw) not in WINDOWS: raise ValueError('invalid window')
        w=int(raw)
        if len(d)!=10 or date.fromisoformat(d).isoformat()!=d: raise ValueError('invalid date')
        if o not in OUTCOMES or not g or g.strip()!=g: raise ValueError('invalid group/outcome')
        v=float(r['contrast_pp'])
        if not math.isfinite(v): raise ValueError('nonfinite contrast')
        k=(w,d,o,g)
        if k in values: raise ValueError('duplicate observation')
        values[k]=v; dates[w,o].add(d); rosters[w,d,o].add(g)
    if not values: raise ValueError('empty panel')
    for w in WINDOWS:
        if not dates[w,'count'] or dates[w,'count']!=dates[w,'volume']: raise ValueError('outcome date mismatch')
    common=sorted(set.intersection(*(dates[w,'count'] for w in WINDOWS)))
    if len(common)<2: raise ValueError('at least two common dates required')
    groups=sorted(rosters[WINDOWS[0],common[0],'count'])
    if len(groups)<2: raise ValueError('at least two groups required')
    for w in WINDOWS:
        for d in common:
            if rosters[w,d,'count']!=set(groups) or rosters[w,d,'volume']!=set(groups):
                raise ValueError('unbalanced common-date roster')
    result={}
    for w in WINDOWS:
        result[str(w)]={}
        for o in OUTCOMES:
            full=math.fsum(values[w,d,o,g] for d in common for g in groups)/(len(common)*len(groups))
            leave_group=[math.fsum(values[w,d,o,h] for d in common for h in groups if h!=g)/(len(common)*(len(groups)-1)) for g in groups]
            leave_date=[math.fsum(values[w,e,o,g] for e in common if e!=d for g in groups)/((len(common)-1)*len(groups)) for d in common]
            result[str(w)][o]=dict(full_mean_pp=full,group_deletion_range_pp=[min(leave_group),max(leave_group)],date_deletion_range_pp=[min(leave_date),max(leave_date)],group_deletion_sign_flip=any(full*x<0 for x in leave_group),date_deletion_sign_flip=any(full*x<0 for x in leave_date),max_abs_group_change_pp=max(abs(x-full) for x in leave_group),max_abs_date_change_pp=max(abs(x-full) for x in leave_date))
    return dict(common_dates=common,fixed_group_ids=groups,results=result,warning='Descriptive only; no source authentication, inference or causal identification.')
def load(path):
    with open(path,newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ())!=FIELDS: raise ValueError('CSV header mismatch')
        return audit(list(reader))
if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/phase185_influence_audit.py group_contrasts.csv')
    print(json.dumps(load(sys.argv[1]),indent=2))
