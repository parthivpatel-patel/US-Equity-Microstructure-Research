"""Fail-closed provenance gate for locally held historical research inputs."""
import hashlib
import json
from pathlib import Path

REQUIRED = ('path', 'sha256', 'bytes', 'origin_url', 'retrieved_utc', 'license_status', 'role')
ALLOWED = {'redistributable', 'restricted', 'unknown'}

def audit(root, manifest):
    root = Path(root).resolve()
    records = json.loads(Path(manifest).read_text(encoding='utf-8'))
    if not isinstance(records, list):
        raise ValueError('manifest must be an array')
    seen = set()
    results = []
    for row in records:
        if not isinstance(row, dict) or any(k not in row for k in REQUIRED):
            raise ValueError('missing manifest fields')
        rel = row['path']
        if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or '\\' in rel:
            raise ValueError('unsafe path')
        p = (root / rel).resolve()
        if not p.is_relative_to(root) or rel in seen:
            raise ValueError('path escape or duplicate')
        seen.add(rel)
        if row['license_status'] not in ALLOWED:
            raise ValueError('unknown license status value')
        if not isinstance(row['bytes'], int) or isinstance(row['bytes'], bool) or row['bytes'] < 0:
            raise ValueError('invalid byte count')
        digest = row['sha256']
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('invalid sha256')
        exists = p.is_file()
        actual = hashlib.sha256(p.read_bytes()).hexdigest() if exists else None
        size = p.stat().st_size if exists else None
        integrity = exists and actual == digest and size == row['bytes']
        metadata = all(isinstance(row[k], str) and bool(row[k].strip()) for k in ('origin_url','retrieved_utc','role'))
        results.append({'path': rel, 'exists': exists, 'integrity_verified': integrity,
                        'metadata_complete': metadata, 'redistribution_allowed_by_manifest': row['license_status'] == 'redistributable',
                        'eligible_for_review': bool(integrity and metadata and row['license_status'] == 'redistributable')})
    return {'entries': len(results), 'verified': sum(r['integrity_verified'] for r in results),
            'eligible_for_review': sum(r['eligible_for_review'] for r in results), 'records': results,
            'source_authenticated': False, 'redistribution_permission_independently_verified': False}

if __name__ == '__main__':
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument('root'); a.add_argument('manifest')
    args = a.parse_args()
    print(json.dumps(audit(args.root, args.manifest), indent=2))
