"""Combined structural and exact-integer gate for a canonical CSV panel.

Requires phase371_panel_gate.py and phase372_exact_integer_gate.py beside this file.
Neither gate authenticates original SEC data or historical treatment assignments.
"""
import argparse
import json
from pathlib import Path

from phase371_panel_gate import audit as structural_audit
from phase372_exact_integer_gate import audit as integer_audit


def audit(path):
    """Run both audits; fail closed on disagreement or either audit failure."""
    structural = structural_audit(path)
    exact = integer_audit(path)
    return {
        'passed': bool(structural['passed'] and exact['passed'] and
                       structural['rows'] == exact['rows']),
        'structural': structural,
        'exact_integer': exact,
        'source_authenticated': False,
        'treatment_authenticated': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_path')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = audit(args.csv_path)
    output = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
    print(output, end='')
    raise SystemExit(0 if result['passed'] else 2)


if __name__ == '__main__':
    main()
