import pytest
from phase500_date_coverage import date_coverage

E = [('T','X','2025-10-01'),('C','X','2025-10-01'),('T','X','2025-10-03'),('C','X','2025-10-03')]
G = {'T':1,'C':0}

def test_date_gap_and_period():
    r = date_coverage(E,E[:-1],G,'2025-10-03')
    assert len(r)==2 and r[0]['period']=='pre' and r[1]['period']=='post'
    assert r[1]['coverage_gap_treated_minus_control']==1.0
    assert r[1]['both_groups_observed'] is False

def test_missing_group_is_not_zero_coverage():
    r = date_coverage(E[:1],[],G,'2025-10-03')[0]
    assert r['control_coverage'] is None and r['coverage_gap_treated_minus_control'] is None
    assert r['treated_coverage']==0.0

def test_explicit_observed_key_is_counted():
    r = date_coverage(E,E,G,'2025-10-03')
    assert all(x['both_groups_observed'] and x['coverage_gap_treated_minus_control']==0 for x in r)

def test_duplicate_rejected():
    with pytest.raises(ValueError,match='duplicate'):
        date_coverage(E+E[:1],E,G,'2025-10-03')

def test_outside_universe_rejected():
    with pytest.raises(ValueError,match='out-of-universe'):
        date_coverage(E,E+[('Z','X','2025-10-01')],G,'2025-10-03')

def test_invalid_label_rejected():
    with pytest.raises(ValueError,match='treatment'):
        date_coverage(E,E,{**G,'T':2},'2025-10-03')

@pytest.mark.parametrize('cutoff', ['20251003','2025-02-30'])
def test_bad_cutoff(cutoff):
    with pytest.raises(ValueError):
        date_coverage(E,E,G,cutoff)

def test_missing_date_not_conflated_with_missing_group():
    r = date_coverage(E[:2],E[:1],G,'2025-10-03')[0]
    assert r['control_coverage']==0.0 and r['both_groups_eligible']
