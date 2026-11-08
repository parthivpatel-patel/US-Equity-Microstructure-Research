"""Fail-closed window guard before published structural preflight.

Does not independently authenticate exchange sessions or SEC data.
"""
from phase236_window_guard import validate_estimation_windows
from phase235_structural_preflight import structurally_gated_matched_hac


def window_gated_matched_hac(rows, pairs, sessions, exchanges, early_dates,
                            late_dates, bandwidth, *, calendar, source_url,
                            retrieved_at, raw_sha256, source_authenticated=False):
    evidence = validate_estimation_windows(sessions, early_dates, late_dates, calendar)
    result = structurally_gated_matched_hac(
        rows, pairs, sessions, exchanges, early_dates, late_dates, bandwidth,
        calendar=calendar, source_url=source_url, retrieved_at=retrieved_at,
        raw_sha256=raw_sha256, source_authenticated=source_authenticated)
    result = dict(result)
    result.pop('calendar_authenticated', None)
    result.update({
        'window_contract_validated': True,
        'window_n_early': evidence['n_early'],
        'window_n_late': evidence['n_late'],
        'window_n_sessions': evidence['n_sessions'],
        'calendar_independently_verified': False,
    })
    return result
