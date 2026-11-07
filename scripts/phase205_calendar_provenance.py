"""Audit externally supplied exchange-session calendars; provenance is NOT authentication."""
from datetime import date
from hashlib import sha256
import json
from urllib.parse import urlparse

def audit_calendar(document, observed_dates):
    if not isinstance(document, dict):
        raise TypeError("calendar document must be a mapping")
    errors = []
    for key in ("source_url", "retrieved_utc", "market", "timezone", "sessions"):
        if key not in document:
            errors.append("missing_" + key)
    for key in ("market", "timezone"):
        if not isinstance(document.get(key), str) or not document.get(key, "").strip():
            errors.append("invalid_" + key)
    url = document.get("source_url", "")
    if not isinstance(url, str) or urlparse(url).scheme != "https" or not urlparse(url).netloc:
        errors.append("invalid_source_url")
    stamp = document.get("retrieved_utc")
    if not isinstance(stamp, str) or not stamp.endswith("Z"):
        errors.append("invalid_retrieval_timestamp")
    sessions = document.get("sessions")
    if not isinstance(sessions, list) or not sessions:
        errors.append("empty_or_invalid_sessions")
        sessions = []
    def normalize(values, label):
        output = []
        for value in values:
            try:
                if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
                    raise ValueError
                output.append(value)
            except (TypeError, ValueError):
                errors.append("invalid_" + label + "_date")
        if len(output) != len(set(output)):
            errors.append("duplicate_" + label + "_date")
        if output != sorted(output):
            errors.append("unordered_" + label + "_date")
        return output
    expected = normalize(sessions, "session")
    observed = normalize(observed_dates, "observed")
    missing = sorted(set(expected) - set(observed))
    unexpected = sorted(set(observed) - set(expected))
    if missing:
        errors.append("missing_observed_sessions")
    if unexpected:
        errors.append("unexpected_observed_sessions")
    digest = sha256(json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return {"admitted": not errors, "errors": sorted(set(errors)),
            "missing_sessions": missing, "unexpected_sessions": unexpected,
            "calendar_document_sha256": digest, "source_authenticated": False}
