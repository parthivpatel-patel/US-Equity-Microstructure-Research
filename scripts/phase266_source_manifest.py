"""Fail-closed SHA-256 byte inventory; byte integrity is not source authentication."""
import argparse
import hashlib
import json
from pathlib import Path

def digest_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def inspect(root, records):
    root = Path(root).resolve()
    seen, results = set(), []
    for rec in records:
        name = rec["path"]
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("duplicate or invalid path")
        seen.add(name)
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("unsafe path")
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError("path escapes root")
        sha, size = rec.get("sha256"), rec.get("size_bytes")
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError("invalid sha256")
        if type(size) is not int or size < 0:
            raise ValueError("invalid size")
        if not path.is_file():
            results.append({"path": name, "status": "missing"})
            continue
        actual_size, actual_sha = path.stat().st_size, digest_file(path)
        status = "verified_bytes" if (actual_size == size and actual_sha == sha) else "mismatch"
        results.append({"path": name, "status": status, "actual_size_bytes": actual_size, "actual_sha256": actual_sha})
    return {"byte_integrity_pass": bool(records) and all(r["status"] == "verified_bytes" for r in results),
            "source_authentication_pass": False, "treatment_authentication_pass": False,
            "historical_inference_authorized": False, "files": results}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--manifest", required=True)
    args = p.parse_args()
    manifest = json.loads(Path(args.manifest).read_text())
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list):
        raise ValueError("manifest requires files list")
    result = inspect(args.root, manifest["files"])
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["byte_integrity_pass"] else 2)

if __name__ == "__main__":
    main()
