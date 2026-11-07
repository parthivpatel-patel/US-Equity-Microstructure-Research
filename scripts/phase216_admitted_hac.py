"""Fail-closed composition of session admission and joint-window HAC.

Calendar is caller supplied, NOT independently authenticated here.
"""
from scripts.phase215_calendar_gate import admit_sessions
from scripts.phase213_joint_hac import joint_window_hac


def admitted_joint_hac(rows, sessions, early, late, lags=(0, 1, 3), min_per_window=5):
    gate = admit_sessions(rows, sessions, early, late)
    estimate = joint_window_hac(rows, early, late, lags=lags,
                                min_per_window=min_per_window)
    if gate['early_n'] != estimate['early_n'] or gate['late_n'] != estimate['late_n']:
        raise AssertionError('admission and estimation disagree on window counts')
    return {'admission': gate, 'estimate': estimate,
            'historical_inference_validated': False,
            'causal_effect_established': False}
