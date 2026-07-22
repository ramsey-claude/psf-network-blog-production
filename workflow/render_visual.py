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
    python3 workflow/render_visual.py blog/<slug>/<name>.html --max-kb 100

Output lands beside the source as <name>.png and <name>.webp.

WebP is the delivery format. Two findings drive how it is produced:

  - For flat-colour graphics like these, LOSSLESS WebP is smaller than lossy.
    Lossy spends bits on ringing artefacts around the sharp edges. On the
    first visual, lossless came to 103 KB while lossy q95 came to 284 KB.

  - Downscaling makes the file BIGGER, not smaller. Lanczos resampling
    invents thousands of intermediate colours and destroys the flat-colour
    structure lossless WebP compresses so well. Render at the target size
    and leave it alone.

So when a size budget is set, the lever is palette size, not quality and not
dimensions. The images carry roughly 1,200 distinct colours, nearly all of
them text antialiasing, so quantising to 256 is visually lossless: measured
PSNR 65.9 dB with 0.5 percent of subpixels altered.

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

try:
    from PIL import Image
except ImportError:
    Image = None

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


def to_webp(png: Path, max_kb: float | None = None):
    """Write a lossless WebP beside the PNG, shrinking the palette if needed.

    Returns (path, kb, colours) where colours is None when no quantisation
    was required.
    """
    if Image is None:
        print('Pillow not installed, skipping WebP. pip install -r requirements.txt',
              file=sys.stderr)
        return None, 0, None

    out = png.with_suffix('.webp')
    im = Image.open(png).convert('RGB')

    im.save(out, 'WEBP', lossless=True, quality=100, method=6)
    kb = out.stat().st_size / 1024
    if max_kb is None or kb <= max_kb:
        return out, kb, None

    # Step the palette down until it fits. 256 is already visually lossless
    # for this kind of graphic; anything below 64 starts to band on gradients.
    for colours in (256, 192, 128, 96, 64):
        q = im.quantize(colors=colours, method=Image.Quantize.MEDIANCUT,
                        dither=Image.Dither.NONE).convert('RGB')
        q.save(out, 'WEBP', lossless=True, quality=100, method=6)
        kb = out.stat().st_size / 1024
        if kb <= max_kb:
            return out, kb, colours

    print(f'WARNING: could not reach {max_kb} KB, smallest was {kb:.1f} KB',
          file=sys.stderr)
    return out, kb, 64


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help='Path to the visual HTML file')
    ap.add_argument('--width', type=int, default=1600, help='CSS width, default 1600')
    ap.add_argument('--height', type=int, default=3000, help='Render height before trim')
    ap.add_argument('--scale', type=int, default=2, help='Device scale factor, default 2')
    ap.add_argument('--no-trim', action='store_true')
    ap.add_argument('--max-kb', type=float, default=100,
                    help='WebP size budget in KB, default 100. Use 0 for no limit.')
    ap.add_argument('--no-webp', action='store_true')
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
        w, _h, _ch, rows = _read_png(out)
        h1 = len(rows)
        print(f'{out.name}  {w}x{h1}  {out.stat().st_size / 1024:.1f} KB')
    else:
        w, h0, h1 = trim_bottom(out, pad=args.scale * 60)
        print(f'{out.name}  {w}x{h1}  {out.stat().st_size / 1024:.1f} KB  (trimmed from {h0})')

    if not args.no_webp:
        budget = args.max_kb if args.max_kb > 0 else None
        wp, kb, colours = to_webp(out, budget)
        if wp:
            note = f'  palette {colours}' if colours else '  full colour'
            print(f'{wp.name}  {w}x{h1}  {kb:.1f} KB  lossless{note}')


if __name__ == '__main__':
    main()
