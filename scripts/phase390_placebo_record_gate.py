"""Fail-closed audit for original dated placebo CSV records (stdlib only)."""
import csv
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

REQUIRED = ('placebo_date','estimate','estimand','window_start','window_end','source_sha256')

def audit(path):
    raw = Path(path).read_bytes()
    rows = list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
    if not rows:
        raise ValueError('no placebo records')
    if not set(REQUIRED).issubset(rows[0]):
        raise ValueError('missing required columns')
    seen, windows = set(), {}
    for i, row in enumerate(rows, 2):
        try:
            date, start, end = (dt.date.fromisoformat(row[k]) for k in ('placebo_date','window_start','window_end'))
            if not start <= date <= end:
                raise ValueError('placebo outside declared window')
            if not math.isfinite(float(row['estimate'])):
                raise ValueError('nonfinite estimate')
            if not row['estimand'].strip():
                raise ValueError('missing estimand')
            sha = row['source_sha256']
            if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
                raise ValueError('invalid source hash')
            key = (date.isoformat(), row['estimand'], start.isoformat(), end.isoformat())
            if key in seen:
                raise ValueError('duplicate dated estimand window')
            seen.add(key)
            windows.setdefault((start.isoformat(), end.isoformat(), row['estimand']), []).append(date.isoformat())
        except (ValueError, TypeError, OverflowError) as exc:
            raise ValueError(f'row {i}: {exc}') from exc
    return {'file_sha256': hashlib.sha256(raw).hexdigest(), 'records': len(rows),
            'distinct_declared_windows': len(windows),
            'repeated_declared_windows': [dict(window_start=k[0],window_end=k[1],estimand=k[2],dates=v)
                for k,v in windows.items() if len(v)>1],
            'source_hashes_authenticated': False, 'effective_trading_windows_verified': False,
            'inference_ready': False}

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('csv_file')
    print(json.dumps(audit(p.parse_args().csv_file), indent=2))
