#!/usr/bin/env python3
"""Robust-location sensitivity on archived processed Phase-2 panel; NOT causal/source-authenticated."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

REQUIRED = {'Ticker','treated','dr','dv','r_pre','r_post','v_pre','v_post'}

def trimmed_mean(values, proportion):
    if not 0 <= proportion < .5:
        raise ValueError('trim must be in [0,0.5)')
    x = sorted(values)
    if not x or not all(math.isfinite(v) for v in x):
        raise ValueError('empty or nonfinite sample')
    k = int(len(x) * proportion)
    return math.fsum(x[k:len(x)-k]) / (len(x)-2*k)

def analyze(path):
    data = Path(path).read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError('missing required fields')
        groups={0:{'dr':[],'dv':[]},1:{'dr':[],'dv':[]}}
        symbols=set()
        for row in reader:
            if None in row or None in row.values():
                raise ValueError('missing cells')
            symbol=row['Ticker']
            if not symbol or symbol in symbols:
                raise ValueError('missing/duplicate ticker')
            symbols.add(symbol)
            if row['treated'] not in ('0','1'):
                raise ValueError('invalid treatment label')
            g=groups[int(row['treated'])]
            for outcome in ('dr','dv'):
                val=float(row[outcome]); pre=float(row['r_pre' if outcome=='dr' else 'v_pre']);post=float(row['r_post' if outcome=='dr' else 'v_post'])
                if not all(map(math.isfinite,(val,pre,post))) or not (0<=pre<=1 and 0<=post<=1) or abs(val-(post-pre))>1e-10:
                    raise ValueError('invalid rate or difference')
                g[outcome].append(val)
    if not all(groups[t]['dr'] for t in (0,1)):
        raise ValueError('missing comparison arm')
    rows=[]
    for outcome in ('dr','dv'):
        for trim in (0,.05,.1,.2):
            rows.append({'outcome':outcome,'trim_each_tail':trim,
                         'treated_n':len(groups[1][outcome]),'control_n':len(groups[0][outcome]),
                         'treated_minus_control_pp':100*(trimmed_mean(groups[1][outcome],trim)-trimmed_mean(groups[0][outcome],trim))})
    return {'source':'processed Phase-2 stock panel; original SEC ZIP and treatment labels unauthenticated',
            'input_sha256':sha,'n_treated':len(groups[1]['dr']),'n_control':len(groups[0]['dr']),
            'location_sensitivity':rows}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('csv');ap.add_argument('--expect-sha256');args=ap.parse_args()
    result=analyze(args.csv)
    if args.expect_sha256 and result['input_sha256'].lower()!=args.expect_sha256.lower():
        raise SystemExit('Processed-input SHA256 mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
