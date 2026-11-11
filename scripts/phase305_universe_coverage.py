"""Declared-universe coverage gate; synthetic diagnostics, not source authentication."""
from collections import Counter
from datetime import date

def audit_declared_universe(rows, expected_pairs, expected_dates):
    if not all(isinstance(x, list) for x in (rows, expected_pairs, expected_dates)):
        raise ValueError("inputs must be lists")
    if not expected_pairs or not expected_dates:
        raise ValueError("declared universe and dates cannot be empty")
    def ident(x):
        if type(x) is not str or not x or x != x.strip():
            raise ValueError("invalid identifier")
        return x
    def day(x):
        if type(x) is not str:
            raise ValueError("date must be a string")
        try:
            d = date.fromisoformat(x)
        except ValueError as exc:
            raise ValueError("invalid ISO date") from exc
        if d.isoformat() != x or d.weekday() >= 5:
            raise ValueError("noncanonical or weekend date")
        return x
    pairs = []
    for pair in expected_pairs:
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError("pair must contain security and exchange")
        pairs.append((ident(pair[0]), ident(pair[1])))
    days = [day(x) for x in expected_dates]
    if len(set(pairs)) != len(pairs) or len(set(days)) != len(days) or days != sorted(days):
        raise ValueError("declared universe must be unique and dates ordered")
    observed = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("row must be a dictionary")
        observed.append((ident(row.get("security")), ident(row.get("exchange")), day(row.get("date"))))
    counts = Counter(observed)
    expected = {(s, e, d) for s, e in pairs for d in days}
    missing = sorted(expected - counts.keys())
    unexpected = sorted(counts.keys() - expected)
    duplicates = sorted((s, e, d, n) for (s, e, d), n in counts.items() if n > 1)
    absent_pairs = sorted(set(pairs) - {(s, e) for s, e, _ in counts})
    return {"declared_cells": len(expected), "observed_unique_cells": len(counts),
            "missing_cells": missing, "unexpected_cells": unexpected,
            "duplicate_cells": duplicates, "entirely_absent_pairs": absent_pairs,
            "structurally_complete": not (missing or unexpected or duplicates),
            "universe_authenticated": False, "source_authenticated": False,
            "calendar_authenticated": False, "causal_inference_authorized": False}
