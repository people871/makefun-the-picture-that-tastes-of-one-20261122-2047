#!/usr/bin/env python3
"""Write the honey hero image to /output/entry.png.

Reads the bundled ``entry.png`` sitting next to this file, checks that it is
a whole PNG or JPEG within the competition caps (at most 1 MiB and at most
1024 by 1024 pixels), copies the exact bytes to
``$MAKEFUN_OUTPUT_DIR/entry.png`` (default ``/output``), then reads the copy
back and refuses to exit cleanly unless its length and sha256 match the
source byte for byte. Standard library only; no network.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8"


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_source():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, SOURCE_NAME)
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (path, exc))
    if not data:
        fail("source image is empty")
    if len(data) > MAX_BYTES:
        fail("source image is %d bytes, over the %d byte cap"
             % (len(data), MAX_BYTES))
    return data


def png_dimensions(data):
    if len(data) < 33 or data[:8] != PNG_MAGIC:
        return None
    if data[12:16] != b"IHDR":
        fail("PNG is missing its IHDR chunk")
    if not data.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
        fail("PNG is truncated: no IEND chunk at the end")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def jpeg_dimensions(data):
    if len(data) < 4 or data[:2] != JPEG_MAGIC:
        return None
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            fail("JPEG marker expected at offset %d" % pos)
        marker = data[pos + 1]
        if marker == 0xD8 or marker == 0x01 or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if marker == 0xDA:
            fail("JPEG scan starts before any frame header")
        if pos + 4 > len(data):
            fail("JPEG segment header is truncated")
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if length < 2 or pos + 2 + length > len(data):
            fail("JPEG segment overruns the file")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            body = data[pos + 4:pos + 2 + length]
            if len(body) < 6:
                fail("JPEG frame header is too short")
            if not data.rstrip(b"\x00").endswith(b"\xff\xd9"):
                fail("JPEG is truncated: no EOI marker at the end")
            height, width = struct.unpack(">HH", body[1:5])
            return width, height
        pos += 2 + length
    fail("JPEG has no frame header")


def measure(data):
    dims = png_dimensions(data)
    kind = "PNG"
    if dims is None:
        dims = jpeg_dimensions(data)
        kind = "JPEG"
    if dims is None:
        fail("source is neither a PNG nor a JPEG")
    width, height = dims
    if width <= 0 or height <= 0:
        fail("%s has non-positive dimensions %dx%d" % (kind, width, height))
    if width > MAX_SIDE or height > MAX_SIDE:
        fail("%s is %dx%d, over the %dx%d cap"
             % (kind, width, height, MAX_SIDE, MAX_SIDE))
    return kind, width, height


def write_output(data):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)
    try:
        with open(target, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("cannot write %s: %s" % (target, exc))
    return target


def verify_copy(target, data):
    try:
        with open(target, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        fail("cannot read back %s: %s" % (target, exc))
    if len(written) != len(data):
        fail("output length %d does not match source %d"
             % (len(written), len(data)))
    source_hash = hashlib.sha256(data).hexdigest()
    written_hash = hashlib.sha256(written).hexdigest()
    if written_hash != source_hash:
        fail("output sha256 %s does not match source %s"
             % (written_hash, source_hash))
    return written_hash


def main():
    data = read_source()
    kind, width, height = measure(data)
    target = write_output(data)
    digest = verify_copy(target, data)
    print("wrote %s (%s %dx%d, %d bytes, sha256 %s)"
          % (target, kind, width, height, len(data), digest))


if __name__ == "__main__":
    main()
