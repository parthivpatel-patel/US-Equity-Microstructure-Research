"""Structural calendar-evidence checks; never claims historical authentication."""
from datetime import date, datetime, timezone
from hashlib import sha256
from urllib.parse import urlsplit

def validate_calendar_evidence(calendar, *, source_url, retrieved_at, raw_sha256):
    if not isinstance(calendar, (list, tuple)) or not calendar:
        raise ValueError("nonempty calendar required")
    dates = []
    for value in calendar:
        if not isinstance(value, str):
            raise ValueError("calendar dates must be strings")
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("invalid ISO calendar date") from exc
        if parsed.isoformat() != value or parsed.weekday() >= 5:
            raise ValueError("noncanonical or weekend session")
        dates.append(parsed)
    if dates != sorted(set(dates)):
        raise ValueError("calendar must be strictly increasing and unique")
    if not isinstance(source_url, str):
        raise ValueError("source URL required")
    url = urlsplit(source_url)
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        raise ValueError("HTTPS source URL without embedded credentials required")
    if not isinstance(retrieved_at, str):
        raise ValueError("retrieval timestamp required")
    try:
        timestamp = datetime.fromisoformat(retrieved_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid retrieval timestamp") from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("retrieval timestamp must include timezone")
    if not isinstance(raw_sha256, str) or len(raw_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in raw_sha256):
        raise ValueError("raw SHA256 required")
    return {
        "roster_sha256": sha256(("\n".join(calendar)+"\n").encode()).hexdigest(),
        "raw_source_sha256": raw_sha256.lower(),
        "source_url": source_url,
        "retrieved_at": timestamp.astimezone(timezone.utc).isoformat(),
        "historical_calendar_authenticated": False,
        "limitations": "Structural checks cannot establish holidays, ad-hoc closures, source authenticity, or complete session coverage.",
    }
