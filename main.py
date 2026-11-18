#!/usr/bin/env python3
"""Entry point: write the day's cover image to /output/entry.png.

The image is committed beside this file, so a run needs no network and writes
the same bytes every time.
"""
import hashlib
import shutil
from pathlib import Path

OUT = Path("/output/entry.png")
IMAGE = Path(__file__).resolve().parent / "entry.png"


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(IMAGE, OUT)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
