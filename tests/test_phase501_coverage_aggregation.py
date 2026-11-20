import pytest
from phase501_coverage_aggregation import aggregate_coverage

def cell(day,te,to,ce,co,period='pre',ex='X'):
    return dict(exchange=ex,date=day,period=period,treated_eligible=te,treated_observed=to,control_eligible=ce,control_observed=co)

def test_weighting_sensitivity_is_exposed():
    r=aggregate_coverage([cell('a',1,1,1,0),cell('b',9,0,1,1)])[0]
    assert r['common_date_equal_weight_gap']==0
    assert r['common_date_eligible_weight_gap']==pytest.approx(-0.4)
    assert r['common_date_gap_weighting_difference']==pytest.approx(0.4)

def test_missing_group_excluded_only_from_common_support():
    r=aggregate_coverage([cell('a',1,1,0,0),cell('b',1,0,1,1)])[0]
    assert r['excluded_dates']==1 and r['common_support_dates']==1
    assert r['treated_coverage_all']==0.5 and r['control_coverage_all']==1
    assert r['common_date_equal_weight_gap']==-1

def test_no_common_support_is_undefined():
    r=aggregate_coverage([cell('a',1,1,0,0),cell('b',0,0,1,1)])[0]
    assert r['common_date_equal_weight_gap'] is None
    assert r['common_date_eligible_weight_gap'] is None

def test_separate_exchange_periods():
    r=aggregate_coverage([cell('a',1,1,1,1),cell('b',1,1,1,1,'post'),cell('a',1,1,1,1,ex='Y')])
    assert len(r)==3

@pytest.mark.parametrize('rows', [[],[cell('a',1,2,1,1)],[cell('a',1,1,1,1),cell('a',1,1,1,1)],[cell('a',True,1,1,1)]])
def test_invalid_input(rows):
    with pytest.raises(ValueError): aggregate_coverage(rows)
