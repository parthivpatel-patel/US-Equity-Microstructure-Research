"""Fail-closed structural audit for a canonical security-date-exchange CSV panel.

Standard library only. Structural checks do not authenticate SEC source bytes.
"""
import csv
import datetime as dt
import json
import math
from collections import Counter
from pathlib import Path

REQUIRED = ('security', 'date', 'exchange', 'cohort', 'hidden_count', 'total_count', 'hidden_volume', 'total_volume')
COHORTS = {'treated', 'control'}

def audit(path):
    path = Path(path)
    issues = Counter()
    securities, keys, dates, exchanges = {}, set(), set(), set()
    n = 0
    with path.open(newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError('missing or duplicate CSV headers')
        missing = set(REQUIRED) - set(reader.fieldnames)
        if missing:
            raise ValueError('missing columns: ' + ', '.join(sorted(missing)))
        for line, row in enumerate(reader, 2):
            n += 1
            if None in row or any(row.get(k) is None for k in REQUIRED):
                issues['malformed_row'] += 1
                continue
            s, d, e, c = (row[k].strip() for k in REQUIRED[:4])
            if not s or not e or c not in COHORTS:
                issues['invalid_identity_or_cohort'] += 1
                continue
            try:
                date = dt.date.fromisoformat(d)
                if date.isoformat() != d:
                    raise ValueError('noncanonical date')
            except ValueError:
                issues['invalid_date'] += 1
                continue
            key = (s, d, e)
            if key in keys:
                issues['duplicate_security_date_exchange'] += 1
            keys.add(key)
            if s in securities and securities[s] != c:
                issues['cohort_switch'] += 1
            securities.setdefault(s, c)
            dates.add(d)
            exchanges.add(e)
            try:
                vals = [float(row[k]) for k in REQUIRED[4:]]
                if any(not math.isfinite(x) or x < 0 or not x.is_integer() for x in vals):
                    raise ValueError('nonfinite, negative or fractional counts')
                hc, tc, hv, tv = vals
                if hc > tc or hv > tv:
                    issues['numerator_exceeds_denominator'] += 1
                if (tc == 0 and hc != 0) or (tv == 0 and hv != 0):
                    issues['nonzero_numerator_zero_denominator'] += 1
            except (ValueError, OverflowError):
                issues['invalid_measure'] += 1
    return {'file': path.name, 'rows': n, 'unique_keys': len(keys),
            'unique_securities': len(securities),
            'treated_securities': sum(v == 'treated' for v in securities.values()),
            'control_securities': sum(v == 'control' for v in securities.values()),
            'unique_dates': len(dates), 'unique_exchanges': len(exchanges),
            'issues': dict(sorted(issues.items())), 'passed': not issues and n > 0,
            'source_authenticated': False, 'treatment_authenticated': False}

def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv_path')
    p.add_argument('--output', help='optional JSON report path')
    args = p.parse_args()
    result = audit(args.csv_path)
    output = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
    print(output, end='')
    raise SystemExit(0 if result['passed'] else 2)

if __name__ == '__main__':
    main()
