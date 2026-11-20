import pytest
from phase498_exclusion_audit import audit_exclusions

def fixture():
    eligible = [(s, 'X', d) for s in ('A', 'B') for d in ('2025-10-01', '2025-10-03')]
    eligible.append(('C', 'X', '2025-10-01'))
    return eligible

def test_one_sided_missing_unit_is_visible():
    eligible = fixture()
    actual = audit_exclusions(eligible, eligible[:-1], '2025-10-03')['X']
    assert actual['all_eligible_units'] == 3
    assert actual['two_sided_units'] == 2
    assert actual['excluded_one_sided_units'] == 1
    assert actual['excluded_one_sided_missing_observations'] == 1
    assert actual['all_eligible_observation_coverage'] == '4/5'

def test_full_observation_keeps_exclusion_visible():
    eligible = fixture()
    actual = audit_exclusions(eligible, eligible, '2025-10-03')['X']
    assert actual['excluded_one_sided_units'] == 1
    assert actual['excluded_one_sided_missing_observations'] == 0

def test_noncanonical_cutoff_rejected():
    eligible = fixture()
    with pytest.raises(ValueError, match='noncanonical'):
        audit_exclusions(eligible, eligible, '20251003')

def test_duplicate_rejected():
    eligible = fixture()
    with pytest.raises(ValueError, match='duplicate'):
        audit_exclusions(eligible + eligible[:1], eligible, '2025-10-03')

def test_outside_universe_rejected():
    eligible = fixture()
    with pytest.raises(ValueError, match='out-of-universe'):
        audit_exclusions(eligible, eligible + [('Z', 'X', '2025-10-01')], '2025-10-03')
