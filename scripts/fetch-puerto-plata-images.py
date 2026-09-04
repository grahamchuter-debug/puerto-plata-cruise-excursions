#!/usr/bin/env python3
"""Download hero and content images from Unsplash (Unsplash License)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"

DOWNLOADS: list[tuple[str, str]] = [
    ("hero-puerto-plata.png", "https://images.unsplash.com/photo-1551632811-561732d1e306?w=1920&q=80&fm=jpg"),
    ("damajagua-waterfalls.png", "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=1920&q=80&fm=jpg"),
    ("monkeyland.png", "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=1920&q=80&fm=jpg"),
    ("puerto-plata-city.png", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80&fm=jpg"),
    ("puerto-plata-beach.png", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80&fm=jpg"),
    ("catamaran-snorkel.png", "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1920&q=80&fm=jpg"),
    ("best-puerto-plata-excursions.png", "https://images.unsplash.com/photo-1682687220063-4742bd7fd538?w=1920&q=80&fm=jpg"),
    ("puerto-plata-port.png", "https://images.unsplash.com/photo-1548574505-5e239809ee19?w=1920&q=80&fm=jpg"),
    ("one-day-puerto-plata.png", "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1920&q=80&fm=jpg"),
    ("puerto-plata-intro.png", "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920&q=80&fm=jpg"),
    ("amber-cove-taino-bay.png", "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920&q=80&fm=jpg"),
    ("waterfall-pools.png", "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=1920&q=80&fm=jpg"),
    ("monkeys-interaction.png", "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=1920&q=80&fm=jpg"),
    ("colonial-street.png", "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1920&q=80&fm=jpg"),
    ("beach-loungers.png", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80&fm=jpg"),
    ("snorkel-caribbean.png", "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1920&q=80&fm=jpg"),
]


def download(filename: str, url: str) -> bool:
    dest = IMAGES / filename
    print(f"  {filename}")
    result = subprocess.run(
        ["curl", "-fsSL", "-o", str(dest), url],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"    FAILED: {result.stderr.strip()}", file=sys.stderr)
        return False
    size = dest.stat().st_size
    if size < 10_000:
        print(f"    WARNING: small file ({size} bytes)", file=sys.stderr)
    print(f"    OK ({size // 1024} KB)")
    return True


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    print("Downloading Puerto Plata images from Unsplash…")
    failed = 0
    for filename, url in DOWNLOADS:
        if not download(filename, url):
            failed += 1
    if failed:
        raise SystemExit(f"{failed} download(s) failed.")
    print("Done.")


if __name__ == "__main__":
    main()
