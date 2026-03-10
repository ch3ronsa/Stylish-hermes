"""
C2: Image Cache Cleanup
Removes generated images older than N days from ~/.hermes/image_cache/
to prevent disk bloat.

Run from WSL:
    python3 scripts/cleanup-image-cache.py          # default: 7 days
    python3 scripts/cleanup-image-cache.py --days 3  # custom age
    python3 scripts/cleanup-image-cache.py --dry-run  # preview only
"""
from __future__ import annotations

import argparse
import os
import time
from pathlib import Path


CACHE_DIR = Path.home() / ".hermes" / "image_cache"


def get_size_str(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean up old generated images")
    parser.add_argument("--days", type=int, default=7, help="Delete images older than N days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Preview deletions without actually deleting")
    args = parser.parse_args()

    if not CACHE_DIR.exists():
        print(f"Cache directory does not exist: {CACHE_DIR}")
        print("Nothing to clean up.")
        return

    cutoff = time.time() - (args.days * 86400)
    total_files = 0
    deleted_files = 0
    freed_bytes = 0
    kept_bytes = 0

    image_exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    for f in CACHE_DIR.iterdir():
        if not f.is_file():
            continue
        if f.suffix.lower() not in image_exts:
            continue

        total_files += 1
        file_size = f.stat().st_size
        file_age = f.stat().st_mtime

        if file_age < cutoff:
            deleted_files += 1
            freed_bytes += file_size
            if args.dry_run:
                age_days = (time.time() - file_age) / 86400
                print(f"  [would delete] {f.name} ({get_size_str(file_size)}, {age_days:.0f} days old)")
            else:
                f.unlink()
        else:
            kept_bytes += file_size

    print(f"\nImage Cache Cleanup {'(DRY RUN)' if args.dry_run else ''}")
    print(f"  Directory: {CACHE_DIR}")
    print(f"  Threshold: {args.days} days")
    print(f"  Total images: {total_files}")
    print(f"  {'Would delete' if args.dry_run else 'Deleted'}: {deleted_files} ({get_size_str(freed_bytes)})")
    print(f"  Kept: {total_files - deleted_files} ({get_size_str(kept_bytes)})")


if __name__ == "__main__":
    main()
