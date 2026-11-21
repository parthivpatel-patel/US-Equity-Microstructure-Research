#!/usr/bin/env python3
"""Audit local historical listing-venue round-lot snapshot vs stock-level study panel.

Input files are not redistributed. Snapshot content is not independently source-authenticated.
"""
import argparse,csv,hashlib,json,collections
from pathlib import Path

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def audit(nyse_path,nasdaq_path,panel_path):
    with open(nyse_path,encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=['Measurement Month','Trade Date','Symbol','Refsym','Listed Mic','Round Lot Size']:
            raise ValueError('Unexpected NYSE columns')
        rows=list(reader)
    if not rows or any(r['Measurement Month']!='202509' or r['Trade Date']!='20251031' for r in rows):
        raise ValueError('NYSE source does not consistently identify September 2025 measurement and October 31 date')
    if any(r['Round Lot Size'] not in {'1','10','40','100'} for r in rows):
        raise ValueError('Unexpected NYSE lot size')
    if any(not r['Symbol'] or not r['Refsym'] for r in rows): raise ValueError('Missing NYSE symbol/refsym')
    if len(set(r['Symbol'] for r in rows))!=len(rows): raise ValueError('Duplicate NYSE symbol')
    if len(set(r['Refsym'] for r in rows))!=len(rows): raise ValueError('Duplicate NYSE reference symbol')
    with open(nasdaq_path,encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=['evaluation_period','issue_id','ticker','average_closing_price','round_lot']:
            raise ValueError('Unexpected Nasdaq columns')
        nr=list(reader)
    invalid=[r for r in nr if r['evaluation_period']!='202609' or not r['ticker'] or not r['round_lot']]
    with open(panel_path,encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if not {'Ticker','treated'}.issubset(set(reader.fieldnames or [])):raise ValueError('Missing panel columns')
        panel=list(reader)
    if any(r['treated'] not in {'0','1'} for r in panel):raise ValueError('Bad panel label')
    nyse_symbols={r['Symbol'] for r in rows}
    panel_symbols={r['Ticker'] for r in panel}
    nyse_lots=collections.Counter(r['Round Lot Size'] for r in rows)
    nyse_mics=collections.Counter(r['Listed Mic'] for r in rows)
    return {
        'scope':'Local-file integrity and cross-source overlap; NOT independently authenticated NYSE/Nasdaq feed or SEC original',
        'inputs':{'nyse_file_sha256':sha256(nyse_path),'nasdaq_file_sha256':sha256(nasdaq_path),'processed_panel_sha256':sha256(panel_path)},
        'nyse_snapshot':{'measurement_month':'202509','trade_date':'20251031','rows':len(rows),'unique_symbols':len(nyse_symbols),'lot_size_counts':dict(sorted(nyse_lots.items(),key=lambda x:int(x[0]))),'listed_mic_counts':dict(sorted(nyse_mics.items()))},
        'nasdaq_file':{'valid_202609_rows':len(nr)-len(invalid),'invalid_or_non_data_rows':len(invalid),'historical_202509_rows':sum(r['evaluation_period']=='202509' for r in nr),'usable_as_2025_treatment_roster':False},
        'study_panel':{'rows':len(panel),'unique_tickers':len(panel_symbols),'treated_rows':sum(r['treated']=='1' for r in panel)},
        'overlap':{'panel_tickers_in_nyse_listing_snapshot':len(panel_symbols & nyse_symbols),'treated_panel_tickers_in_nyse_listing_snapshot':len({r['Ticker'] for r in panel if r['treated']=='1'} & nyse_symbols)},
        'interpretation':'NYSE file is a potentially useful September 2025 measurement-month cross-venue historical roster, but 0 study ticker overlap prevents direct authentication of Nasdaq treated cohort. The Nasdaq file is dated September 2026 and cannot authenticate November 2025 assignments. Source origin and completeness remain unverified.'
    }

def main():
    p=argparse.ArgumentParser();p.add_argument('nyse');p.add_argument('nasdaq');p.add_argument('panel');args=p.parse_args()
    print(json.dumps(audit(args.nyse,args.nasdaq,args.panel),indent=2,sort_keys=True))
if __name__=='__main__':main()
