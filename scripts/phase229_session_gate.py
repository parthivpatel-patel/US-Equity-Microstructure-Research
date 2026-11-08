"""Fail-closed session membership gate; caller must authenticate source externally."""
from datetime import date
from hashlib import sha256

def validate_sessions(requested, calendar, *, source, expected_sha256):
    """Validate canonical session roster and externally pinned SHA256.

    A checksum pins bytes, not truth. Caller must independently validate source.
    """
    if not isinstance(source,str) or not source.strip() or not isinstance(expected_sha256,str) or len(expected_sha256)!=64:
        raise ValueError('source identifier and pinned SHA256 required')
    if not isinstance(calendar,(list,tuple)) or not calendar:
        raise ValueError('nonempty canonical calendar required')
    if any(not isinstance(x,str) for x in calendar):
        raise ValueError('calendar dates must be strings')
    try:
        parsed=[date.fromisoformat(x) for x in calendar]
    except ValueError as e:
        raise ValueError('invalid calendar date') from e
    if any(x.isoformat()!=raw for x,raw in zip(parsed,calendar)) or list(calendar)!=sorted(set(calendar)):
        raise ValueError('calendar must be unique, sorted and canonical')
    if any(x.weekday()>4 for x in parsed):
        raise ValueError('weekend in calendar')
    digest=sha256(('\n'.join(calendar)+'\n').encode('ascii')).hexdigest()
    if digest!=expected_sha256.lower():
        raise ValueError('calendar digest mismatch')
    if not isinstance(requested,(list,tuple)) or not requested or len(requested)!=len(set(requested)) or list(requested)!=sorted(requested):
        raise ValueError('requested sessions invalid')
    if any(x not in set(calendar) for x in requested):
        raise ValueError('requested session absent from pinned calendar')
    return {'sessions':list(requested),'calendar_sha256':digest,'calendar_source':source,'calendar_authenticated':False}
