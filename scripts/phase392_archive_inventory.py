"""Read-only ZIP inventory; metadata checks do not establish source authenticity."""
import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath


def inspect_archive(path, max_members=100000, max_uncompressed=10_000_000_000, max_ratio=1000):
    path = Path(path)
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(chunk)
    issues = []
    members = []
    total = 0
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        if len(infos) > max_members:
            issues.append('member_limit_exceeded')
        seen = set()
        for info in infos:
            name = info.filename
            p = PurePosixPath(name)
            mode = info.external_attr >> 16
            if not name or p.is_absolute() or '\\' in name or any(part in ('.', '..') for part in p.parts) or ':' in p.parts[0]:
                issues.append('unsafe_path:' + name)
            if name in seen:
                issues.append('duplicate_member:' + name)
            seen.add(name)
            if stat.S_ISLNK(mode):
                issues.append('symlink:' + name)
            if info.flag_bits & 1:
                issues.append('encrypted:' + name)
            total += info.file_size
            if info.file_size > 0 and (info.compress_size == 0 or info.file_size / info.compress_size > max_ratio):
                issues.append('compression_ratio:' + name)
            members.append({'name': name, 'bytes': info.file_size, 'compressed_bytes': info.compress_size, 'crc32': f'{info.CRC:08x}'})
        if total > max_uncompressed:
            issues.append('uncompressed_limit_exceeded')
    return {'archive': path.name, 'archive_sha256': digest.hexdigest(), 'archive_bytes': path.stat().st_size,
            'member_count': len(members), 'total_declared_uncompressed_bytes': total,
            'issues': sorted(set(issues)), 'members': members,
            'contents_authenticated': False, 'redistribution_authorized': False,
            'safe_to_extract': False}


def inventory(paths):
    return [inspect_archive(p) for p in sorted(paths, key=lambda x: str(x))]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read-only ZIP inventory; does not extract files')
    parser.add_argument('archives', nargs='+')
    args = parser.parse_args()
    print(json.dumps(inventory(args.archives), indent=2))
