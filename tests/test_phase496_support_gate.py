import pytest
from phase496_support_gate import support_gate

def fixture():
    e = [(s,'X',d) for s in ('A','B') for d in ('2025-10-01','2025-10-03')]
    return e, {'A':1,'B':0}

def test_admits_complete_common_support():
    e,t=fixture(); r=support_gate(e,e,t,'2025-10-03')
    assert r['admitted_exchanges']==['X']
    assert r['exchanges']['X']['common_pre_dates']==['2025-10-01']

def test_missing_observation_fails():
    e,t=fixture(); r=support_gate(e,e[:-1],t,'2025-10-03')
    assert r['admitted_exchanges']==[]

def test_disjoint_dates_fail():
    e=[('A','X','2025-10-01'),('A','X','2025-10-03'),('B','X','2025-10-02'),('B','X','2025-10-04')]
    assert support_gate(e,e,{'A':1,'B':0},'2025-10-03')['admitted_exchanges']==[]

def test_missing_control_fails():
    e,t=fixture(); assert support_gate(e,e,{'A':1,'B':1},'2025-10-03')['admitted_exchanges']==[]

def test_duplicate_rejected():
    e,t=fixture()
    with pytest.raises(ValueError,match='duplicate'): support_gate(e+e[:1],e,t,'2025-10-03')

def test_invalid_cutoff_rejected():
    e,t=fixture()
    with pytest.raises(ValueError,match='cutoff'): support_gate(e,e,t,'2025-99-03')

def test_outside_universe_rejected():
    e,t=fixture()
    with pytest.raises(ValueError,match='out-of-universe'): support_gate(e,e+[('Z','X','2025-10-01')],t,'2025-10-03')

def test_threshold():
    e,t=fixture(); assert support_gate(e,e,t,'2025-10-03',2)['admitted_exchanges']==[]


def test_compact_cutoff_rejected_instead_of_lexical_misclassification():
    e, t = fixture()
    with pytest.raises(ValueError, match='noncanonical cutoff'):
        support_gate(e, e, t, '20251003')

def test_canonical_cutoff_still_admitted():
    e, t = fixture()
    assert support_gate(e, e, t, '2025-10-03')['admitted_exchanges'] == ['X']
