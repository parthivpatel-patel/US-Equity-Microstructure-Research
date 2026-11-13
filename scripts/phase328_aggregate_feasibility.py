"""Exact-decimal necessary-condition audit of Phase 130 aggregate placebo rows."""
import csv
import json
import sys
from decimal import Decimal

def audit(r):
    n=int(r['pre_placebo_n'])
    negative=int(r['pre_placebo_at_least_as_negative'])
    extreme=int(r['pre_placebo_at_least_as_extreme_absolute'])
    d=Decimal(r['nov_minus_oct_pp'])
    lo=Decimal(r['pre_placebo_min_pp'])
    hi=Decimal(r['pre_placebo_max_pp'])
    if n<1 or not (0<=negative<=n and 0<=extreme<=n) or not all(x.is_finite() for x in (d,lo,hi)) or lo>hi:
        raise ValueError('invalid aggregate row')
    if d<0:
        minimum=negative+int(hi>=-d)
    elif d>0:
        minimum=int(lo<=-d)+int(hi>=d)
    else:
        minimum=n
    failures=[]
    if extreme<minimum:
        failures.append('absolute-extreme count below necessary minimum')
    if hi<=d and negative!=n:
        failures.append('negative-tail count incompatible with maximum')
    if lo>d and negative!=0:
        failures.append('negative-tail count incompatible with minimum')
    return {'outcome':r['outcome'],'reported_absolute_extreme':extreme,'necessary_minimum':minimum,'consistent_with_necessary_conditions':not failures,'failures':failures,'warning':'Necessary conditions only; not authentication of raw windows'}

def run(path):
    with open(path,newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    if not rows or len({r['outcome'] for r in rows})!=len(rows):
        raise ValueError('empty or duplicate outcomes')
    return [audit(r) for r in rows]

if __name__=='__main__':
    if len(sys.argv)!=2:
        sys.exit('usage: python scripts/phase328_aggregate_feasibility.py results/phase130_summary.csv')
    print(json.dumps(run(sys.argv[1]),indent=2))
