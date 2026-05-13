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
from pathlib import Path

import yaml


FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)$', re.DOTALL)
VISUAL_PLACEHOLDER_RE = re.compile(r'\[VISUAL-HERO-(\d+)\]')
LIST_LINE_RE = re.compile(r'^\s*([\-\*]|\d+\.)\s+')


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
            '-f', 'gfm',
            '-t', 'docx',
            '-o', str(out_path),
        ], check=True)
    finally:
        Path(tmp_md_path).unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path, help='Path to draft.md')
    ap.add_argument('--output', '-o', type=Path, required=True, help='Path to output .docx')
    args = ap.parse_args()
    render(args.input, args.output)
    print(f'Wrote {args.output}', file=sys.stderr)


if __name__ == '__main__':
    main()
