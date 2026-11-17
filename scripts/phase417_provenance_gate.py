"""Hardened provenance metadata and local SHA-256 integrity gate (no source authentication)."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

REQUIRED = ("path", "sha256", "source_url", "retrieved_utc", "redistribution", "grain")
RIGHTS = {"permitted", "restricted", "unknown"}
GRAINS = {"security-date-exchange", "security-date", "security", "exchange-date", "date", "document"}

def valid_https(value):
    try:
        u = urlsplit(value)
        return u.scheme == "https" and bool(u.hostname) and not u.username and not u.password and not any(c.isspace() for c in value)
    except ValueError:
        return False

def valid_utc(value):
    try:
        if not (value.endswith("Z") or value.endswith("+00:00")):
            return False
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.utcoffset().total_seconds() == 0
    except (ValueError, AttributeError):
        return False

def audit(manifest, root):
    root = Path(root).resolve()
    entries = manifest.get("sources") if isinstance(manifest, dict) else None
    if not isinstance(entries, list) or not entries:
        return {"status":"BLOCKED", "checked":[], "errors":["sources must be a nonempty list"], "publication_clearance":"NOT_ESTABLISHED"}
    errors, checked, seen = [], [], set()
    for i, entry in enumerate(entries):
        tag = f"sources[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{tag}: not an object")
            continue
        missing = [k for k in REQUIRED if not isinstance(entry.get(k), str) or not entry[k].strip()]
        if missing:
            errors.append(f"{tag}: missing {missing}")
            continue
        rel = Path(entry["path"])
        path = (root / rel).resolve()
        if rel.is_absolute() or path == root or not path.is_relative_to(root):
            errors.append(f"{tag}: unsafe path")
            continue
        if path in seen:
            errors.append(f"{tag}: duplicate canonical path")
            continue
        seen.add(path)
        if entry["redistribution"] not in RIGHTS:
            errors.append(f"{tag}: invalid redistribution status")
        if not valid_https(entry["source_url"]):
            errors.append(f"{tag}: invalid HTTPS source URL")
        if not valid_utc(entry["retrieved_utc"]):
            errors.append(f"{tag}: invalid UTC retrieval timestamp")
        if entry["grain"] not in GRAINS:
            errors.append(f"{tag}: unsupported observational grain")
        expected = entry["sha256"].lower()
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"{tag}: invalid SHA-256")
            continue
        if not path.is_file():
            errors.append(f"{tag}: source missing")
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        match = digest.hexdigest() == expected
        if not match:
            errors.append(f"{tag}: SHA-256 mismatch")
        checked.append({"path":str(rel), "sha256_match":match, "redistribution":entry["redistribution"]})
    return {"status":"PASS" if not errors else "BLOCKED", "checked":checked, "errors":errors, "publication_clearance":"NOT_ESTABLISHED"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest", type=Path)
    p.add_argument("--root", type=Path, required=True)
    args = p.parse_args()
    result = audit(json.loads(args.manifest.read_text()), args.root)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 2)

if __name__ == "__main__":
    main()
