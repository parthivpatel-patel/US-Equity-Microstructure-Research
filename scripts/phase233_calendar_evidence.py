"""Conservative evidence metadata; neither checksum nor attestation proves session authenticity."""
from hashlib import sha256

def assess_calendar_evidence(calendar, *, source_url, retrieved_at, raw_sha256,
                             independently_checked=False, reviewer_evidence=None):
    if not isinstance(calendar, (list, tuple)) or not calendar or not all(isinstance(d, str) for d in calendar):
        raise ValueError('nonempty string calendar required')
    if not isinstance(source_url, str) or not source_url.startswith(('https://', 'http://')):
        raise ValueError('source URL required')
    if not isinstance(retrieved_at, str) or not retrieved_at.strip():
        raise ValueError('retrieval timestamp required')
    if not isinstance(raw_sha256, str) or len(raw_sha256) != 64 or any(c not in '0123456789abcdefABCDEF' for c in raw_sha256):
        raise ValueError('raw source SHA256 required')
    if type(independently_checked) is not bool:
        raise ValueError('independently_checked must be bool')
    if independently_checked and (not isinstance(reviewer_evidence, str) or not reviewer_evidence.strip()):
        raise ValueError('independent check requires evidence reference')
    return {
        'roster_sha256': sha256(('\n'.join(calendar) + '\n').encode('utf-8')).hexdigest(),
        'raw_source_sha256': raw_sha256.lower(),
        'source_url': source_url,
        'retrieved_at': retrieved_at,
        'independent_check_documented': independently_checked,
        'independent_check_evidence': reviewer_evidence if independently_checked else None,
        'historical_calendar_authenticated': False,
        'status': 'requires_independent_source_and_session_verification',
    }
