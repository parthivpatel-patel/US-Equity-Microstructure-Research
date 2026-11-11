"""Fail-closed structural input admission before Phase 307 eligibility auditing.

Does not authenticate the provenance of supplied records or calendar.
"""
from scripts.phase307_eligibility import audit, day


def admitted_audit(observations, intervals, sessions):
    """Require nonempty materialized inputs and nonempty expected panel.

    Missing cells remain missing, never inferred as zero-volume observations.
    """
    observations = list(observations)
    intervals = list(intervals)
    sessions = list(sessions)
    if not sessions:
        raise ValueError('empty trading-session calendar')
    if not intervals:
        raise ValueError('empty eligibility universe')
    for interval in intervals:
        if len(interval) != 4:
            raise ValueError('eligibility interval requires four fields')
        if not all(isinstance(x, str) and x for x in interval):
            raise ValueError('eligibility fields must be nonempty strings')
    for row in observations:
        if len(row) != 3:
            raise ValueError('observation requires three fields')
        if not all(isinstance(x, str) and x for x in row):
            raise ValueError('observation fields must be nonempty strings')
    for session in sessions:
        day(session)
    result = audit(observations, intervals, sessions)
    if result['expected_cells'] == 0:
        raise ValueError('eligibility intervals cover no supplied sessions')
    return result
