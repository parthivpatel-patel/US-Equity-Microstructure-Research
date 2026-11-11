"""Strict wrapper for the Phase 309 structural admission gate.

Reject any eligibility interval that contributes no expected trading session.
This is a structural condition, not proof of source or calendar authenticity.
"""
from scripts.phase309_admission import admitted_audit


def strict_admitted_audit(observations, intervals, sessions):
    observations = list(observations)
    intervals = list(intervals)
    sessions = list(sessions)
    result = admitted_audit(observations, intervals, sessions)
    if result['empty_intervals']:
        raise ValueError('eligibility interval covers no supplied trading session')
    return result
