"""Fail-closed local source-file provenance and integrity gate; never uploads data."""
import argparse
import hashlib
import json
from pathlib import Path

REQUIRED = ("path", "sha256", "source_url", "retrieved_utc", "redistribution", "grain")
RIGHTS = {"permitted", "restricted", "unknown"}

def audit(manifest, root):
    root = Path(root).resolve()
    entries = manifest.get("sources")
    if not isinstance(entries, list) or not entries:
        return {"status": "BLOCKED", "checked": [], "errors": ["sources must be a nonempty list"]}
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
        if rel.is_absolute() or not path.is_relative_to(root) or path == root:
            errors.append(f"{tag}: unsafe path")
            continue
        if str(rel) in seen:
            errors.append(f"{tag}: duplicate path")
            continue
        seen.add(str(rel))
        if entry["redistribution"] not in RIGHTS:
            errors.append(f"{tag}: invalid redistribution status")
        expected = entry["sha256"].lower()
        if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
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
        checked.append({"path": str(rel), "sha256_match": match, "redistribution": entry["redistribution"]})
    return {"status": "PASS" if not errors else "BLOCKED", "checked": checked, "errors": errors}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    result = audit(json.loads(args.manifest.read_text()), args.root)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 2)

if __name__ == "__main__":
    main()
