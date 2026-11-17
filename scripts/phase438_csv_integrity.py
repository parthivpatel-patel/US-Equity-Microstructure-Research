"""Fail-closed CSV structural integrity audit; not SEC authentication or causal inference."""
import csv
import hashlib
import io
from collections import Counter
REQUIRED = ('date','security','exchange','match_group','treated','hidden_count','total_count')

def audit_bytes(raw):
    if not isinstance(raw, bytes) or not raw:
        raise ValueError('nonempty CSV bytes required')
    try:
        decoded = raw.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ValueError('invalid UTF-8') from exc
    if '\x00' in decoded:
        raise ValueError('NUL byte in CSV')
    reader = csv.reader(io.StringIO(decoded, newline=''), strict=True)
    try:
        header = next(reader)
    except StopIteration as exc:
        raise ValueError('missing header') from exc
    if len(header) != len(set(header)):
        raise ValueError('duplicate CSV header')
    if any(not col or col != col.strip() for col in header):
        raise ValueError('blank or whitespace-padded header')
    missing = set(REQUIRED) - set(header)
    if missing:
        raise ValueError('missing required columns: ' + ','.join(sorted(missing)))
    counts = Counter()
    n = 0
    for line, row in enumerate(reader, 2):
        if len(row) != len(header):
            raise ValueError(f'row {line}: expected {len(header)} fields, found {len(row)}')
        if any(not value.strip() for value in row):
            raise ValueError(f'row {line}: empty field')
        n += 1
        counts[row[header.index('exchange')]] += 1
    if n == 0:
        raise ValueError('header-only CSV')
    return {'source_sha256':hashlib.sha256(raw).hexdigest(), 'source_bytes':len(raw),
            'rows':n, 'columns':len(header), 'exchange_row_counts':dict(sorted(counts.items())),
            'structural_csv_valid':True, 'sec_source_authenticated':False,
            'historical_effect_estimated':False}
