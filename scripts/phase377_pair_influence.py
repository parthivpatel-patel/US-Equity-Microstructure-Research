"""Exact matched-pair deletion sensitivity for phase376; no empirical inference."""
from fractions import Fraction
from phase376_matched_date_contrast import contrast

def pair_deletion_audit(rows, pre_dates, post_dates):
    """Return full contrast and all leave-one-pair-out contrasts; requires >=2 pairs."""
    rows = tuple(rows)
    full = contrast(rows, pre_dates, post_dates)
    if full['pairs'] < 2:
        raise ValueError('at least two matched pairs required')
    per_pair = full['per_pair']
    n = full['pairs']
    deleted = {pair: (n * full['estimate'] - effect) / (n - 1)
               for pair, effect in sorted(per_pair.items())}
    for pair, value in deleted.items():
        recomputed = contrast((r for r in rows if r[0] != pair), pre_dates, post_dates)['estimate']
        if recomputed != value:
            raise AssertionError('deletion identity violated')
    return {
        'estimate': full['estimate'], 'pair_count': n,
        'leave_one_out': deleted,
        'min_leave_one_out': min(deleted.values()),
        'max_leave_one_out': max(deleted.values()),
        'sign_reversal_on_deletion': any(
            (value > 0) != (full['estimate'] > 0) if value and full['estimate'] else False
            for value in deleted.values()),
        'source_authenticated': False, 'treatment_authenticated': False,
        'inferential_p_value': None,
    }
