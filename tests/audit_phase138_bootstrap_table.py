"""Audit published Phase 137 bootstrap intervals; Python standard library only.

Usage: python tests/audit_phase138_bootstrap_table.py results/phase137_block_bootstrap.csv
This does NOT rerun the underlying bootstrap or authenticate SEC source data.
"""
import csv
import math
import sys
from pathlib import Path

OUTCOMES = ("count", "volume")
PERIODS = ("July-September", "July-October")
BLOCKS = (3, 5, 10, 15)

def audit(path):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    expected = {(o, p, b) for o in OUTCOMES for p in PERIODS for b in BLOCKS}
    assert len(rows) == 16, f"Expected 16 rows, got {len(rows)}"
    found = set()
    for r in rows:
        key = (r["outcome"], r["period"], int(r["block_days"]))
        assert key in expected and key not in found, f"Unexpected/duplicate: {key}"
        found.add(key)
        assert int(r["draws"]) == 2000
        assert int(r["groups"]) == 68
        assert int(r["dates"]) == (64 if r["period"] == "July-September" else 87)
        beta, lo, hi = (float(r[k]) for k in
                        ("slope_pp_per_day", "bootstrap_95_low", "bootstrap_95_high"))
        assert all(map(math.isfinite, (beta, lo, hi))) and lo <= hi
        width = hi - lo
        excludes_zero = lo > 0 or hi < 0
        print(f"{key[0]:6} {key[1]:14} block={key[2]:2} "
              f"slope={beta:+.9f} width={width:.6f} excludes_zero={excludes_zero}")
    assert found == expected
    for outcome in OUTCOMES:
        for period in PERIODS:
            subset = [r for r in rows if r["outcome"] == outcome and r["period"] == period]
            slopes = [float(r["slope_pp_per_day"]) for r in subset]
            assert max(slopes) - min(slopes) < 1e-10, (outcome, period)
    print("PASS: 16 unique specifications; finite, coherent intervals and invariant slopes.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tests/audit_phase138_bootstrap_table.py PATH.csv")
    audit(sys.argv[1])
