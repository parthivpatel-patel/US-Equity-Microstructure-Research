"""Audit pilot date membership against an explicitly scoped 2025 US-equity calendar.

Calendar is an independently encoded EXPECTATION, not proof of SEC provenance.
Only October-November 2025 supported; November 28 is an early-close session.
"""
import argparse
import csv
import datetime as dt
import json
from collections import Counter

START = dt.date(2025, 10, 1)
END = dt.date(2025, 11, 28)
CLOSED = {dt.date(2025, 11, 27)}  # Thanksgiving; confirm with exchange calendar
TIERS = {10, 40, 100}

def expected_dates():
    days = []
    day = START
    while day <= END:
        if day.weekday() < 5 and day not in CLOSED:
            days.append(day)
        day += dt.timedelta(days=1)
    return set(days)

def parse_date(value):
    value = value.strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError("unsupported date format: " + repr(value))

def audit(path):
    counts = Counter()
    with open(path, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            date = parse_date(row["Date"])
            lot = float(row["lot"])
            if not lot.is_integer() or int(lot) not in TIERS:
                raise ValueError("invalid tier")
            counts[(date, int(lot))] += 1
    expected = expected_dates()
    observed = {day for day, _ in counts}
    duplicates = sorted((str(d), tier, n) for (d, tier), n in counts.items() if n != 1)
    missing_dates = sorted(str(d) for d in expected - observed)
    unexpected_dates = sorted(str(d) for d in observed - expected)
    incomplete = sorted((str(d), sorted(TIERS - {t for x, t in counts if x == d})) for d in observed if {t for x, t in counts if x == d} != TIERS)
    return {"expected_sessions": len(expected), "observed_sessions": len(observed),
            "observed_rows": sum(counts.values()), "missing_dates": missing_dates,
            "unexpected_dates": unexpected_dates, "duplicate_keys": duplicates,
            "incomplete_tiers": incomplete, "calendar_membership_pass":
            not (missing_dates or unexpected_dates or duplicates or incomplete)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    args = parser.parse_args()
    print(json.dumps(audit(args.csv), indent=2))
