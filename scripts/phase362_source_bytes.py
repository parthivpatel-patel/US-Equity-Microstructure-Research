"""Verify local source bytes against a declared SHA-256. Not historical authentication."""
import hashlib
from pathlib import Path

def verify_source_bytes(manifest, root):
    if not isinstance(manifest, list) or not manifest:
        raise ValueError("manifest must be nonempty list")
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be directory")
    seen, results = set(), []
    for item in manifest:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ValueError("invalid manifest entry")
        rel, expected = item["path"], item["sha256"]
        if not isinstance(rel, str) or not rel or not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise ValueError("invalid path or digest")
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts or rel in seen:
            raise ValueError("unsafe or duplicate path")
        seen.add(rel)
        resolved = (root / p).resolve(strict=True)
        if not resolved.is_relative_to(root) or not resolved.is_file():
            raise ValueError("source outside root or not file")
        h, size = hashlib.sha256(), 0
        with resolved.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                h.update(chunk)
                size += len(chunk)
        results.append({"path": rel, "size_bytes": size, "sha256_matches": h.hexdigest() == expected})
    return {"files": results, "all_bytes_match": all(r["sha256_matches"] for r in results), "historical_source_authenticated": False, "licensing_authenticated": False}
