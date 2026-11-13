"""Cross-table aggregate placebo consistency gate; not source-data authentication."""
import csv, json, sys
from decimal import Decimal

def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def audit(summary, windows):
    index={(r['outcome'],r['window_days']):r for r in windows}
    if len(index)!=len(windows): raise ValueError('duplicate outcome/window')
    out=[]
    for row in summary:
        name=row['outcome']; w=index.get((name,'5'))
        if w is None: raise ValueError('missing five-day row: '+name)
        e=Decimal(row['nov_minus_oct_pp'])
        lo=Decimal(row['pre_placebo_min_pp']); hi=Decimal(row['pre_placebo_max_pp'])
        n=int(row['pre_placebo_n'])
        neg=int(row['pre_placebo_at_least_as_negative'])
        extreme=int(row['pre_placebo_at_least_as_extreme_absolute'])
        if not (lo<=hi and n>0 and 0<=neg<=n and 0<=extreme<=n):
            raise ValueError('invalid summary')
        minimum=(neg if e<0 else 0)+(1 if e<0 and hi>abs(e) else 0)
        if e>=0 and lo < -abs(e): minimum=1
        diff=abs(e-Decimal(w['nov_minus_oct_pp']))
        count_match=(n==int(w['pre_placebo_count']) and
                     neg==int(w['pre_placebo_at_least_as_negative']) and
                     extreme==int(w['pre_placebo_at_least_as_extreme_abs']))
        out.append({'outcome':name,
                    'five_day_contrast_rounding_match':diff<=Decimal('0.0000005'),
                    'five_day_tail_counts_match':count_match,
                    'required_absolute_extremes_lower_bound':minimum,
                    'reported_absolute_extremes':extreme,
                    'joint_feasible_necessary_condition':extreme>=minimum})
    return out

if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: phase331_cross_table_joint_gate.py summary.csv windows.csv')
    results=audit(load(sys.argv[1]),load(sys.argv[2]))
    print(json.dumps(results,indent=2))
    if not all(x['five_day_contrast_rounding_match'] and
               x['five_day_tail_counts_match'] and
               x['joint_feasible_necessary_condition'] for x in results):
        sys.exit(1)
