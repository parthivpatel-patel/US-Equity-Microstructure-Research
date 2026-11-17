"""Audit calendar overlap across matched group/exchange cells; structural only."""
import csv
import json
import argparse
from collections import defaultdict
from datetime import date

CUTOFF = date(2025, 11, 3)
REQUIRED = {'date', 'security', 'exchange', 'match_group', 'treated'}

def audit(rows):
    cells = defaultdict(lambda: defaultdict(set))
    identities = defaultdict(set)
    seen = set()
    n = 0
    for line, row in enumerate(rows, 2):
        if not REQUIRED.issubset(row):
            raise ValueError(f'line {line}: missing columns')
        try:
            d = date.fromisoformat(row['date'])
        except (ValueError, TypeError) as exc:
            raise ValueError(f'line {line}: invalid date') from exc
        if d.weekday() >= 5:
            raise ValueError(f'line {line}: weekend date')
        s, e, g = (row[k].strip() for k in ('security','exchange','match_group'))
        a = row['treated']
        if not all((s,e,g)) or a not in ('0','1'):
            raise ValueError(f'line {line}: invalid identifiers or treatment')
        if (d,s,e) in seen:
            raise ValueError(f'line {line}: duplicate security/exchange/date')
        seen.add((d,s,e))
        identities[(s,e)].add((g,a))
        period = 'pre' if d < CUTOFF else 'post'
        cells[(g,e,period)][d].add(a)
        n += 1
    if not n:
        raise ValueError('empty panel')
    result = []
    for (g,e,p), by_date in sorted(cells.items()):
        paired = {d for d, arms in by_date.items() if arms == {'0','1'}}
        result.append({'match_group':g, 'exchange':e, 'period':p,
                       'observed_dates':len(by_date), 'paired_dates':len(paired),
                       'unpaired_dates':len(by_date)-len(paired),
                       'paired_date_values':sorted(d.isoformat() for d in paired)})
    cross = []
    for p in ('pre','post'):
        date_sets = [set(x['paired_date_values']) for x in result if x['period']==p and x['paired_dates']]
        union = set().union(*date_sets) if date_sets else set()
        intersection = set.intersection(*date_sets) if date_sets else set()
        cross.append({'period':p,'eligible_group_exchange_units':len(date_sets),
                      'union_paired_dates':len(union), 'common_paired_dates':len(intersection),
                      'common_date_values':sorted(intersection)})
    unstable = sorted(f'{s}@{e}' for (s,e),v in identities.items() if len(v)>1)
    return {'observations':n,'by_unit':result,'cross_unit':cross,
            'unstable_security_exchange_assignments':unstable,
            'warning':'No source authentication or causal inference; common dates are only a diagnostic.'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('input_csv')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    with open(args.input_csv, newline='', encoding='utf-8') as f:
        result=audit(csv.DictReader(f))
    with open(args.output,'w',encoding='utf-8') as f:
        json.dump(result,f,indent=2,sort_keys=True)
    if result['unstable_security_exchange_assignments']:
        raise SystemExit(2)

if __name__=='__main__':
    main()
