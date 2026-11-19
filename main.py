#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261118.

Copies the pre-rendered entry.png (shipped in this repo) to the output
directory, then verifies the copy landed intact: the source must be a
real PNG of at most 1024x1024 pixels, and the destination must exist,
start with the PNG magic bytes, and match the source's byte size exactly.
Standard library only: no network, no randomness, no clock, so repeated
runs produce byte-identical output.
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    """Read (width, height) from a PNG's IHDR chunk; None if not a PNG."""
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != PNG_MAGIC:
        return None
    if header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing from the repository: %s" % src)
    dims = png_dimensions(src)
    if dims is None:
        raise SystemExit("entry.png is not a valid PNG: %s" % src)
    if dims[0] > 1024 or dims[1] > 1024:
        raise SystemExit(
            "entry.png too large: %dx%d, max 1024x1024" % dims)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    expected = os.path.getsize(src)
    if not os.path.isfile(dst):
        raise SystemExit("output entry.png was not created: %s" % dst)
    with open(dst, "rb") as f:
        if f.read(8) != PNG_MAGIC:
            raise SystemExit("output entry.png is not a valid PNG: %s" % dst)
    actual = os.path.getsize(dst)
    if actual != expected:
        raise SystemExit(
            "output entry.png size mismatch: expected %d bytes, got %d"
            % (expected, actual)
        )


if __name__ == "__main__":
    main()
