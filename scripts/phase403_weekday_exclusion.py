import csv,datetime,collections,sys,json,math

def evaluate(path):
    rows=list(csv.DictReader(open(path,newline='')))
    d=collections.defaultdict(dict)
    for r in rows:
        date=datetime.datetime.strptime(r['Date'],'%Y%m%d').date();lot=int(float(r['lot']))
        assert lot not in d[date]
        d[date][lot]=r
        for n,den,rate in [('Hidden','TradesForHidden','hidden_trade_rate'),("HiddenVol('000)","TradeVolForHidden('000)",'hidden_volume_rate')]:
            assert float(r[den])>0 and 0<=float(r[n])<=float(r[den]) and abs(float(r[n])/float(r[den])-float(r[rate]))<1e-10
    assert all(set(x)=={10,40,100} for x in d.values())
    dates=sorted(d); octdates=[x for x in dates if x.month==10];novdates=[x for x in dates if x.month==11]
    windows={'early_oct':[x for x in octdates if x.day<=15],'late_oct':[x for x in octdates if x.day>15],'nov':[x for x in novdates]}
    def contrast(exclude=None):
        def gap(window,num,den):
            ds=[x for x in windows[window] if exclude is None or x.weekday()!=exclude]
            assert ds
            def rate(lots):
                a=sum(float(d[day][lot][num]) for day in ds for lot in lots)
                b=sum(float(d[day][lot][den]) for day in ds for lot in lots)
                return a/b
            return rate([10,40])-rate([100])
        result={}
        for label,num,den in [('trade','Hidden','TradesForHidden'),('volume',"HiddenVol('000)","TradeVolForHidden('000)")]:
            result[label]={'oct_placebo_pp':100*(gap('late_oct',num,den)-gap('early_oct',num,den)),'nov_contrast_pp':100*(gap('nov',num,den)-gap('late_oct',num,den))}
        return result
    base=contrast();variants={datetime.date(2026,11,16+i).strftime('%A'):contrast(i) for i in range(5)}
    return {'n_rows':len(rows),'n_dates':len(d),'window_dates':{k:len(v) for k,v in windows.items()},'baseline':base,'exclude_weekday':variants,'sign_stable':{out:{metric:all(math.copysign(1,variants[w][out][metric])==math.copysign(1,base[out][metric]) for w in variants) for metric in base[out]} for out in base}}

if __name__=='__main__':print(json.dumps(evaluate(sys.argv[1]),indent=2))
