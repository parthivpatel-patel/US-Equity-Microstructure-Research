"""Fail-closed integration of Phase 274 outcomes and Phase 275 session endpoints.

Synthetic validation only. No calendar, treatment, or source authentication.
"""
from phase274_pretrend import evaluate
from phase275_pretrend_window_audit import audit_windows


def evaluate_admitted(calendar, observations, early, late, *, require_contiguous_partition=False):
    """Audit the same materialized calendar/observations passed to estimation."""
    sessions = tuple(calendar)
    rows = tuple(observations)
    admission = audit_windows(sessions, early, late,
                              require_contiguous_partition=require_contiguous_partition)
    result = evaluate(sessions, rows, early, late)
    if result['early']['n'] != admission['early_sessions'] or result['late']['n'] != admission['late_sessions']:
        raise ValueError('admission and estimation disagree on session counts')
    return {'admission': admission, 'descriptive_pretrend': result,
            'source_authenticated': False, 'calendar_authenticated': False,
            'treatment_authenticated': False, 'historical_inference_authorized': False}
