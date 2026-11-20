"""Strict CSV entry point for Phase 488 composition diagnostics.

Reuses Phase 488's existing summary logic with Phase 490 input validation.
Does not authenticate the underlying historical sources.
"""
import argparse
import json
from pathlib import Path
import phase488_period_composition as composition
from phase490_strict_csv import read_strict


def audit(eligibility, panel, cutoff):
    original = composition.read
    try:
        composition.read = read_strict
        return composition.audit(eligibility, panel, cutoff)
    finally:
        composition.read = original


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--eligibility', required=True)
    parser.add_argument('--panel', required=True)
    parser.add_argument('--cutoff', required=True)
    parser.add_argument('--output')
    args = parser.parse_args()
    payload = json.dumps(audit(args.eligibility, args.panel, args.cutoff), indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(payload, encoding='utf-8')
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
