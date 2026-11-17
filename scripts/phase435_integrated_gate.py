"""Joint fail-closed structural gate for Phase 432 and 433 reports; no SEC data."""
import argparse
import json

def evaluate(daily, calendar):
    units = daily.get('by_group_exchange', [])
    cal = calendar.get('by_unit', [])
    reasons = []
    if not units or not cal:
        reasons.append('empty unit inventory')
    if daily.get('unstable_security_membership') or calendar.get('unstable_security_exchange_assignments'):
        reasons.append('unstable assignments')
    keys = [(u['match_group'], u['exchange']) for u in units]
    if len(set(keys)) != len(keys):
        reasons.append('duplicate daily units')
    if any(not u['strict_support'] for u in units):
        reasons.append('at least one unit lacks strict fixed-security support')
    common = {}
    for period in ('pre', 'post'):
        subset = [u for u in cal if u['period'] == period]
        ck = [(u['match_group'], u['exchange']) for u in subset]
        if len(ck) != len(set(ck)) or set(ck) != set(keys):
            reasons.append(f'{period}: calendar/daily unit mismatch')
        sets = [set(u['paired_date_values']) for u in subset]
        overlap = set.intersection(*sets) if sets else set()
        common[period] = sorted(overlap)
        if not overlap:
            reasons.append(f'{period}: no dates shared by all units')
    if daily.get('observations') != calendar.get('observations'):
        reasons.append('input observation counts disagree')
    return {'pass': not reasons, 'reasons': reasons, 'units': len(units),
            'common_dates': common,
            'warning': 'Structural gate only; no SEC source or treatment authentication and no causal inference.'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('daily_json')
    p.add_argument('calendar_json')
    p.add_argument('--output', required=True)
    a = p.parse_args()
    with open(a.daily_json, encoding='utf-8') as f:
        daily = json.load(f)
    with open(a.calendar_json, encoding='utf-8') as f:
        calendar = json.load(f)
    result = evaluate(daily, calendar)
    with open(a.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, sort_keys=True)
    if not result['pass']:
        raise SystemExit(2)

if __name__ == '__main__':
    main()
