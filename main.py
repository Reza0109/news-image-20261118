#!/usr/bin/env python3
"""Copy entry.png into the make.fun output directory after validating it.

Standard library only. Expects MAKEFUN_OUTPUT_DIR to be set. The source
must be a real PNG of at most 1024x1024, and the copy is verified by
comparing byte sizes afterwards.
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND"
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
MAX_BYTES = 1048576


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_png_size(path):
    """Return (width, height) of a PNG, failing unless magic and IHDR check out."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33:
        fail(f"{path} is too short to be a PNG file")
    if header[:8] != PNG_MAGIC:
        fail(f"{path} is not a PNG file (bad magic bytes)")
    if header[12:16] != b"IHDR":
        fail(f"{path} has no IHDR chunk where one is expected")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_png_complete(path):
    """Fail unless the file ends with a proper IEND chunk."""
    with open(path, "rb") as handle:
        handle.seek(-12, os.SEEK_END)
        tail = handle.read(12)
    if len(tail) < 12 or tail[:8] != PNG_IEND:
        fail(f"{path} is truncated: no IEND chunk at the end")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")
    if not os.path.isfile(source):
        fail(f"source image not found: {source}")
    width, height = read_png_size(source)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        fail(f"image is {width}x{height}, larger than {MAX_WIDTH}x{MAX_HEIGHT}")
    if os.path.getsize(source) > MAX_BYTES:
        fail(f"image is larger than 1 MiB ({os.path.getsize(source)} bytes)")
    check_png_complete(source)
    destination = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, destination)
    src_size = os.path.getsize(source)
    dst_size = os.path.getsize(destination)
    if src_size != dst_size:
        fail(
            f"copy size mismatch: source {src_size} bytes, "
            f"destination {dst_size} bytes"
        )
    print(f"copied entry.png ({width}x{height}, {src_size} bytes) to {destination}")


if __name__ == "__main__":
    main()
