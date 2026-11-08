# Phase 231: Authentication attestation is not authentication

Date: 2026-11-07. Scope: exact published Phase 229 and Phase 230 Python sources inspected through the connected GitHub repository. No historical observations were processed.

## Reproducible source-code finding

In `scripts/phase230_authenticated_session_bridge.py`, the caller supplies `source_authenticated=True`. The function then calls `validate_sessions` and unconditionally sets `result['calendar_authenticated'] = True`. Yet the same result records `calendar_authentication_method = 'caller_attestation_not_independently_verified'`. This creates a misleading machine-readable field: external consumers may interpret `calendar_authenticated=True` as independent authentication although the code has performed none. Phase 229 explicitly returns `calendar_authenticated=False` after checking only calendar membership, sorted uniqueness, weekday restriction and a caller-supplied digest. A digest pins a submitted roster, not an authoritative exchange calendar.

## Severity and recommended repair

Treat this as a **provenance-labeling defect** rather than proof of contaminated empirical data. In a future revised bridge, preserve separate fields `caller_attested_calendar_source` and `calendar_independently_verified`; set the latter to false until a separately documented verification process validates the original authoritative source and its exact bytes. Do not rely on a caller-selected source name and SHA256 alone. A calendar containing a false weekday holiday can satisfy the current digest check.

## Reproduction

Source-only assertion: Phase 230 contains both the literal assignment `result['calendar_authenticated'] = True` and the literal `caller_attestation_not_independently_verified`; Phase 229 returns `calendar_authenticated: False`. These can be checked by reading the published files. This report does not assert that the full bridge integration was executed or that any SEC estimate changed.

## Empirical status

No historical SEC panel, original-source checksum, authenticated 2025 exchange calendar, or Nasdaq treatment classification was available for validation in this session. The September pretrends and October placebo remain serious obstacles to causal interpretation. Matched-security and HAC implementations have not been validated on authenticated historical inputs. Previously recovered research archives were not accessible for a complete inventory or redistribution review. No causal effect is established.

## Next step

Replace the misleading boolean and add a test that a caller attestation never becomes an independent-verification claim; then establish a source-authentication manifest and rerun September/October placebo estimates only after independently checking original data and treatment assignments.
