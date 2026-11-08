"""Fail-closed structural wrapper for Phase 242; not historical session authentication."""
from phase243_placebo_calendar_guard import validate_placebo_sessions
from phase242_placebo_scan import placebo_scan

def guarded_placebo_scan(daily, cuts, half_window, bandwidth, *, admitted_sessions=None):
    """Validate dates before descriptive estimation; caller-supplied roster is not authenticated."""
    validation = validate_placebo_sessions(daily, cuts, half_window)
    if admitted_sessions is not None:
        if not isinstance(admitted_sessions, (list, tuple)) or [r['date'] for r in daily] != list(admitted_sessions):
            raise ValueError('daily observations must exactly match supplied session roster')
    result = placebo_scan(daily, cuts, half_window, bandwidth)
    result['structural_calendar_guard'] = validation
    result['calendar_independently_verified'] = False
    result['source_authenticated'] = False
    result['treatment_authenticated'] = False
    result['causal_effect_established'] = False
    result['session_roster_supplied'] = admitted_sessions is not None
    return result
