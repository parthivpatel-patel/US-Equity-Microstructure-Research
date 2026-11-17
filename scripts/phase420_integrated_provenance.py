"""Fail-closed composition of Phase 417 integrity and Phase 419 source policy.

Requires both modules alongside this file. Does not authenticate upstream publisher.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from phase417_provenance_gate import audit
from phase419_source_policy import check_manifest_policy


def integrated_audit(manifest, root, as_of_utc):
    integrity = audit(manifest, root)
    policy = check_manifest_policy(manifest, as_of_utc)
    errors = [f'integrity: {x}' for x in integrity['errors']]
    errors += [f'policy: {x}' for x in policy['errors']]
    return {
        'status': 'BLOCKED' if errors else 'INTEGRITY_AND_POLICY_PASS_NOT_AUTHENTICATED',
        'integrity_status': integrity['status'],
        'policy_status': policy['status'],
        'checked': integrity['checked'],
        'errors': errors,
        'source_authenticated': False,
        'publication_clearance': 'NOT_ESTABLISHED',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--as-of-utc', help='Explicit UTC timestamp for reproducibility; defaults to current UTC')
    args = parser.parse_args()
    as_of = datetime.fromisoformat(args.as_of_utc.replace('Z', '+00:00')) if args.as_of_utc else datetime.now(timezone.utc)
    result = integrated_audit(json.loads(args.manifest.read_text()), args.root, as_of)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'].startswith('INTEGRITY_AND_POLICY_PASS') else 2)


if __name__ == '__main__':
    main()
