"""Structural preflight for matched HAC. Does not authenticate historical sessions."""
from phase234_calendar_evidence_validator import validate_calendar_evidence
from phase232_provenance_safe_bridge import provenance_safe_matched_hac

def structurally_gated_matched_hac(rows, pairs, sessions, exchanges, early_dates,
                                    late_dates, bandwidth, *, calendar, source_url,
                                    retrieved_at, raw_sha256, source_authenticated=False):
    evidence = validate_calendar_evidence(calendar, source_url=source_url,
                                          retrieved_at=retrieved_at, raw_sha256=raw_sha256)
    requested = list(sessions)
    if not requested or requested != list(early_dates) + list(late_dates):
        raise ValueError('requested sessions must partition into early and late windows')
    if len(set(requested)) != len(requested) or requested != sorted(requested):
        raise ValueError('requested sessions must be strictly increasing and unique')
    if any(s not in set(calendar) for s in requested):
        raise ValueError('requested sessions absent from supplied roster')
    if source_authenticated is not True:
        raise ValueError('caller source attestation required; not independent verification')
    result = provenance_safe_matched_hac(
        rows, pairs, sessions, exchanges, early_dates, late_dates, bandwidth,
        calendar=calendar, calendar_source=source_url,
        calendar_sha256=evidence['roster_sha256'], source_authenticated=True)
    result = dict(result)
    result.pop('calendar_authenticated', None)
    result.update({
        'calendar_structurally_validated': True,
        'calendar_raw_source_sha256_claimed': evidence['raw_source_sha256'],
        'calendar_retrieved_at_claimed': evidence['retrieved_at'],
        'calendar_independently_verified': False,
        'calendar_source_authentication_pending': True,
    })
    return result
