import csv
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from phase495_common_date_support import common_date_audit

def write(path, columns, rows):
    with path.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(columns); w.writerows(rows)

def test_fully_covered_units_without_common_dates(tmp_path):
    e, p = tmp_path/"e.csv", tmp_path/"p.csv"
    rows = [("A","X","2025-10-01"),("A","X","2025-10-03"),
            ("B","X","2025-10-02"),("B","X","2025-10-04")]
    write(e, ["security","exchange","date"], rows)
    write(p, ["security","exchange","date","outcome"], [(*r,0) for r in rows])
    result = common_date_audit(e,p,"2025-10-03")
    assert result["fully_covered_paired_units"] == 2
    assert result["common_full_dates"] == []
    assert result["common_eligible_dates_all_paired"] == {"pre":0,"post":0}

def test_common_dates_exist(tmp_path):
    e, p = tmp_path/"e.csv", tmp_path/"p.csv"
    rows = [(s,"X",d) for s in ("A","B") for d in ("2025-10-01","2025-10-03")]
    write(e, ["security","exchange","date"], rows)
    write(p, ["security","exchange","date","outcome"], [(*r,1) for r in rows])
    result = common_date_audit(e,p,"2025-10-03")
    assert result["common_full_dates"] == ["2025-10-01","2025-10-03"]

def test_reject_out_of_universe(tmp_path):
    e, p = tmp_path/"e.csv", tmp_path/"p.csv"
    write(e, ["security","exchange","date"], [("A","X","2025-10-01"),("A","X","2025-10-03")])
    write(p, ["security","exchange","date","outcome"], [("Z","X","2025-10-01",1)])
    with pytest.raises(ValueError, match="out-of-universe"):
        common_date_audit(e,p,"2025-10-03")
