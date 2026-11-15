"""Exact decimal validation for count/volume CSV measures (stdlib only).

This is a supplementary gate; it does not authenticate source provenance.
"""
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

MEASURES = ('hidden_count', 'total_count', 'hidden_volume', 'total_volume')

def exact_nonnegative_integer(value):
    try:
        number = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError('invalid decimal') from None
    if not number.is_finite() or number < 0 or number != number.to_integral_value():
        raise ValueError('not a finite nonnegative integer')
    return int(number)

def audit(path):
    errors = []
    rows = 0
    with Path(path).open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames) or not set(MEASURES).issubset(reader.fieldnames):
            raise ValueError('missing or duplicate headers')
        for row_number, row in enumerate(reader, 2):
            rows += 1
            if None in row or any(v is None for v in row.values()):
                errors.append({'line': row_number, 'issue': 'malformed_row'})
                continue
            try:
                hc, tc, hv, tv = (exact_nonnegative_integer(row[k]) for k in MEASURES)
            except ValueError:
                errors.append({'line': row_number, 'issue': 'invalid_integer'})
                continue
            if hc > tc or hv > tv:
                errors.append({'line': row_number, 'issue': 'numerator_exceeds_denominator'})
    return {'rows': rows, 'passed': rows > 0 and not errors, 'errors': errors,
            'source_authenticated': False, 'treatment_authenticated': False}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path')
    args = parser.parse_args()
    result = audit(args.csv_path)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 2)
