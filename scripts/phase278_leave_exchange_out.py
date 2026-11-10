"""Phase 278: fixed-roster leave-one-exchange-out sensitivity; descriptive only.

Inputs are already admitted by phase277.audit_panel. This function deliberately
makes no claim about historical provenance or statistical significance.
"""
import math

def leave_exchange_out(admitted):
    days = admitted['dates']
    counts = admitted['pair_counts_by_exchange']
    if not days or len(counts) < 2:
        raise ValueError('at least two exchanges and one day required')
    if any(type(n) is not int or n <= 0 for n in counts.values()):
        raise ValueError('invalid fixed-roster pair counts')
    exchanges = sorted(counts)
    if any(set(day['by_exchange']) != set(exchanges) for day in days):
        raise ValueError('exchange roster changed across dates')
    if len({day['date'] for day in days}) != len(days):
        raise ValueError('duplicate dates')
    for day in days:
        if any(not math.isfinite(float(v)) for v in day['by_exchange'].values()):
            raise ValueError('nonfinite contrast')
    def estimate(excluded):
        active = [e for e in exchanges if e != excluded]
        denominator = sum(counts[e] for e in active)
        daily_pair = [sum(float(d['by_exchange'][e])*counts[e] for e in active)/denominator for d in days]
        daily_equal = [sum(float(d['by_exchange'][e]) for e in active)/len(active) for d in days]
        return {'pair_weighted_mean': sum(daily_pair)/len(days),
                'exchange_equal_mean': sum(daily_equal)/len(days)}
    full = estimate(None)
    omitted = {e:estimate(e) for e in exchanges}
    def flips(key):
        base = full[key]
        return sorted(e for e,v in omitted.items() if base*v[key] < 0)
    return {'full_sample':full, 'leave_one_exchange_out':omitted,
            'sign_reversals_pair_weighted':flips('pair_weighted_mean'),
            'sign_reversals_exchange_equal':flips('exchange_equal_mean'),
            'n_dates':len(days), 'n_exchanges':len(exchanges),
            'source_authenticated':False, 'historical_inference_authorized':False}
