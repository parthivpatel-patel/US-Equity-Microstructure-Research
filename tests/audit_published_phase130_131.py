"""Cross-phase output integrity audit. Standard library only; no source-data claims.

Run: python tests/audit_published_phase130_131.py
Reads already published result CSVs, checks consistency and reports descriptive
sensitivity. It does NOT independently reproduce estimates from SEC raw files.
"""
from __future__ import annotations
import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
def d(row, field):
    return Decimal(row[field])
def main():
    p130 = {r["outcome"]: r for r in load("results/phase130_summary.csv")}
    p131 = load("results/phase131_window_sensitivity.csv")
    assert len(p130) == 2 and len(p131) == 10
    for outcome in ("count", "volume"):
        rs = sorted((r for r in p131 if r["outcome"] == outcome),
                    key=lambda r: int(r["window_days"]))
        assert [int(r["window_days"]) for r in rs] == [3, 5, 7, 10, 15]
        assert all(int(r["pre_placebo_count"]) > 0 for r in rs)
        for r in rs:
            n = int(r["pre_placebo_count"])
            for col in ("pre_placebo_at_least_as_negative",
                        "pre_placebo_at_least_as_extreme_abs"):
                assert 0 <= int(r[col]) <= n
            assert abs((d(r,"november_pp")-d(r,"october6_pp"))-
                       d(r,"nov_minus_oct_pp")) <= Decimal("0.000001")
        five = next(r for r in rs if int(r["window_days"]) == 5)
        old = p130[outcome]
        for oldkey, newkey in (("november_pp","november_pp"),
                               ("october_pp","october6_pp"),
                               ("nov_minus_oct_pp","nov_minus_oct_pp")):
            assert abs(d(old,oldkey)-d(five,newkey)) < Decimal("0.000001")
        assert int(old["pre_placebo_n"]) == int(five["pre_placebo_count"])
        assert int(old["pre_placebo_at_least_as_negative"]) == int(
            five["pre_placebo_at_least_as_negative"])
        assert int(old["pre_placebo_at_least_as_extreme_absolute"]) == int(
            five["pre_placebo_at_least_as_extreme_abs"])
        vals = [d(r,"nov_minus_oct_pp") for r in rs]
        print(outcome, "five-window cross-phase checks PASS",
              "Nov-minus-Oct range pp", min(vals), max(vals),
              "signs", ["+" if v > 0 else "-" if v < 0 else "0" for v in vals])
        print("  Nov event sign:",
              ["+" if d(r,"november_pp") > 0 else "-" if d(r,"november_pp") < 0 else "0"
               for r in rs])
        print("  historical abs-extreme counts:",
              [f'{r["pre_placebo_at_least_as_extreme_abs"]}/{r["pre_placebo_count"]}'
               for r in rs])
    assert next(r for r in p131 if r["outcome"]=="count" and r["window_days"]=="10")["nov_minus_oct_pp"] == "0.337165"
    print("All cross-phase table checks PASS; raw-data validation NOT performed.")

if __name__ == "__main__":
    main()
