"""Cross-table consistency and sensitivity checks; aggregate-only, no causal inference."""
import csv
from decimal import Decimal

def read(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def audit(summary, windows):
    output=[]
    for r in summary:
        outcome=r['outcome']
        matches=[w for w in windows if w['outcome']==outcome and int(w['window_days'])==5]
        if len(matches)!=1:
            raise ValueError('five-day row must be unique for '+outcome)
        w=matches[0]
        checks={
          'n_equal':int(r['pre_placebo_n'])==int(w['pre_placebo_count']),
          'negative_equal':int(r['pre_placebo_at_least_as_negative'])==int(w['pre_placebo_at_least_as_negative']),
          'extreme_equal':int(r['pre_placebo_at_least_as_extreme_absolute'])==int(w['pre_placebo_at_least_as_extreme_abs']),
          'contrast_within_rounding':abs(Decimal(r['nov_minus_oct_pp'])-Decimal(w['nov_minus_oct_pp']))<=Decimal('0.000001'),
        }
        rows=[x for x in windows if x['outcome']==outcome]
        signs={int(x['window_days']): ('positive' if Decimal(x['nov_minus_oct_pp'])>0 else 'negative' if Decimal(x['nov_minus_oct_pp'])<0 else 'zero') for x in rows}
        output.append({'outcome':outcome,'checks':checks,'window_signs':signs,'sign_sensitive':len(set(signs.values()))>1})
    return output

if __name__=='__main__':
    import json,sys
    if len(sys.argv)!=3: raise SystemExit('usage: python scripts/phase329_cross_table_gate.py results/phase130_summary.csv results/phase131_window_sensitivity.csv')
    print(json.dumps(audit(read(sys.argv[1]),read(sys.argv[2])),indent=2))
