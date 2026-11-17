"""Additional deterministic manifest policy checks; never claims publisher authentication."""
from datetime import datetime, timedelta
from ipaddress import ip_address
from urllib.parse import urlsplit
import re

def check_manifest_policy(manifest, as_of_utc, tolerance_seconds=300):
    """Complement Phase 417 local SHA-256 gate; never proves upstream authenticity."""
    if not isinstance(as_of_utc, datetime) or as_of_utc.tzinfo is None or as_of_utc.utcoffset() != timedelta(0):
        raise ValueError('as_of_utc must be a timezone-aware UTC datetime')
    if not isinstance(tolerance_seconds, int) or isinstance(tolerance_seconds, bool) or not 0 <= tolerance_seconds <= 3600:
        raise ValueError('invalid clock tolerance')
    entries = manifest.get('sources') if isinstance(manifest, dict) else None
    if not isinstance(entries, list) or not entries:
        return {'status': 'BLOCKED', 'errors': ['sources must be nonempty'], 'source_authenticated': False}
    errors = []
    for i, entry in enumerate(entries):
        tag = f'sources[{i}]'
        if not isinstance(entry, dict):
            errors.append(f'{tag}: not an object')
            continue
        timestamp = entry.get('retrieved_utc')
        try:
            if not isinstance(timestamp, str) or not (timestamp.endswith('Z') or timestamp.endswith('+00:00')):
                raise ValueError()
            parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            if parsed.utcoffset() != timedelta(0):
                raise ValueError()
            if parsed > as_of_utc + timedelta(seconds=tolerance_seconds):
                errors.append(f'{tag}: retrieval after as-of time')
        except (ValueError, TypeError, OverflowError):
            errors.append(f'{tag}: invalid UTC retrieval timestamp')
        url = entry.get('source_url')
        try:
            if not isinstance(url, str) or re.search(r'\s', url):
                raise ValueError()
            parsed_url = urlsplit(url)
            host = parsed_url.hostname
            if parsed_url.scheme != 'https' or not host or parsed_url.username or parsed_url.password:
                raise ValueError()
            host = host.rstrip('.').lower()
            if host == 'localhost' or host.endswith('.localhost') or host.endswith('.local') or host.endswith('.internal'):
                errors.append(f'{tag}: local host prohibited')
            else:
                try:
                    ip = ip_address(host)
                    if not ip.is_global:
                        errors.append(f'{tag}: non-global IP host prohibited')
                except ValueError:
                    if '.' not in host or any(not label or len(label) > 63 or not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?', label) for label in host.split('.')):
                        errors.append(f'{tag}: invalid public hostname syntax')
        except ValueError:
            errors.append(f'{tag}: invalid HTTPS source URL')
    return {'status': 'BLOCKED' if errors else 'POLICY_PASS_NOT_AUTHENTICATED', 'errors': errors, 'source_authenticated': False}
