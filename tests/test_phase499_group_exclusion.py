import pytest
from phase499_group_exclusion import group_exclusion_audit

E = [('T','X','2025-10-01'),('T','X','2025-10-03'),('C','X','2025-10-01'),('C','X','2025-10-03'),('S','X','2025-10-01')]
G = {'T':1,'C':0,'S':1}

def test_stratification_and_one_sided_missing():
    r=group_exclusion_audit(E,E[:-1],G,'2025-10-03')['X']
    assert r['1']['one_sided_missing_rows']==1
    assert r['1']['eligible_rows']==3 and r['1']['observed_rows']==2
    assert r['0']['eligible_rows']==2 and r['0']['observed_rows']==2

def test_observed_zero_rows_is_allowed():
    assert group_exclusion_audit(E,[],G,'2025-10-03')['X']['0']['two_sided_missing_rows']==2

def test_duplicate():
    with pytest.raises(ValueError,match='duplicate'):
        group_exclusion_audit(E+E[:1],E,G,'2025-10-03')

def test_out_of_universe():
    with pytest.raises(ValueError,match='out-of-universe'):
        group_exclusion_audit(E,E+[('Z','X','2025-10-01')],G,'2025-10-03')

def test_bad_label():
    with pytest.raises(ValueError,match='treatment'):
        group_exclusion_audit(E,E,{**G,'T':2},'2025-10-03')

def test_bad_cutoff():
    with pytest.raises(ValueError,match='noncanonical'):
        group_exclusion_audit(E,E,G,'20251003')
