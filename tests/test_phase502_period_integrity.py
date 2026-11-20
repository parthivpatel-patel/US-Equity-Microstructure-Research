import pytest
from phase502_period_integrity import audit_periods, canonical_day

def row(day, period):
    return {'exchange':'X', 'date':day, 'period':period,
            'treated_eligible':1,'treated_observed':1,
            'control_eligible':1,'control_observed':1}

def test_cutoff_is_post():
    assert [r['period'] for r in audit_periods([row('2025-11-02','pre'),row('2025-11-03','post')])] == ['pre','post']

def test_reject_mislabeled_pre():
    with pytest.raises(ValueError,match='period disagrees'): audit_periods([row('2025-11-04','pre')])

def test_reject_mislabeled_post():
    with pytest.raises(ValueError,match='period disagrees'): audit_periods([row('2025-10-03','post')])

@pytest.mark.parametrize('bad',['20251103','2025-2-03','2025-02-30','2025-11-03T00:00:00',None])
def test_reject_noncanonical_or_invalid_dates(bad):
    with pytest.raises(ValueError): canonical_day(bad)

def test_reject_excluded_date():
    with pytest.raises(ValueError,match='excluded'): audit_periods([row('2025-11-03','post')],excluded_dates=['2025-11-03'])

def test_no_input_mutation():
    r=row('2025-11-03','post')
    assert audit_periods([r])[0] == r
    assert audit_periods([r])[0] is not r

def test_empty_rejected():
    with pytest.raises(ValueError): audit_periods([])
