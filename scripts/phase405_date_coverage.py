"""Audit daily tier coverage and temporal integrity before placebo estimation."""
import argparse
import csv
import datetime as dt
import json
from collections import Counter, defaultdict

TIERS = {10, 40, 100}
NUMERIC = [('Hidden', 'TradesForHidden'), ("HiddenVol('000)", "TradeVolForHidden('000)")]

def parse_date(value):
    value = value.strip()
    if len(value) == 8 and value.isdigit():
        return dt.datetime.strptime(value, '%Y%m%d').date()
    return dt.date.fromisoformat(value)

def audit(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        needed = {'Date', 'lot'} | {v for pair in NUMERIC for v in pair}
        if not needed.issubset(reader.fieldnames or []):
            raise ValueError('missing columns: ' + ', '.join(sorted(needed - set(reader.fieldnames or []))))
        rows = list(reader)
    if not rows:
        raise ValueError('empty input')
    by_date = defaultdict(set)
    duplicates = []
    invalid = []
    for i, r in enumerate(rows, 2):
        try:
            date = parse_date(r['Date'])
            lot = int(float(r['lot']))
            if float(r['lot']) != lot or lot not in TIERS:
                raise ValueError('invalid tier')
            if lot in by_date[date]:
                duplicates.append(i)
            by_date[date].add(lot)
            if date.weekday() >= 5:
                invalid.append({'row': i, 'reason': 'weekend'})
            for numerator, denominator in NUMERIC:
                n, d = float(r[numerator]), float(r[denominator])
                if not (0 <= n <= d and 0 < d and n == n and d == d and d != float('inf')):
                    invalid.append({'row': i, 'reason': 'invalid numerator/denominator'})
        except (ValueError, KeyError, OverflowError) as e:
            invalid.append({'row': i, 'reason': str(e)})
    dates = sorted(by_date)
    missing = {date.isoformat(): sorted(TIERS - tiers) for date, tiers in by_date.items() if tiers != TIERS}
    month_counts = Counter(d.strftime('%Y-%m') for d in dates)
    return {'rows': len(rows), 'distinct_dates': len(dates), 'first_date': dates[0].isoformat() if dates else None,
            'last_date': dates[-1].isoformat() if dates else None,
            'month_date_counts': dict(sorted(month_counts.items())), 'missing_tiers_by_date': dict(sorted(missing.items())),
            'duplicate_rows': duplicates, 'invalid_rows': invalid,
            'complete': not (missing or duplicates or invalid) and len(rows) == 3 * len(dates)}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('csv')
    args = p.parse_args()
    print(json.dumps(audit(args.csv), indent=2))
