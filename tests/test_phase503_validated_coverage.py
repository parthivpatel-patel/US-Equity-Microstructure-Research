import pytest
from phase503_validated_coverage import validated_coverage


def row(day='2025-10-01', period='pre', **changes):
    d = dict(exchange='X', date=day, period=period, treated_eligible=2,
             treated_observed=1, control_eligible=2, control_observed=2)
    d.update(changes)
    return d


def test_valid_gap():
    out = validated_coverage([row()])[0]
    assert out['common_date_equal_weight_gap'] == -0.5
    assert out['common_date_eligible_weight_gap'] == -0.5


def test_cutoff_is_post():
    assert validated_coverage([row('2025-11-03', 'post')])[0]['period'] == 'post'

@pytest.mark.parametrize('change', [
    dict(date='20251001'), dict(date='2025-02-30'), dict(period='post'),
    dict(treated_observed=3), dict(treated_eligible=True), dict(exchange=' '),
    dict(control_eligible=-1), dict(date='2025-11-03'),
])
def test_invalid(change):
    with pytest.raises(ValueError):
        validated_coverage([row(**change)])


def test_duplicate():
    with pytest.raises(ValueError):
        validated_coverage([row(), row()])


def test_exclusion():
    with pytest.raises(ValueError):
        validated_coverage([row()], excluded_dates=['2025-10-01'])


def test_zero_common_support():
    out = validated_coverage([row(control_eligible=0, control_observed=0)])[0]
    assert out['common_support_dates'] == 0
    assert out['common_date_equal_weight_gap'] is None


def test_fail_closed_across_rows():
    with pytest.raises(ValueError):
        validated_coverage([row(), row('2025-10-02', 'post')])
