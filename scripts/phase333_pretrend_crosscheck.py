"""Audit published pretrend and October-shift tables; no raw-panel inference."""
import csv
import json
import sys
from decimal import Decimal
from pathlib import Path

D = Decimal

def rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def audit(a, b, c):
    output = []
    for outcome in ('count', 'volume'):
        x = next(r for r in a if r['outcome'] == outcome)
        allperiod = [r for r in b if r['outcome'] == outcome and r['period'] == 'Jul-Oct']
        early = [r for r in b if r['outcome'] == outcome and r['period'] == 'Jul-Sep']
        shifts = [r for r in c if r['outcome'] == outcome]
        assert len(allperiod) == len(early) == 5 and len(shifts) == 4
        assert {int(r['hac_lag']) for r in allperiod} == {0,3,5,10,15}
        assert {int(r['hac_lag']) for r in early} == {0,3,5,10,15}
        assert {int(r['block_days']) for r in shifts} == {3,5,10,15}
        assert int(x['pre_days']) == 87
        assert all(int(r['dates']) == 87 and int(r['groups']) == 68 for r in allperiod)
        assert all(int(r['dates']) == 64 and int(r['groups']) == 68 for r in early)
        assert all(int(r['days_jul_sep']) == 64 and int(r['days_oct']) == 23 and int(r['groups']) == 68 for r in shifts)
        assert abs(D(x['daily_slope_pp']) - D(allperiod[0]['slope_pp_per_trading_day'])) < D('0.000001')
        assert abs(D(json.loads(x['leave_month_out_slopes_pp_per_day'])['10']) - D(early[0]['slope_pp_per_trading_day'])) < D('0.000001')
        assert all(abs(D(r['slope_pp_per_trading_day'])-D(allperiod[0]['slope_pp_per_trading_day'])) < D('0.000001') for r in allperiod)
        assert all(abs(D(r['slope_pp_per_trading_day'])-D(early[0]['slope_pp_per_trading_day'])) < D('0.000001') for r in early)
        assert all(abs(D(r['jul_sep_slope_pp_day'])-D(early[0]['slope_pp_per_trading_day'])) < D('0.000001') for r in shifts)
        for r in shifts:
            assert abs((D(r['oct_slope_pp_day'])-D(r['jul_sep_slope_pp_day']))-D(r['oct_minus_jul_sep_slope_pp_day'])) < D('0.000001')
            assert D(r['bootstrap_95_low']) < D(r['oct_minus_jul_sep_slope_pp_day']) < D(r['bootstrap_95_high'])
        output.append({'outcome':outcome,'jul_sep_slope_pp_per_day':early[0]['slope_pp_per_trading_day'], 'jul_oct_slope_pp_per_day':allperiod[0]['slope_pp_per_trading_day'], 'oct_slope_pp_per_day':shifts[0]['oct_slope_pp_day'], 'oct_minus_jul_sep_pp_per_day':shifts[0]['oct_minus_jul_sep_slope_pp_day'], 'jul_sep_two_way_ci_excludes_zero_all_lags':all(D(r['two_way_ci_low'])>0 or D(r['two_way_ci_high'])<0 for r in early), 'jul_oct_two_way_ci_excludes_zero_all_lags':all(D(r['two_way_ci_low'])>0 or D(r['two_way_ci_high'])<0 for r in allperiod), 'oct_shift_bootstrap_ci_excludes_zero_all_blocks':all(D(r['bootstrap_95_low'])>0 or D(r['bootstrap_95_high'])<0 for r in shifts)})
    return output

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('usage: python phase333_pretrend_crosscheck.py phase135.csv phase136.csv phase139.csv')
    print(json.dumps(audit(*(rows(Path(p)) for p in sys.argv[1:])), indent=2))
