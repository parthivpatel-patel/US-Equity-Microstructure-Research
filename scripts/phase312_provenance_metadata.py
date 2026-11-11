"""Supplemental metadata and canonical-path checks before Phase 311 byte validation."""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from scripts.phase311_source_gate import verify_sources


def verify_manifest_strict(manifest_path, root):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or not isinstance(manifest.get('sources'), list) or not manifest['sources']:
        raise ValueError('nonempty sources required')
    root = Path(root).resolve(strict=True)
    canonical = set()
    for entry in manifest['sources']:
        if not isinstance(entry, dict):
            raise ValueError('invalid source entry')
        stamp = entry.get('retrieved_utc')
        if not isinstance(stamp, str):
            raise ValueError('missing timestamp')
        try:
            parsed = datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        except ValueError as exc:
            raise ValueError('invalid calendar timestamp') from exc
        if parsed.strftime('%Y-%m-%dT%H:%M:%SZ') != stamp:
            raise ValueError('noncanonical timestamp')
        url = entry.get('source_url')
        if not isinstance(url, str):
            raise ValueError('missing URL')
        parts = urlsplit(url)
        if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password or parts.fragment or not parts.netloc or any(c.isspace() for c in url):
            raise ValueError('invalid source URL')
        name = entry.get('path')
        if not isinstance(name, str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('invalid source path')
        target = (root / name).resolve(strict=True)
        if not target.is_relative_to(root) or target in canonical:
            raise ValueError('duplicate canonical file or escape')
        canonical.add(target)
    return verify_sources(manifest_path, root)
