"""Fail-closed provenance gate for historical market estimations.

Verifies local bytes against a pinned SHA-256 and requires declared source,
calendar and treatment references. Does not independently authenticate them.
"""
import hashlib
from pathlib import Path

REQUIRED = ('source_url', 'retrieved_utc', 'source_sha256', 'calendar_reference',
            'treatment_reference', 'treatment_rule_version', 'license_review')


def audit_input(path, manifest):
    if not isinstance(manifest, dict):
        raise ValueError('manifest must be a dictionary')
    missing = [k for k in REQUIRED if not isinstance(manifest.get(k), str) or not manifest[k].strip()]
    if missing:
        return {'admitted': False, 'reason': 'missing provenance fields', 'missing': missing}
    digest = manifest['source_sha256'].lower()
    if len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
        return {'admitted': False, 'reason': 'invalid sha256'}
    p = Path(path)
    if not p.is_file():
        return {'admitted': False, 'reason': 'source file unavailable'}
    hasher = hashlib.sha256()
    with p.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            hasher.update(block)
    actual = hasher.hexdigest()
    if actual != digest:
        return {'admitted': False, 'reason': 'digest mismatch', 'actual_sha256': actual}
    return {'admitted': True, 'reason': 'manifest completeness and bytes verified only',
            'actual_sha256': actual, 'independent_source_authentication': False,
            'calendar_authenticated': False, 'treatment_authenticated': False,
            'redistribution_authorized': False}
