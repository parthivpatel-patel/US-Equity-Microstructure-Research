import pytest
from phase504_support_attrition import support_attrition


def row(day, te, to, ce, co, **kw):
    return dict(exchange='X', date=day, treated_eligible=te, treated_observed=to,
                control_eligible=ce, control_observed=co, **kw)


def test_support_selection_changes_coverage():
    a = support_attrition([row('2025-10-01', 2, 2, 2, 2), row('2025-10-02', 2, 0, 0, 0)])[0]
    assert a['all_dates'] == 2 and a['common_dates'] == 1
    assert a['treated_coverage_all'] == .5
    assert a['treated_coverage_common'] == 1
    assert a['treated_eligible_excluded'] == 2


def test_no_common_support_is_explicit():
    a = support_attrition([row('2025-10-01', 1, 1, 0, 0)])[0]
    assert a['common_dates'] == 0 and a['control_coverage_common'] is None


def test_period_boundary():
    a = support_attrition([row('2025-11-02', 1, 1, 1, 1), row('2025-11-03', 1, 1, 1, 1)])
    assert [x['period'] for x in a] == ['post', 'pre']

@pytest.mark.parametrize('bad', [
    row('20251001', 1, 1, 1, 1), row('2025-02-30', 1, 1, 1, 1),
    row('2025-10-01', 1, 2, 1, 1), row('2025-10-01', True, 1, 1, 1),
    row('2025-10-01', 0, 0, 0, 0), row('2025-10-01', 1, 1, 1, 1, period='post')
])
def test_invalid_rows(bad):
    with pytest.raises(ValueError): support_attrition([bad])


def test_duplicates():
    r = row('2025-10-01', 1, 1, 1, 1)
    with pytest.raises(ValueError): support_attrition([r, r])


def test_empty():
    with pytest.raises(ValueError): support_attrition([])
