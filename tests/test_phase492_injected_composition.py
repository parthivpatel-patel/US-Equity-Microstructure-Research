"""Deterministic tests; run pytest -q tests/test_phase492_injected_composition.py."""
import csv
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase492_injected_composition import audit

def write(path, header, rows):
    with path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def fixture(tmp_path):
    e, p = tmp_path/'e.csv', tmp_path/'p.csv'
    write(e, ['security','exchange','date'], [('A','X','2025-10-01'),('A','X','2025-10-02'),('B','Y','2025-10-02')])
    write(p, ['security','exchange','date','outcome'], [('A','X','2025-10-01','0'),('B','Y','2025-10-02','2')])
    return e, p

def test_coverage(tmp_path):
    e,p = fixture(tmp_path)
    r = audit(e,p,'2025-10-02')
    assert r['pre']['observed_zero_cells'] == 1
    assert r['post']['missing_eligible_cells'] == 1
    assert r['eligible_unit_composition'] == {'both':1,'pre_only':0,'post_only':1}
    assert r['observed_unit_composition'] == {'both':0,'pre_only':1,'post_only':1}

def test_invalid_cutoff(tmp_path):
    e,p = fixture(tmp_path)
    with pytest.raises(ValueError): audit(e,p,'2025-10-01')

def test_extra_csv_column(tmp_path):
    e,p = fixture(tmp_path)
    with p.open('a') as f: f.write('C,X,2025-10-02,1,extra\n')
    with pytest.raises(ValueError, match='malformed CSV row'): audit(e,p,'2025-10-02')

def test_reader_is_injected_without_global_mutation(tmp_path):
    e,p = fixture(tmp_path)
    calls=[]
    from phase490_strict_csv import read_strict
    def custom(path, observed=False):
        calls.append(observed)
        return read_strict(path,observed)
    audit(e,p,'2025-10-02',reader=custom)
    assert calls == [False,True]

def test_outside_eligibility(tmp_path):
    e,p = fixture(tmp_path)
    with p.open('a') as f: f.write('C,X,2025-10-02,1\n')
    with pytest.raises(ValueError,match='outside eligibility'): audit(e,p,'2025-10-02')
