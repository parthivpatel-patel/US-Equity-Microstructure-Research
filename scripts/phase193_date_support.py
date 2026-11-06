"""Audit exact placebo-window date support; structural diagnostics only."""
from datetime import date
from collections import defaultdict
import csv, json, sys

FIELDS = ('window_id','trade_date','matched_group_id','outcome')

def audit(rows):
    membership=defaultdict(set)
    duplicates=set()
    for r in rows:
        if set(r)!=set(FIELDS): raise ValueError('schema mismatch')
        w,d,g,o=(r[k] for k in FIELDS)
        if any(not isinstance(x,str) or not x or x.strip()!=x for x in (w,d,g,o)):
            raise ValueError('invalid identifier')
        if o not in ('count','volume'): raise ValueError('invalid outcome')
        try:
            parsed=date.fromisoformat(d)
            if parsed.isoformat()!=d or parsed.weekday()>=5: raise ValueError('invalid date')
        except ValueError as exc: raise ValueError('invalid date') from exc
        key=(w,d,g,o)
        if key in duplicates: raise ValueError('duplicate membership')
        duplicates.add(key)
        membership[(w,o)].add((d,g))
    windows=sorted({w for w,o in membership})
    if not windows: raise ValueError('empty membership')
    outcomes=('count','volume')
    if any((w,o) not in membership for w in windows for o in outcomes):
        raise ValueError('both outcomes required per window')
    common=set.intersection(*(membership[w,o] for w in windows for o in outcomes))
    per_window={w:{o:len(membership[w,o]) for o in outcomes} for w in windows}
    pairwise={w:len(membership[w,'count'] & membership[w,'volume']) for w in windows}
    common_dates=sorted({d for d,g in common})
    common_groups=sorted({g for d,g in common})
    return {'windows':windows,'membership_counts':per_window,
            'paired_unit_dates_per_window':pairwise,
            'all_window_common_unit_dates':len(common),
            'all_window_common_dates':common_dates,
            'all_window_common_groups':common_groups,
            'warning':'Membership-only audit; neither authenticated market dates nor causal estimates.'}

def load(path):
    with open(path,newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ())!=FIELDS: raise ValueError('CSV header mismatch')
        return audit(list(reader))

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python phase193_date_support.py membership.csv')
    print(json.dumps(load(sys.argv[1]),indent=2))
