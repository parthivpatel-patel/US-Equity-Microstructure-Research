"""Bridge Phase 248 byte-integrity output to Phase 249 policy, fail closed.

This module cannot authenticate independent evidence. Explicit external
attestations must be supplied and audited outside this function.
"""
from phase248_authentication_gate import audit_input
from phase249_admission_policy import historical_estimation_allowed


def evaluate_historical_input(path, manifest, attestations):
    """Return decision and reasons; never infer authenticity from manifest text."""
    integrity = audit_input(path, manifest)
    if not isinstance(attestations, dict):
        raise TypeError('attestations must be a dictionary')
    names = ('source_authenticated', 'calendar_authenticated',
             'treatment_authenticated', 'license_authorized')
    if any(type(attestations.get(name)) is not bool for name in names):
        raise TypeError('four explicit boolean attestations required')
    byte_verified = integrity.get('admitted') is True
    allowed = historical_estimation_allowed(byte_verified,
        attestations['source_authenticated'],
        attestations['calendar_authenticated'],
        attestations['treatment_authenticated'],
        attestations['license_authorized'])
    failed = ([] if byte_verified else ['byte_integrity']) + [
        name for name in names if not attestations[name]]
    return {'historical_estimation_allowed': allowed,
            'failed_checks': failed, 'integrity': integrity,
            'attestation_origin': 'caller_supplied_not_independently_verified'}
