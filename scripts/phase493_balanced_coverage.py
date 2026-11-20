"""Eligibility-aware paired-cell diagnostics; not a treatment-effect estimator."""
import hashlib
import json
from collections import defaultdict
from datetime import date
from pathlib import Path


def _read(path, observed):
    import csv
    required = ['security', 'exchange', 'date'] + (['outcome'] if observed else [])
    with open(path, newline='', encoding='utf-8-sig') as f:
        r = csv.DictReader(f, restkey='__extra__', restval=None, strict=True)
        if r.fieldnames is None or len(r.fieldnames) != len(required) or set(r.fieldnames) != set(required):
            raise ValueError('invalid schema')
        result = {}
        for line, row in enumerate(r, 2):
            if '__extra__' in row or any(not isinstance(v, str) or not v.strip() for v in row.values()):
                raise ValueError(f'malformed row {line}')
            try:
                parsed = date.fromisoformat(row['date'])
            except ValueError as exc:
                raise ValueError(f'invalid date {line}') from exc
            if parsed.isoformat() != row['date']:
                raise ValueError(f'noncanonical date {line}')
            key = tuple(row[k] for k in required[:3])
            if key in result:
                raise ValueError(f'duplicate key {line}')
            if observed:
                import math
                try:
                    value = float(row['outcome'])
                except ValueError as exc:
                    raise ValueError(f'invalid outcome {line}') from exc
                if not math.isfinite(value):
                    raise ValueError(f'nonfinite outcome {line}')
            else:
                value = True
            result[key] = value
    return result


def audit(eligibility, panel, cutoff):
    try:
        dt = date.fromisoformat(cutoff)
    except ValueError as exc:
        raise ValueError('invalid cutoff') from exc
    if dt.isoformat() != cutoff:
        raise ValueError('noncanonical cutoff')
    eligible = _read(eligibility, False)
    observed = _read(panel, True)
    if not eligible or set(observed) - set(eligible):
        raise ValueError('empty eligibility or out-of-universe observation')
    days = {k[2] for k in eligible}
    if not any(x < cutoff for x in days) or not any(x >= cutoff for x in days):
        raise ValueError('two-sided eligibility required')
    groups = defaultdict(lambda: {'pre': set(), 'post': set(), 'pre_obs': set(), 'post_obs': set()})
    for key in eligible:
        unit = key[:2]
        side = 'pre' if key[2] < cutoff else 'post'
        groups[unit][side].add(key[2])
    for key in observed:
        unit = key[:2]
        side = 'pre_obs' if key[2] < cutoff else 'post_obs'
        groups[unit][side].add(key[2])
    out = {'cutoff': cutoff, 'provenance_status': 'UNAUTHENTICATED_INPUTS',
           'eligible_units': len(groups), 'both_side_eligible_units': 0,
           'both_side_observed_units': 0, 'fully_covered_both_side_units': 0,
           'eligible_cells_both_side_units': 0, 'observed_cells_both_side_units': 0,
           'observed_zero_cells_both_side_units': 0, 'by_exchange': {}}
    by_exchange = defaultdict(lambda: {'both_side_eligible_units': 0, 'fully_covered_both_side_units': 0,
                                       'eligible_cells': 0, 'observed_cells': 0})
    for (security, exchange), g in groups.items():
        if not g['pre'] or not g['post']:
            continue
        out['both_side_eligible_units'] += 1
        out['both_side_observed_units'] += bool(g['pre_obs'] and g['post_obs'])
        full = g['pre'] == g['pre_obs'] and g['post'] == g['post_obs']
        out['fully_covered_both_side_units'] += full
        expected = len(g['pre']) + len(g['post'])
        actual = len(g['pre_obs']) + len(g['post_obs'])
        out['eligible_cells_both_side_units'] += expected
        out['observed_cells_both_side_units'] += actual
        out['observed_zero_cells_both_side_units'] += sum(observed[(security, exchange, day)] == 0 for day in g['pre_obs'] | g['post_obs'])
        b = by_exchange[exchange]
        b['both_side_eligible_units'] += 1
        b['fully_covered_both_side_units'] += full
        b['eligible_cells'] += expected
        b['observed_cells'] += actual
    out['by_exchange'] = dict(sorted(by_exchange.items()))
    out['sha256'] = {name: hashlib.sha256(Path(p).read_bytes()).hexdigest() for name,p in [('eligibility',eligibility),('panel',panel)]}
    return out


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('eligibility'); p.add_argument('panel'); p.add_argument('cutoff')
    a = p.parse_args()
    print(json.dumps(audit(a.eligibility, a.panel, a.cutoff), sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
