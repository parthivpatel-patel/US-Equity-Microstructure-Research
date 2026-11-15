"""Read-only bounded ZIP byte/CRC verification; not source authentication."""
import argparse, hashlib, json, stat, zipfile
from pathlib import Path

def verify(path, max_members=10000, max_total_bytes=1000000000,
           max_member_bytes=200000000, max_ratio=1000, chunk_size=1048576):
    if min(max_members, max_total_bytes, max_member_bytes, max_ratio, chunk_size) <= 0:
        raise ValueError("limits must be positive")
    results, seen, budget, consumed = [], set(), 0, 0
    with zipfile.ZipFile(Path(path)) as z:
        infos = z.infolist()
        if len(infos) > max_members:
            return dict(status="rejected", reason="member_count_limit", members=[])
        for info in infos:
            name = info.filename
            parts = name.split("/")
            mode = info.external_attr >> 16
            if (not name or name.startswith("/") or "\\" in name or "\x00" in name
                or any(p in ("", ".", "..") for p in parts[:-1])
                or parts[-1] in (".", "..") or ":" in parts[0]
                or name in seen or stat.S_ISLNK(mode) or info.flag_bits & 1):
                return dict(status="rejected", reason="unsafe_member", members=[])
            seen.add(name)
            if info.is_dir():
                continue
            budget += info.file_size
            if (info.file_size > max_member_bytes or budget > max_total_bytes
                or (info.file_size and (not info.compress_size
                    or info.file_size / info.compress_size > max_ratio))):
                return dict(status="rejected", reason="declared_size_or_ratio_limit", members=[])
        for info in infos:
            if info.is_dir():
                continue
            digest, size = hashlib.sha256(), 0
            try:
                with z.open(info, "r") as stream:
                    while True:
                        chunk = stream.read(min(chunk_size, max_member_bytes-size+1,
                                                max_total_bytes-consumed+1))
                        if not chunk:
                            break
                        size += len(chunk)
                        consumed += len(chunk)
                        if (size > max_member_bytes or consumed > max_total_bytes
                            or size > info.file_size):
                            return dict(status="rejected", reason="actual_size_limit", members=[])
                        digest.update(chunk)
            except (zipfile.BadZipFile, RuntimeError, EOFError, OSError) as exc:
                return dict(status="rejected", reason="member_read_or_crc_error",
                            members=[], error_type=type(exc).__name__)
            if size != info.file_size:
                return dict(status="rejected", reason="declared_actual_size_mismatch", members=[])
            results.append(dict(name=info.filename, bytes_verified=size,
                                sha256=digest.hexdigest(), crc_checked_by_zipfile=True))
    return dict(status="verified_bytes_only", members=results, bytes_verified=consumed,
                source_authenticated=False, redistribution_authorized=False,
                safe_to_extract=False)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("archive")
    p.add_argument("--max-total-bytes", type=int, default=1000000000)
    p.add_argument("--max-member-bytes", type=int, default=200000000)
    a = p.parse_args()
    print(json.dumps(verify(a.archive, max_total_bytes=a.max_total_bytes,
                            max_member_bytes=a.max_member_bytes), indent=2))
