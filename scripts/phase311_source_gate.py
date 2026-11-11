"""Fail-closed authentication gate for locally acquired SEC panel sources.

A matching hash authenticates bytes against a *trusted independently recorded*
expected digest; it does not authenticate the issuer or methodology by itself.
"""
import hashlib
import json
import re
from pathlib import Path

SHA256 = re.compile(r'^[0-9a-f]{64}$')


def verify_sources(manifest_path, root):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or not isinstance(manifest.get('sources'), list) or not manifest['sources']:
        raise ValueError('nonempty sources array required')
    root = Path(root).resolve(strict=True)
    seen = set()
    verified = []
    for entry in manifest['sources']:
        if not isinstance(entry, dict):
            raise ValueError('invalid source record')
        name = entry.get('path')
        digest = entry.get('sha256')
        url = entry.get('source_url')
        retrieved = entry.get('retrieved_utc')
        if not all(isinstance(x, str) and x.strip() for x in (name, digest, url, retrieved)):
            raise ValueError('source provenance incomplete')
        if not SHA256.fullmatch(digest):
            raise ValueError('invalid sha256')
        if not url.startswith('https://') or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', retrieved):
            raise ValueError('invalid provenance metadata')
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts or name in seen:
            raise ValueError('unsafe or duplicate source path')
        seen.add(name)
        path = (root / rel).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('source outside root or not file')
        with path.open('rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != digest:
            raise ValueError(f'checksum mismatch: {name}')
        verified.append({'path': name, 'sha256': actual, 'bytes': path.stat().st_size})
    return verified
