#!/usr/bin/env python3
"""
Render a draft.md (markdown + YAML frontmatter) into a .docx file suitable
for upload to Google Drive. Drive converts .docx -> Google Doc automatically,
preserving headings, bold/italic, lists, tables, hyperlinks, blockquotes.

Implementation: prepares a single markdown document (Production Notes table
plus the post body) and pipes it through pandoc for clean GitHub-flavored
markdown to docx conversion. Pandoc produces a much smaller and cleaner
docx than python-docx with hand-built styling, and the resulting Drive
import is properly typeset.

Why docx (and not HTML or plain text):
- The Drive create_file MCP auto-conversion list only includes text/plain
  and text/csv. HTML uploads stay as HTML files. Plain text uploads strip
  markdown formatting.
- Docx is universally converted by Drive into Google Doc with full
  heading/list/table/link preservation.

Usage:
    .venv/bin/python3 workflow/render-for-drive.py blog/<slug>/draft.md \\
        --output blog/<slug>/<slug>.docx

Dependencies:
    pip: pyyaml
    system: pandoc (brew install pandoc)
"""
import sys
import re
import argparse
import subprocess
import tempfile
import zipfile
from pathlib import Path

import yaml


FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)$', re.DOTALL)
VISUAL_PLACEHOLDER_RE = re.compile(r'\[VISUAL-HERO-(\d+)\]')
LIST_LINE_RE = re.compile(r'^\s*([\-\*]|\d+\.)\s+')

# Client-facing Drive doc style spec (measured from the delivered GO-LIVE docs
# on 2026-08-14; Google Docs renders "Aptos Display" as Play). Every render
# must produce this exact look regardless of the local pandoc version's
# reference defaults, so the fonts are pinned after pandoc runs.
DRIVE_BODY_FONT = 'Aptos'
DRIVE_HEADING_FONT = 'Aptos Display'
DRIVE_HEADING_COLOR = '0F4761'
DRIVE_LINK_COLOR = '156082'
DRIVE_HEADING_SIZES = {'Heading1': 40, 'Heading2': 32, 'Heading3': 28, 'Heading4': 24}  # half-points
DRIVE_BODY_SIZE = 24  # half-points = 12pt


def split_frontmatter(raw: str):
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return {}, raw
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def normalize_blank_lines_before_lists(text: str) -> str:
    lines = text.split('\n')
    out = []
    for i, line in enumerate(lines):
        is_list = bool(LIST_LINE_RE.match(line))
        prev = lines[i - 1] if i > 0 else ''
        prev_is_list = bool(LIST_LINE_RE.match(prev))
        prev_is_blank = prev.strip() == ''
        if is_list and i > 0 and not prev_is_list and not prev_is_blank:
            out.append('')
        out.append(line)
    return '\n'.join(out)


def replace_visual_placeholders(text: str) -> str:
    def repl(m):
        n = m.group(1)
        return (
            f'\n> **Designer note:** Hero visual [VISUAL-HERO-{n}] '
            f'goes here (1200x630). See hero_visual_alt in Production Notes '
            f'for alt text.\n'
        )
    return VISUAL_PLACEHOLDER_RE.sub(repl, text)


def production_notes_md(fm: dict) -> str:
    rows = [
        ('Title tag (SEO)', fm.get('title', '')),
        ('Slug', fm.get('slug', '')),
        ('Type', fm.get('type', '')),
        ('Topic', fm.get('topic', '')),
        ('Focus keyword', fm.get('focus_keyword', '')),
        ('Secondary keywords', ', '.join(fm.get('secondary_keywords', []) or [])),
        ('Meta description', fm.get('meta_description', '')),
        ('Canonical URL', fm.get('canonical', '')),
        ('Hero visual alt text', fm.get('hero_visual_alt', '')),
        ('Author', fm.get('author', '')),
        ('Reviewer', fm.get('reviewer', '')),
        ('Read time', fm.get('read_time', '')),
        ('Published', str(fm.get('published', ''))),
        ('Updated', str(fm.get('updated', ''))),
    ]
    rows = [(k, str(v)) for k, v in rows if v]
    if not rows:
        # Notes-style drafts (Batch 2+) carry their Production Notes in the
        # body; an empty frontmatter table would render as a stub artifact.
        return ''
    lines = [
        '**Production Notes** (SEO metadata, not part of the published body)',
        '',
        '| Field | Value |',
        '|-------|-------|',
    ]
    for k, v in rows:
        # Escape pipes inside cell content
        v_safe = v.replace('|', r'\|')
        lines.append(f'| {k} | {v_safe} |')
    lines += ['', '---', '']
    return '\n'.join(lines)


