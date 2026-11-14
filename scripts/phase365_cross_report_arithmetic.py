"""Exact arithmetic checks of archived report values; NOT SEC-panel re-estimation."""
from decimal import Decimal as D
from fractions import Fraction
def audit():
    rows=[("trade","-1.335781","-0.601120","-0.734661",2),("volume","-0.006939","-0.633537","+0.626598",48)]
    result={}
    for label,nov,oct_,expected,n in rows:
        delta=D(nov)-D(oct_)
        assert delta==D(expected)
        result[label]={"delta_pp":str(delta),"placebo_rank":f"{n}/78","fraction":str(Fraction(n,78))}
    shift=D("+0.014789")-D("-0.025721")
    assert shift==D("+0.040510")
    result["phase2_volume_adjustment_rate_units"]=str(shift)
    return result
if __name__=="__main__":
    import json
    print(json.dumps(audit(),indent=2))
