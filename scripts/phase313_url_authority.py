"""Supplemental fail-closed URL authority syntax gate; not source authentication."""
import json
import ipaddress
from pathlib import Path
from urllib.parse import urlsplit
from scripts.phase312_provenance_metadata import verify_manifest_strict


def verify_authorities(manifest_path, root):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or not isinstance(manifest.get('sources'), list) or not manifest['sources']:
        raise ValueError('nonempty sources required')
    for entry in manifest['sources']:
        if not isinstance(entry, dict) or not isinstance(entry.get('source_url'), str):
            raise ValueError('invalid source URL')
        url = entry['source_url']
        if '\\' in url or any(ord(c) < 33 or ord(c) == 127 for c in url):
            raise ValueError('unsafe URL characters')
        try:
            p = urlsplit(url)
            host = p.hostname
            port = p.port  # validates malformed and out-of-range ports
        except ValueError as exc:
            raise ValueError('invalid URL authority') from exc
        if p.scheme != 'https' or not host or p.username is not None or p.password is not None or p.fragment:
            raise ValueError('invalid URL authority')
        if port is not None and port != 443:
            raise ValueError('nonstandard HTTPS port')
        if host.endswith('.') or host.startswith('.') or '..' in host:
            raise ValueError('invalid host labels')
        try:
            ipaddress.ip_address(host)
        except ValueError:
            labels = host.split('.')
            if len(labels) < 2 or any(not label or len(label) > 63 or label[0] == '-' or label[-1] == '-' or not all(ch.isascii() and (ch.isalnum() or ch == '-') for ch in label) for label in labels):
                raise ValueError('invalid host labels')
        else:
            raise ValueError('IP literal not accepted as source host')
    return verify_manifest_strict(manifest_path, root)
