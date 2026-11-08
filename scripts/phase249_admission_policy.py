"""Explicit policy for admission to historical causal estimation.

This policy does not perform independent authentication. Callers must supply
verified boolean attestations, with external evidence documented separately.
"""

def historical_estimation_allowed(byte_verified, source_authenticated,
                                  calendar_authenticated, treatment_authenticated,
                                  license_authorized):
    checks = (byte_verified, source_authenticated, calendar_authenticated,
              treatment_authenticated, license_authorized)
    if not all(type(value) is bool for value in checks):
        raise TypeError("all attestations must be explicit booleans")
    return all(checks)
