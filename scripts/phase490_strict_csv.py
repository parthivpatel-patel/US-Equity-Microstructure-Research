"""Strict CSV admission for security-exchange-date panels; does not authenticate data sources."""
import csv
import math
from datetime import date

def read_strict(path, observed=False):
    expected = ('security', 'exchange', 'date', 'outcome') if observed else ('security', 'exchange', 'date')
    result = {}
    with open(path, newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream, restkey='__extra__', restval=None, strict=True)
        if reader.fieldnames is None or len(reader.fieldnames) != len(expected) or set(reader.fieldnames) != set(expected):
            raise ValueError('invalid CSV schema')
        try:
            for line, row in enumerate(reader, start=2):
                if '__extra__' in row or any(not isinstance(v, str) or not v.strip() for v in row.values()):
                    raise ValueError(f'malformed CSV row at line {line}')
                try:
                    parsed = date.fromisoformat(row['date'])
                except ValueError as exc:
                    raise ValueError(f'invalid date at line {line}') from exc
                if parsed.isoformat() != row['date']:
                    raise ValueError(f'noncanonical date at line {line}')
                key = (row['security'], row['exchange'], row['date'])
                if key in result:
                    raise ValueError(f'duplicate key at line {line}')
                if observed:
                    try:
                        value = float(row['outcome'])
                    except ValueError as exc:
                        raise ValueError(f'invalid outcome at line {line}') from exc
                    if not math.isfinite(value):
                        raise ValueError(f'nonfinite outcome at line {line}')
                else:
                    value = True
                result[key] = value
        except csv.Error as exc:
            raise ValueError('malformed CSV quoting') from exc
    return result
