"""Fail-closed source manifest reconciliation. Integrity is not provenance."""
import csv, hashlib, json
from pathlib import Path

def rows(path, required):
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader=csv.DictReader(f, strict=True)
        if not reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames) or not set(required)<=set(reader.fieldnames):
            raise ValueError('invalid headers')
        data=list(reader)
    if not data or any(None in row or any(v is None for v in row.values()) for row in data):
        raise ValueError('invalid rows')
    return data

def audit(records_path, manifest_path, source_root=None):
    records=rows(records_path, {'source_sha256','placebo_date','estimand'})
    manifest=rows(manifest_path, {'source_sha256','relative_path','redistribution_status'})
    lookup={}
    def digest(s):
        if len(s)!=64 or any(c not in '0123456789abcdef' for c in s):
            raise ValueError('invalid SHA-256')
        return s
    for row in manifest:
        h=digest(row['source_sha256'])
        p=Path(row['relative_path'])
        if h in lookup: raise ValueError('duplicate manifest digest')
        if p.is_absolute() or not p.parts or any(x in ('.','..') for x in p.parts) or '\\' in row['relative_path']:
            raise ValueError('unsafe source path')
        lookup[h]=row
    referenced={digest(r['source_sha256']) for r in records}
    missing=sorted(referenced-lookup.keys())
    verified=[]; absent=[]
    if source_root is not None:
        root=Path(source_root).resolve(strict=True)
        for h in sorted(referenced & lookup.keys()):
            path=(root/lookup[h]['relative_path']).resolve()
            if not path.is_relative_to(root): raise ValueError('path escapes source root')
            if not path.is_file():
                absent.append(h); continue
            sha=hashlib.sha256()
            with path.open('rb') as f:
                for chunk in iter(lambda:f.read(1048576),b''): sha.update(chunk)
            if sha.hexdigest()!=h: raise ValueError('source checksum mismatch')
            verified.append(h)
    return dict(placebo_records=len(records), referenced_unique_sources=len(referenced),
                missing_manifest_digests=missing, missing_local_source_digests=absent,
                locally_checksum_verified_digests=verified, source_bytes_checked=source_root is not None,
                source_origin_authenticated=False, redistribution_authorized=False,
                empirical_inference_ready=False)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('placebo_csv'); p.add_argument('manifest_csv'); p.add_argument('--source-root')
    a=p.parse_args()
    print(json.dumps(audit(a.placebo_csv,a.manifest_csv,a.source_root),indent=2))
