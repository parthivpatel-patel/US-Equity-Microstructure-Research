import csv
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase493_balanced_coverage import audit

def write(p, header, rows):
    with p.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(header); w.writerows(rows)

def sample(tmp_path):
    e,p=tmp_path/'e.csv',tmp_path/'p.csv'
    write(e,['security','exchange','date'], [('A','X','2025-10-01'),('A','X','2025-10-02'),('A','X','2025-10-03'),('B','X','2025-10-01'),('B','X','2025-10-02'),('C','Y','2025-10-03')])
    write(p,['security','exchange','date','outcome'], [('A','X','2025-10-01',0),('A','X','2025-10-03',2),('B','X','2025-10-01',1),('B','X','2025-10-02',0),('C','Y','2025-10-03',4)])
    return e,p

def test_two_sided_not_fully_balanced(tmp_path):
    e,p=sample(tmp_path); r=audit(e,p,'2025-10-02')
    assert (r['eligible_units'],r['both_side_eligible_units'],r['both_side_observed_units'],r['fully_covered_both_side_units'])==(3,2,2,1)
    assert (r['eligible_cells_both_side_units'],r['observed_cells_both_side_units'],r['observed_zero_cells_both_side_units'])==(5,4,2)
    assert r['by_exchange']['X']['fully_covered_both_side_units']==1

def test_cutoff_rejects_one_sided(tmp_path):
    e,p=sample(tmp_path)
    with pytest.raises(ValueError,match='two-sided'): audit(e,p,'2025-10-01')

def test_outside_universe(tmp_path):
    e,p=sample(tmp_path)
    with p.open('a') as f: f.write('Z,X,2025-10-02,1\n')
    with pytest.raises(ValueError,match='out-of-universe'): audit(e,p,'2025-10-02')

def test_malformed_extra_field(tmp_path):
    e,p=sample(tmp_path)
    with p.open('a') as f: f.write('Z,X,2025-10-02,1,extra\n')
    with pytest.raises(ValueError,match='malformed'): audit(e,p,'2025-10-02')

def test_nonfinite(tmp_path):
    e,p=sample(tmp_path)
    with p.open('a') as f: f.write('A,X,2025-10-02,nan\n')
    with pytest.raises(ValueError,match='nonfinite'): audit(e,p,'2025-10-02')

def test_hash_changes(tmp_path):
    e,p=sample(tmp_path); first=audit(e,p,'2025-10-02')['sha256']['panel']
    with p.open('a') as f: f.write('\n')
    assert first != audit(e,p,'2025-10-02')['sha256']['panel']
