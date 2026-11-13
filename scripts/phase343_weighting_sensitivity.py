#!/usr/bin/env python3
"""Weighting sensitivity for paired group-date-exchange hidden-rate differences.

No causal or inferential interpretation. Source authentication is external.
"""
import csv
import json
import math
import sys
from collections import defaultdict
from datetime import date

FIELDS = {'security','date','exchange','treated','match_group','numerator','denominator'}

def analyze(rows):
    cells = defaultdict(lambda: {'0': [0.0, 0.0], '1': [0.0, 0.0]})
    assignments, seen = {}, set()
    for i, row in enumerate(rows, 2):
        if not FIELDS.issubset(row):
            raise ValueError(f'line {i}: missing fields')
        sec, day, ex, arm, group = (row[k].strip() for k in ('security','date','exchange','treated','match_group'))
        if not sec or not ex or not group or arm not in ('0','1'):
            raise ValueError(f'line {i}: invalid identifiers')
        try:
            if date.fromisoformat(day).isoformat() != day:
                raise ValueError('noncanonical date')
            num, den = float(row['numerator']), float(row['denominator'])
        except (TypeError, ValueError) as e:
            raise ValueError(f'line {i}: invalid date or quantity') from e
        if not all(map(math.isfinite, (num,den))) or not (0 <= num <= den) or den <= 0:
            raise ValueError(f'line {i}: invalid rate components')
        key = (sec,day,ex)
        if key in seen:
            raise ValueError(f'line {i}: duplicate security-date-exchange')
        seen.add(key)
        if sec in assignments and assignments[sec] != (arm,group):
            raise ValueError(f'line {i}: treatment or matching drift')
        assignments[sec] = (arm,group)
        sums = cells[(group,day,ex)][arm]
        sums[0] += num
        sums[1] += den
    if not seen:
        raise ValueError('empty panel')
    by_group = defaultdict(list)
    discarded = 0
    for (group,day,ex), arms in sorted(cells.items()):
        if not arms['0'][1] or not arms['1'][1]:
            discarded += 1
            continue
        diff = 100 * (arms['1'][0]/arms['1'][1] - arms['0'][0]/arms['0'][1])
        by_group[group].append((diff, arms['0'][1]+arms['1'][1]))
    if not by_group:
        return {'status':'NO_PAIRED_SUPPORT','paired_cells':0,'discarded_cells':discarded,'estimates_pp':None,
                'source_authenticated':False,'inference':'NOT_COMPUTED'}
    group_means = {g: sum(d for d,w in cells)/len(cells) for g,cells in sorted(by_group.items())}
    all_cells = [x for group in by_group.values() for x in group]
    sum_weights = sum(w for d,w in all_cells)
    estimates = {
        'equal_group': sum(group_means.values())/len(group_means),
        'equal_paired_cell': sum(d for d,w in all_cells)/len(all_cells),
        'combined_denominator_weighted_cell': sum(d*w for d,w in all_cells)/sum_weights,
    }
    return {'status':'DESCRIPTIVE_WEIGHTING_SENSITIVITY_ONLY','source_authenticated':False,
            'input_rows':len(seen),'paired_cells':len(all_cells),'discarded_cells':discarded,
            'supported_groups':len(by_group),'group_means_pp':group_means,
            'estimates_pp':estimates,'range_pp':max(estimates.values())-min(estimates.values()),
            'inference':'NOT_COMPUTED: common-date, group, exchange and serial dependence not resolved'}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: phase343_weighting_sensitivity.py AUTHORIZED_PANEL.csv')
    with open(sys.argv[1], newline='', encoding='utf-8') as f:
        print(json.dumps(analyze(csv.DictReader(f)), indent=2, sort_keys=True))
