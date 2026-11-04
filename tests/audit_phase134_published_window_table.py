"""Phase 134: validate arithmetic/signs in the already-published Phase 131 table.

This verifies *only* table consistency, not underlying SEC data or causal identification.
Run from repo root: python tests/audit_phase134_published_window_table.py
"""
import csv
import json
import math
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "results" / "phase131_window_sensitivity.csv"
WINDOWS = {3, 5, 7, 10, 15}
with SOURCE.open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))
assert len(rows) == 10, f"Expected 10 rows, got {len(rows)}"
results = {}
for outcome in ("count", "volume"):
    subset = [r for r in rows if r["outcome"] == outcome]
    assert len(subset) == 5
    assert {int(r["window_days"]) for r in subset} == WINDOWS
    subset.sort(key=lambda r: int(r["window_days"]))
    differences = []
    event_signs = []
    diff_signs = []
    for r in subset:
        nov = float(r["november_pp"])
        oct6 = float(r["october6_pp"])
        delta = float(r["nov_minus_oct_pp"])
        assert all(map(math.isfinite, (nov, oct6, delta)))
        assert abs((nov - oct6) - delta) <= 0.0000011, r
        assert 0 <= int(r["pre_placebo_at_least_as_negative"]) <= int(r["pre_placebo_count"])
        assert 0 <= int(r["pre_placebo_at_least_as_extreme_abs"]) <= int(r["pre_placebo_count"])
        differences.append(delta)
        event_signs.append(1 if nov > 0 else (-1 if nov < 0 else 0))
        diff_signs.append(1 if delta > 0 else (-1 if delta < 0 else 0))
    results[outcome] = {
        "windows": sorted(WINDOWS),
        "november_event_signs": event_signs,
        "november_minus_october_signs": diff_signs,
        "difference_min_pp": min(differences),
        "difference_max_pp": max(differences),
    }
assert results["count"]["november_event_signs"] == [-1] * 5
assert results["count"]["november_minus_october_signs"] == [-1, -1, -1, 1, -1]
assert results["volume"]["november_event_signs"] == [-1, -1, 1, -1, -1]
assert results["volume"]["november_minus_october_signs"] == [1] * 5
print(json.dumps(results, indent=2))
