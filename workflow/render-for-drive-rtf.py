#!/usr/bin/env python3
"""
Render a draft.md into RTF for upload to Google Drive via the Drive MCP
(create_file with contentMimeType application/rtf + textContent). Drive
converts RTF to a native Google Doc.

Why RTF (cloud sessions): the MCP's base64 docx path is impractical for a
model-mediated transfer (a single corrupted character breaks the zip), while
RTF is plain text, converts cleanly, and Drive's importer applies the same
font substitutions the delivered GO-LIVE docs got from the docx path:
"Aptos Display" imports as Play (headings) and "Aptos" falls back to the
default body font, which is exactly how the older docs render on screen.

Style spec (measured from delivered GO-LIVE docs, 2026-08-14):
  body    Aptos 12pt black; headings Aptos Display, not bold, #0F4761,
  H1 20pt / H2 16pt / H3 14pt; links #156082, not underlined.

Supported markdown subset (what the drafts use): #/##/### headings,
paragraphs, **bold**, [text](url) links, "-" bullet lists, "1." numbered
lists, pipe tables, [VISUAL-HERO-XX] placeholders, --- rules (skipped).
"""
import re
import sys
import argparse
from pathlib import Path

FS_BODY = 24        # half-points: 12pt
FS_H = {1: 40, 2: 32, 3: 28}
CF_HEADING = 1      # colortbl index for #0F4761
CF_LINK = 2         # colortbl index for #156082
CF_BODY = 3         # black

HEADER = (
    r'{\rtf1\ansi\deff0' '\n'
    r'{\fonttbl{\f0\fnil\fcharset0 Aptos;}{\f1\fnil\fcharset0 Aptos Display;}}' '\n'
    r'{\colortbl;\red15\green71\blue97;\red21\green96\blue130;\red0\green0\blue0;}' '\n'
)
FOOTER = '}\n'

BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
VISUAL_RE = re.compile(r'\[VISUAL-HERO-(\d+)\]')


def esc(text: str) -> str:
    out = []
    for ch in text:
        if ch in '\\{}':
            out.append('\\' + ch)
        elif ord(ch) > 127:
            out.append(r'\uc0\u%d ' % ord(ch))
        else:
            out.append(ch)
    return ''.join(out)


def inline(text: str) -> str:
    """Markdown inline (bold, links) -> RTF, escaping everything else."""
    parts = []
    pos = 0
    tokens = []
    for m in BOLD_RE.finditer(text):
        tokens.append((m.start(), m.end(), 'b', m.group(1)))
    for m in LINK_RE.finditer(text):
        tokens.append((m.start(), m.end(), 'a', m))
    tokens.sort()
    prev_end = 0
    for start, end, kind, payload in tokens:
        if start < prev_end:
            continue  # overlapping (link inside bold handled by outer token)
        parts.append(esc(text[prev_end:start]))
        if kind == 'b':
            parts.append(r'{\b ' + inline(payload) + '}')
        else:
            label, url = payload.group(1), payload.group(2)
            parts.append(
                r'{\field{\*\fldinst{HYPERLINK "' + esc(url) + '"}}'
                r'{\fldrslt{\cf%d ' % CF_LINK + inline(label) + '}}}')
        prev_end = end
    parts.append(esc(text[prev_end:]))
    return ''.join(parts)


def para(text: str, extra='') -> str:
    return (r'\pard\sa160%s\f0\fs%d\cf%d ' % (extra, FS_BODY, CF_BODY)
            + inline(text) + r'\par' + '\n')


def heading(level: int, text: str) -> str:
    fs = FS_H.get(level, FS_H[3])
    return (r'\pard\sb240\sa120\keepn\f1\fs%d\cf%d ' % (fs, CF_HEADING)
            + inline(text) + r'\par' + '\n')


def list_item(text: str, marker: str) -> str:
    return (r'\pard\fi-260\li560\sa80\f0\fs%d\cf%d %s\tab ' % (FS_BODY, CF_BODY, marker)
            + inline(text) + r'\par' + '\n')


def table(rows) -> str:
    ncols = max(len(r) for r in rows)
    width = 9360 // ncols
    out = []
    for r in rows:
        cells = list(r) + [''] * (ncols - len(r))
        row = [r'\trowd\trgaph80']
        for i in range(ncols):
            row.append(
                r'\clbrdrt\brdrs\brdrw10\clbrdrl\brdrs\brdrw10'
                r'\clbrdrb\brdrs\brdrw10\clbrdrr\brdrs\brdrw10'
                r'\cellx%d' % ((i + 1) * width))
        for c in cells:
            row.append(r'\intbl\f0\fs%d\cf%d ' % (FS_BODY, CF_BODY) + inline(c) + r'\cell')
        row.append(r'\row' + '\n')
        out.append(''.join(row))
    out.append(r'\pard\sa160\par' + '\n')
    return ''.join(out)


def convert(md: str) -> str:
    md = VISUAL_RE.sub(
        lambda m: '*Designer note: hero visual [VISUAL-HERO-%s] goes here '
                  '(1200x630); see hero alt in Production Notes.*' % m.group(1), md)
    lines = md.split('\n')
    out = [HEADER]
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip() or line.strip() == '---':
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append(table(rows))
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            out.append(heading(len(m.group(1)), m.group(2)))
            i += 1
            continue
        m = re.match(r'^[-*]\s+(.*)$', line)
        if m:
            out.append(list_item(m.group(1), r'\bullet'))
            i += 1
            continue
        m = re.match(r'^(\d+)\.\s+(.*)$', line)
        if m:
            out.append(list_item(m.group(2), esc(m.group(1) + '.')))
            i += 1
            continue
        if line.startswith('> '):
            out.append(para(line[2:], extra=r'\li400'))
            i += 1
            continue
        # paragraph: join soft-wrapped lines until blank
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|[-*]\s|\d+\.\s|\||>)', lines[i]):
            buf.append(lines[i].rstrip())
            i += 1
        out.append(para(' '.join(buf)))
    out.append(FOOTER)
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)
    ap.add_argument('--output', '-o', type=Path, required=True)
    args = ap.parse_args()
    md = args.input.read_text(encoding='utf-8')
    args.output.write_text(convert(md), encoding='utf-8')
    print(f'Wrote {args.output}', file=sys.stderr)


if __name__ == '__main__':
    main()
