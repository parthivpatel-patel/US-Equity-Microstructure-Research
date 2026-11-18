"""Fail-closed assignment consistency on the identical bytes used by Phase 439.

Structural and treatment checks are not SEC source authentication.
"""
import argparse
import csv
import io
import json
from pathlib import Path

from phase439_verified_entrypoint import evaluate_verified_bytes
from phase442_assignment_gate import evaluate as assignment_audit


def evaluate_bytes(raw):
    # Phase 439 validates raw CSV bytes before any downstream DictReader.
    report = evaluate_verified_bytes(raw)
    decoded = raw.decode('utf-8-sig')
    assignment = assignment_audit(csv.DictReader(io.StringIO(decoded, newline='')))
    assignment['source_sha256'] = report['source_sha256']
    assignment['source_bytes'] = report['source_bytes']
    report['assignment_scope'] = assignment
    report['pass'] = bool(report.get('pass') is True and assignment['pass'] is True)
    report['treatment_authenticated'] = False
    report['historical_effect_estimated'] = False
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = evaluate_bytes(Path(args.input_csv).read_bytes())
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    if not result['pass']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
