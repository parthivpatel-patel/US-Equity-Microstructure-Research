"""Byte-identity and CSV structural gate. Does not authenticate historical origins."""
import csv
import hashlib
import io
import math
from datetime import date

def verify_inputs(observation_bytes, calendar_bytes, manifest):
    """Expected SHA-256 values must come from independently maintained provenance."""
    if not isinstance(manifest, dict):
        raise ValueError("manifest required")
    for label, blob in (("observations", observation_bytes), ("calendar", calendar_bytes)):
        if not isinstance(blob, bytes):
            raise ValueError("input must be bytes")
        expected = manifest.get(label + "_sha256")
        if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise ValueError("invalid expected digest")
        if hashlib.sha256(blob).hexdigest() != expected:
            raise ValueError("digest mismatch")
    def read(blob, fields):
        try:
            reader = csv.DictReader(io.StringIO(blob.decode("utf-8-sig"), newline=""))
            if reader.fieldnames is None or set(reader.fieldnames) != set(fields):
                raise ValueError("CSV schema mismatch")
            rows = list(reader)
        except UnicodeDecodeError as exc:
            raise ValueError("invalid UTF-8") from exc
        if not rows or any(None in r or any(v is None or not v.strip() for v in r.values()) for r in rows):
            raise ValueError("malformed CSV")
        return rows
    obs = read(observation_bytes, ("security","exchange","matched_group","date","treated","outcome"))
    cal = read(calendar_bytes, ("date",))
    try:
        sessions = [date.fromisoformat(r["date"]) for r in cal]
        dates = [date.fromisoformat(r["date"]) for r in obs]
    except ValueError as exc:
        raise ValueError("invalid ISO date") from exc
    if len(sessions) != len(set(sessions)):
        raise ValueError("duplicate calendar session")
    if set(dates) - set(sessions):
        raise ValueError("observations outside supplied calendar")
    seen = set()
    for r in obs:
        key = (r["security"],r["exchange"],r["date"])
        if key in seen:
            raise ValueError("duplicate security-exchange-date")
        seen.add(key)
        if r["treated"] not in ("True","False"):
            raise ValueError("invalid treatment encoding")
        try:
            value = float(r["outcome"])
        except ValueError as exc:
            raise ValueError("invalid outcome") from exc
        if not math.isfinite(value):
            raise ValueError("nonfinite outcome")
    return {"observation_rows":len(obs),"calendar_sessions":len(sessions),
            "observation_sha256":manifest["observations_sha256"],
            "calendar_sha256":manifest["calendar_sha256"],
            "bytes_match_manifest":True,"source_origin_authenticated":False,
            "treatment_authenticated":False,
            "warning":"Hash equality proves byte identity, not SEC origin, calendar authority, or treatment."}