def _patch_style_block(styles: str, style_id: str, size_halfpt: int) -> str:
    """Pin one heading style to the Drive spec: not bold, sized, colored."""
    m = re.search(
        r'(<w:style [^>]*w:styleId="' + style_id + r'".*?</w:style>)',
        styles, re.DOTALL)
    if not m:
        return styles
    block = m.group(1)
    block = re.sub(r'<w:bC?s?\s*/>', '', block)
    block = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{size_halfpt}" />', block)
    block = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{size_halfpt}" />', block)
    block = re.sub(r'<w:color [^/]*/>', '', block)
    block = block.replace('<w:rPr>', f'<w:rPr><w:color w:val="{DRIVE_HEADING_COLOR}" />', 1)
    return styles[:m.start(1)] + block + styles[m.end(1):]


def normalize_docx_styles(docx_path: Path):
    """Rewrite theme + styles inside the pandoc docx so the Drive-converted
    Google Doc matches the delivered GO-LIVE look byte-for-byte in fonts,
    sizes, and colors, independent of the local pandoc version."""
    zin = zipfile.ZipFile(docx_path)
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()

    theme = items['word/theme/theme1.xml'].decode('utf-8')
    theme = re.sub(
        r'(<a:majorFont>\s*<a:latin typeface=")[^"]*(")',
        r'\g<1>' + DRIVE_HEADING_FONT + r'\g<2>', theme)
    theme = re.sub(
        r'(<a:minorFont>\s*<a:latin typeface=")[^"]*(")',
        r'\g<1>' + DRIVE_BODY_FONT + r'\g<2>', theme)
    items['word/theme/theme1.xml'] = theme.encode('utf-8')

    styles = items['word/styles.xml'].decode('utf-8')
    for style_id, size in DRIVE_HEADING_SIZES.items():
        styles = _patch_style_block(styles, style_id, size)
    m = re.search(r'(<w:style [^>]*w:styleId="Hyperlink".*?</w:style>)', styles, re.DOTALL)
    if m:
        block = re.sub(r'<w:color [^/]*/>',
                       f'<w:color w:val="{DRIVE_LINK_COLOR}" />', m.group(1))
        styles = styles[:m.start(1)] + block + styles[m.end(1):]
    dd = re.search(r'(<w:docDefaults>.*?</w:docDefaults>)', styles, re.DOTALL)
    if dd:
        block = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{DRIVE_BODY_SIZE}" />', dd.group(1))
        block = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{DRIVE_BODY_SIZE}" />', block)
        styles = styles[:dd.start(1)] + block + styles[dd.end(1):]
    items['word/styles.xml'] = styles.encode('utf-8')

    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in items.items():
            zout.writestr(name, data)


def render(draft_path: Path, out_path: Path):
    raw = draft_path.read_text(encoding='utf-8')
    fm, body = split_frontmatter(raw)

    body = replace_visual_placeholders(body)
    body = normalize_blank_lines_before_lists(body)

    combined = production_notes_md(fm) + body

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tf:
        tf.write(combined)
        tmp_md_path = tf.name

    try:
        subprocess.run([
            'pandoc',
            tmp_md_path,
            # tex_math_dollars must be OFF: a line with two dollar amounts
            # ("**$200,000** in income, or **$1 million**") otherwise parses
            # as inline TeX math, and Drive's docx import silently drops the
            # oMath block. This was the root cause of the recurring stat-card
            # text loss in delivered docs (found 2026-08-14).
            '-f', 'gfm-tex_math_dollars',
            '-t', 'docx',
            '-o', str(out_path),
        ], check=True)
    finally:
        Path(tmp_md_path).unlink(missing_ok=True)

    normalize_docx_styles(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path, help='Path to draft.md')
    ap.add_argument('--output', '-o', type=Path, required=True, help='Path to output .docx')
    args = ap.parse_args()
    render(args.input, args.output)
    print(f'Wrote {args.output}', file=sys.stderr)


if __name__ == '__main__':
    main()
