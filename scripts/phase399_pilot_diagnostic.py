import csv,datetime,hashlib,json,sys
from collections import defaultdict

def audit(path):
    raw=open(path,'rb').read(); rows=list(csv.DictReader(raw.decode('utf-8-sig').splitlines()))
    d=defaultdict(dict)
    for r in rows:
        day=datetime.datetime.strptime(r['Date'],'%Y%m%d').date(); lot=int(float(r['lot']))
        assert lot in (10,40,100) and lot not in d[day], (day,lot)
        for a,b,c in [('Hidden','TradesForHidden','hidden_trade_rate'),("HiddenVol('000)","TradeVolForHidden('000)",'hidden_volume_rate')]:
            numerator,denominator,rate=map(float,(r[a],r[b],r[c]))
            assert 0<=numerator<=denominator and denominator>0 and abs(numerator/denominator-rate)<1e-10
        d[day][lot]=r
    assert all(set(v)=={10,40,100} for v in d.values())
    periods={'oct_early':('2025-10-01','2025-10-15'),'oct_late':('2025-10-16','2025-10-31'),'nov':('2025-11-03','2025-11-28')}
    out={'source_sha256':hashlib.sha256(raw).hexdigest(),'rows':len(rows),'days':len(d),'periods':{}}
    for name,(start,end) in periods.items():
        dates=[x for x in sorted(d) if start<=x.isoformat()<=end];assert dates
        entry={'days':len(dates),'lots':{}}
        for lot in (10,40,100):
            rs=[d[x][lot] for x in dates]; entry['lots'][str(lot)]={}
            for n,den,key in [('Hidden','TradesForHidden','trade'),("HiddenVol('000)","TradeVolForHidden('000)",'volume')]:
                entry['lots'][str(lot)][key]=sum(float(r[n]) for r in rs)/sum(float(r[den]) for r in rs)
        out['periods'][name]=entry
    out['contrasts']={}
    for lot in ('10','40','100'):
        out['contrasts'][lot]={}
        for metric in ('trade','volume'):
            p=out['periods'];a=p['oct_early']['lots'][lot][metric];b=p['oct_late']['lots'][lot][metric];c=p['nov']['lots'][lot][metric]
            out['contrasts'][lot][metric]={'october_placebo_late_minus_early':b-a,'november_minus_october_late':c-b}
    return out
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2,sort_keys=True))
