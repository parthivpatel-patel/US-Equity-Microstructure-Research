"""Fail-closed calendar support gate for Phase 433 JSON outputs.

No SEC data bundled. Prevents excluding zero-pair units from the common-date
denominator and interpreting a vacuous intersection as support.
"""
import argparse
import json


def gate(report, period):
    units = [u for u in report['by_unit'] if u['period'] == period]
    if not units:
        return {'period': period, 'pass': False, 'reason': 'no units'}
    missing = [(u['match_group'], u['exchange']) for u in units if not u['paired_date_values']]
    sets = [set(u['paired_date_values']) for u in units]
    common = set.intersection(*sets)
    passed = bool(common) and not missing
    return {'period': period, 'pass': passed, 'units': len(units),
            'zero_paired_units': len(missing), 'common_dates': sorted(common),
            'reason': 'ok' if passed else 'zero paired units or no common date'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('report_json')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    with open(args.report_json, encoding='utf8') as f:
        report = json.load(f)
    result = {'pre': gate(report, 'pre'), 'post': gate(report, 'post')}
    with open(args.output, 'w', encoding='utf8') as f:
        json.dump(result, f, indent=2, sort_keys=True)
    if not all(v['pass'] for v in result.values()):
        raise SystemExit(2)


if __name__ == '__main__':
    main()
