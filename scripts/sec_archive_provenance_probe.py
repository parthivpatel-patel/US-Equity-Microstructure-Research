#!/usr/bin/env python3
"""Acquire SEC original Q3/Q4 2025 ZIPs and publish provenance metadata only.

No raw archive, member, or underlying observation is uploaded to GitHub.
A successful HTTP download alone does not authenticate the SEC dataset's
lineage or verify treatment assignment. Run on GitHub Actions or locally.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.request
import zipfile

BASE = 'https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security-exchange/individual_security_exchange_2025_{}.zip'


def fetch(q, directory, user_agent, attempts=3):
    url = BASE.format(q)
    result = {'quarter': q, 'url': url, 'attempts': [], 'status': 'failed',
              'retrieved_at_utc': None}
    target = directory / (q + '.zip')
    for attempt in range(1, attempts + 1):
        started = dt.datetime.now(dt.timezone.utc).isoformat()
        log = {'attempt': attempt, 'utc': started}
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': user_agent, 'Accept': 'application/zip,application/octet-stream',
                'Accept-Encoding': 'identity'})
            with urllib.request.urlopen(req, timeout=65) as response, target.open('wb') as out:
                log['http_status'] = response.status
                log['content_type'] = response.headers.get('Content-Type')
                log['content_length'] = response.headers.get('Content-Length')
                sha = hashlib.sha256()
                n = 0
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    n += len(chunk)
                    sha.update(chunk)
                    out.write(chunk)
                log['bytes'] = n
            if not zipfile.is_zipfile(target):
                raise ValueError('HTTP response is not a ZIP archive')
            result.update(status='retrieved_unverified_source',
                          retrieved_at_utc=started, zip_sha256=sha.hexdigest(),
                          zip_bytes=n)
            members = []
            with zipfile.ZipFile(target) as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    digest = hashlib.sha256()
                    count = 0
                    with z.open(info) as f:
                        first = f.readline()
                        digest.update(first)
                        count += len(first)
                        while True:
                            b = f.read(1024 * 1024)
                            if not b:
                                break
                            digest.update(b)
                            count += len(b)
                    members.append({
                        'name': info.filename, 'bytes_uncompressed': count,
                        'sha256': digest.hexdigest(), 'crc32': format(info.CRC, '08x'),
                        'first_line_utf8': first.decode('utf-8-sig', 'replace').strip()[:400]})
            result['members'] = members
            result['attempts'].append(log)
            break
        except Exception as exc:
            log['error_type'] = type(exc).__name__
            log['error'] = str(exc)[:500]
            result['attempts'].append(log)
            target.unlink(missing_ok=True)
            if attempt < attempts:
                time.sleep(2 * attempt)
    target.unlink(missing_ok=True)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    p.add_argument('--quarters', nargs='+', choices=['q3', 'q4'], default=['q3', 'q4'])
    p.add_argument('--user-agent', default=os.environ.get(
        'SEC_USER_AGENT',
        'IndependentResearch https://github.com/parthivpatel-patel/US-Equity-Microstructure-Research'))
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    summary = {
        'purpose': 'Original SEC ZIP provenance acquisition, NOT treatment authentication or row-level replication',
        'run_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'quarters': [], 'raw_data_redistributed': False}
    for q in a.quarters:
        summary['quarters'].append(fetch(q, out, a.user_agent))
    (out / 'sec_q3_q4_2025_provenance.json').write_text(
        json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'quarters': [
        {'quarter': r['quarter'], 'status': r['status'],
         'zip_sha256': r.get('zip_sha256')} for r in summary['quarters']]}, indent=2))
    return 0 if all(r['status'] == 'retrieved_unverified_source'
                    for r in summary['quarters']) else 1


if __name__ == '__main__':
    sys.exit(main())
