"""Bind daily and calendar support diagnostics to identical CSV bytes.

Run: python scripts/phase437_source_bound_gate.py panel.csv --output report.json
This is a structural diagnostic, NOT SEC source authentication or causal inference.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from phase432_daily_fixed_support import audit as daily_audit
from phase433_calendar_support import audit as calendar_audit
from phase435_integrated_gate import evaluate

def evaluate_bytes(raw):
    if not isinstance(raw, bytes) or not raw:
        raise ValueError("nonempty CSV bytes required")
    digest = hashlib.sha256(raw).hexdigest()
    try:
        decoded = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV must be UTF-8") from exc
    daily = daily_audit(csv.DictReader(io.StringIO(decoded, newline="")))
    calendar = calendar_audit(csv.DictReader(io.StringIO(decoded, newline="")))
    for report in (daily, calendar):
        report["source_sha256"] = digest
        report["source_bytes"] = len(raw)
    gate = evaluate(daily, calendar)
    gate.update(source_sha256=digest, source_bytes=len(raw),
                daily=daily, calendar=calendar,
                source_authentication="NOT VERIFIED: byte identity is not SEC origin or treatment authentication",
                historical_effect_estimated=False)
    return gate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = evaluate_bytes(Path(args.input_csv).read_bytes())
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result["pass"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
