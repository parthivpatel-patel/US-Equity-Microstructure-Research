"""Provenance-safe wrapper around Phase 230; no independent source verification claimed."""
from phase230_authenticated_session_bridge import calendar_gated_matched_hac

def provenance_safe_matched_hac(*args, **kwargs):
    """Preserve caller attestation separately from independently verified provenance."""
    result = calendar_gated_matched_hac(*args, **kwargs)
    if not isinstance(result, dict):
        raise TypeError('expected mapping result from Phase 230')
    result = dict(result)
    result.pop('calendar_authenticated', None)
    result['calendar_caller_attested'] = kwargs.get('source_authenticated') is True
    result['calendar_independently_verified'] = False
    result['calendar_verification_basis'] = 'caller_attestation_and_digest_only'
    result['calendar_source_authentication_pending'] = True
    return result
