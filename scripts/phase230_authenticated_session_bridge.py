"""Calendar-gated matched HAC bridge; source authenticity remains external."""
from phase229_session_gate import validate_sessions
from phase226_matched_hac_bridge import matched_full_series_hac

def calendar_gated_matched_hac(rows, pairs, sessions, exchanges, early_dates, late_dates,
                              bandwidth, *, calendar, calendar_source, calendar_sha256,
                              source_authenticated=False):
    """Fail closed unless caller attests independent calendar authentication."""
    if source_authenticated is not True:
        raise ValueError('independent calendar authentication required')
    admitted = validate_sessions(sessions, calendar, source=calendar_source,
                                 expected_sha256=calendar_sha256)
    if list(sessions) != list(early_dates) + list(late_dates):
        raise ValueError('windows do not partition requested sessions')
    result = matched_full_series_hac(rows, pairs, sessions, exchanges,
                                     early_dates, late_dates, bandwidth)
    result['calendar_sha256'] = admitted['calendar_sha256']
    result['calendar_source'] = admitted['calendar_source']
    result['calendar_authenticated'] = True
    result['calendar_authentication_method'] = 'caller_attestation_not_independently_verified'
    return result
