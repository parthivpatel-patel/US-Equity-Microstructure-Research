"""Phase 439: strict structural preflight before source-bound panel diagnostics.

Not SEC provenance authentication or causal inference.
Run: python scripts/phase439_verified_entrypoint.py panel.csv --output report.json
"""
import argparse
import json
from pathlib import Path
from phase438_csv_integrity import audit_bytes
from phase437_source_bound_gate import evaluate_bytes

def evaluate_verified_bytes(raw):
    structural = audit_bytes(raw)
    panel = evaluate_bytes(raw)
    if (panel.get('source_sha256') != structural['source_sha256'] or
            panel.get('source_bytes') != structural['source_bytes']):
        raise ValueError('source digest/length mismatch between structural and panel audits')
    for key in ('daily', 'calendar'):
        report = panel.get(key)
        if not isinstance(report, dict) or report.get('source_sha256') != structural['source_sha256'] or report.get('source_bytes') != structural['source_bytes']:
            raise ValueError(f'{key} report missing or mismatched source fingerprint')
    panel['structural_integrity'] = structural
    panel['source_authentication'] = 'NOT VERIFIED: SHA-256 consistency is not proof of SEC origin or treatment assignment'
    panel['historical_effect_estimated'] = False
    return panel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = evaluate_verified_bytes(Path(args.input_csv).read_bytes())
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    if not result['pass']:
        raise SystemExit(2)

if __name__ == '__main__':
    main()
