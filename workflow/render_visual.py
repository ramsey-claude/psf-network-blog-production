#!/usr/bin/env python3
"""
Render an article visual from HTML to a high-resolution PNG.

Visuals are authored as standalone HTML so they stay editable, diffable, and
brand-consistent. This script renders them with headless Chrome at 2x device
scale, then trims the trailing background so the PNG has no dead space.

Framer does not take SVG reliably in every field, and the API is unavailable,
so PNG is the delivery format. The HTML source stays in the repo next to the
article as the editable original.

Usage:
    python3 workflow/render_visual.py blog/<slug>/<name>.html
    python3 workflow/render_visual.py blog/<slug>/<name>.html --width 1600 --scale 2

Output lands beside the source as <name>.png.

Brand and accessibility constraints for any visual rendered here:
  - Background cream #F7F5F0, ink #1C1C1C
  - Vermillion #FF7141 as the single accent, blue #4F8FA3 as secondary
  - Vermillion against grey is colourblind-safe. Never encode meaning with a
    red and green pair.
  - No em dashes or en dashes in any label, per the brand rule
"""
import argparse
import struct
import subprocess
import sys
import zlib
from pathlib import Path

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


def _read_png(path: Path):
    data = path.read_bytes()
    pos, idat, w, h, ct = 8, b'', None, None, None
    while pos < len(data):
        ln = struct.unpack('>I', data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        if typ == b'IHDR':
            w, h, _bd, ct = struct.unpack('>IIBB', data[pos + 8:pos + 18])
        elif typ == b'IDAT':
            idat += data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
    raw = zlib.decompress(idat)
    ch = 4 if ct == 6 else 3
    stride = w * ch
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[i]; i += 1
        line = bytearray(raw[i:i + stride]); i += stride
        if f == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                b = prev[x]
                c = prev[x - ch] if x >= ch else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        rows.append(bytes(line))
        prev = line
    return w, h, ch, rows


def _write_png(path: Path, w: int, h: int, ch: int, rows):
    raw = b''.join(b'\x00' + r for r in rows)

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)

    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6 if ch == 4 else 2, 0, 0, 0)
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
                     + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def trim_bottom(path: Path, pad: int = 120):
    """Drop trailing rows that match the background colour."""
    w, h, ch, rows = _read_png(path)
    bg = rows[2][0:ch]
    last = h - 1
    for y in range(h - 1, -1, -1):
        row = rows[y]
        if any(row[x * ch:(x + 1) * ch] != bg for x in range(0, w, 13)):
            last = y
            break
    nh = min(h, last + 1 + pad)
    if nh < h:
        _write_png(path, w, nh, ch, rows[:nh])
    return w, h, nh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help='Path to the visual HTML file')
    ap.add_argument('--width', type=int, default=1600, help='CSS width, default 1600')
    ap.add_argument('--height', type=int, default=3000, help='Render height before trim')
    ap.add_argument('--scale', type=int, default=2, help='Device scale factor, default 2')
    ap.add_argument('--no-trim', action='store_true')
    args = ap.parse_args()

    src = Path(args.source).resolve()
    if not src.exists():
        sys.exit(f'Source not found: {src}')
    if not Path(CHROME).exists():
        sys.exit(f'Chrome not found at {CHROME}')

    out = src.with_suffix('.png')
    cmd = [
        CHROME, '--headless', '--disable-gpu', '--hide-scrollbars',
        f'--screenshot={out}',
        f'--window-size={args.width},{args.height}',
        f'--force-device-scale-factor={args.scale}',
        '--virtual-time-budget=3000',
        f'file://{src}',
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not out.exists():
        sys.exit(f'Render failed:\n{r.stderr[-800:]}')

    if args.no_trim:
        w, h, _, _ = _read_png(out)
        print(f'{out.name}  {w}x{h}')
    else:
        w, h0, h1 = trim_bottom(out, pad=args.scale * 60)
        print(f'{out.name}  {w}x{h1}  (trimmed from {h0})')


if __name__ == '__main__':
    main()
