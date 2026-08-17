#!/usr/bin/env python3
"""
Build one Framer CMS import CSV for a whole batch.

The psf-editorial-agent skill ships scripts/framer_export.py, which does this
for a single article from a hand-written JSON file. Batch 2 is fifteen
articles that already exist as drafts, so this reads the drafts directly and
emits one CSV with one row per article. Same columns, same slug-matching
contract, same hard-won rules, restated here because getting any of them
wrong is expensive:

  - The body goes into the EXISTING rich-text field named "Content", the one
    the site template renders. An import that creates a "Body" field looks
    like it worked and shows nothing on the page.
  - Framer identifies items by Slug. A slug that matches an existing item
    updates it in place; a slug that does not match creates a NEW item. That
    is what we want for Batch 2, since all fifteen slugs currently 404, but
    it also means a typo in a slug silently produces a duplicate rather than
    an error.
  - Author, Hero Image, Blog Categories and FAQ S are reference or asset
    fields. They are deliberately NOT columns here. Importing them as plain
    text either fails or, worse, blanks the reference on an existing item.
    They are set in the CMS after the import.

What is stripped from Content, and why:

  - The H1. Framer renders the Title field as the page heading, so leaving
    the markdown H1 in the body ships two competing H1s and costs the page
    its heading structure.
  - The [VISUAL-HERO-XX] placeholder. It is an instruction to a designer,
    not copy, and it would render as a literal paragraph of bracket text.
  - The Production Notes block, which is not part of the published body.

What is kept: everything else, Sources included. The dek is kept in Content
AND copied into Excerpt, because Excerpt feeds listing cards while Content
feeds the page; dropping it from Content would lose the standfirst.

Usage:
    python3 workflow/framer_batch_csv.py --batch2 -o ~/Desktop/batch2-framer.csv
    python3 workflow/framer_batch_csv.py --slug reit-dividend-taxation
    python3 workflow/framer_batch_csv.py --batch2 --check   # report, write nothing
"""
import argparse
import csv
import importlib.util
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOG = REPO / 'blog'

_spec = importlib.util.spec_from_file_location(
    'make_paste_kit', Path(__file__).resolve().parent / 'make_paste_kit.py')
_mpk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mpk)

BATCH2 = [
    'debt-vs-equity-fractional',
    'fractional-real-estate-ira',
    'fractional-real-estate-vs-other-investments',
    'how-to-choose-fractional-real-estate-platform',
    'how-to-read-reg-a-offering-circular',
    'legal-tax-guide-fractional-real-estate',
    'proptech-future-of-real-estate',
    'proptech-trends-2026',
    'real-estate-as-an-asset-class',
    'real-estate-etfs-vs-fractional',
    'real-estate-vs-index-funds-retirement',
    'reit-dividend-taxation',
    'single-family-vs-multifamily-fractional',
    'tokenized-vs-traditional-fractional',
    'how-to-sell-fractional-real-estate',
]

# Column set is copied from the skill's framer_export.py rather than widened.
# That script's author left out every reference and asset field on purpose.
FIELDS = ['Title', 'Slug', 'Date', 'Excerpt', 'Meta Description', 'Keywords', 'Content']

HERO_PLACEHOLDER = re.compile(r'^\s*\[VISUAL-[A-Z0-9-]+\]\s*$', re.MULTILINE)
H1 = re.compile(r'^#\s+.*$', re.MULTILINE)


def split_dek(body_md: str):
    """Return (dek_text, body_without_h1_or_placeholder).

    The dek is the first non-empty paragraph after the H1. Batch 2 writes it
    as a plain paragraph; Batch 3 labels it "**Dek:** ...". Handle both, and
    stop at the first heading so an article with no dek does not swallow its
    first section.
    """
    lines = body_md.split('\n')
    h1_at = next((i for i, l in enumerate(lines) if re.match(r'^#\s+', l)), None)
    dek = ''
    if h1_at is not None:
        for l in lines[h1_at + 1:]:
            s = l.strip()
            if not s:
                continue
            if s.startswith('#') or s.startswith('['):
                break
            dek = s
            break
    dek = re.sub(r'^\*\*Dek:?\*\*\s*', '', dek)
    # Strip inline markdown so the Excerpt is plain text, which is what a
    # listing card wants. Links become their anchor text.
    dek = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', dek)
    dek = re.sub(r'\*\*([^*]+)\*\*', r'\1', dek)
    dek = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'\1', dek)

    stripped = H1.sub('', body_md, count=1)
    stripped = HERO_PLACEHOLDER.sub('', stripped)
    return dek.strip(), stripped


def row_for(slug: str):
    """Return (row_dict, problems)."""
    src = BLOG / slug / 'draft-v2-humanized.md'
    if not src.exists():
        src = BLOG / slug / 'draft.md'
    if not src.exists():
        return None, [f'no draft in blog/{slug}/']

    md = src.read_text(encoding='utf-8')
    notes_raw, body_md = _mpk.split_notes(md)
    notes = _mpk.parse_notes(notes_raw)

    dek, body_md = split_dek(body_md)
    content = _mpk.md_to_html(body_md)

    declared = notes.get('slug', '').strip().strip('/')
    problems = []
    # A slug mismatch here does not raise in Framer, it silently creates a
    # duplicate item. Refuse to emit the row instead.
    if not declared:
        problems.append('no Slug in the draft metadata')
    elif declared != slug:
        problems.append(f'declared slug "{declared}" != folder "{slug}"')
    if not notes.get('title'):
        problems.append('no Title')
    if not content.strip():
        problems.append('empty Content after rendering')
    if '<h1' in content:
        problems.append('an H1 survived into Content')
    if '[VISUAL' in content:
        problems.append('a visual placeholder survived into Content')

    # make_paste_kit.parse_notes has no alias for the secondary-keyword field,
    # so reading it through notes silently yields nothing and Keywords ships
    # with the focus keyword alone. Pull it out of the raw block instead.
    # Two shapes: a Production Notes bullet with a comma list, and Batch 3's
    # YAML list of "  - keyword" lines.
    kw = [notes.get('focus_keyword', '').strip()]
    m = re.search(r'Secondary keywords?:?\**\s*([^\n]+)', notes_raw, re.IGNORECASE)
    if m:
        kw += [k.strip() for k in m.group(1).split(',')]
    else:
        m = re.search(r'^secondary_keywords:\s*\n((?:\s*-\s*[^\n]+\n?)+)',
                      notes_raw, re.IGNORECASE | re.MULTILINE)
        if m:
            kw += [re.sub(r'^\s*-\s*', '', l).strip()
                   for l in m.group(1).strip().split('\n')]
    seen, keywords = set(), []
    for k in kw:
        k = k.strip().strip('"')
        if k and k.lower() not in seen:
            seen.add(k.lower())
            keywords.append(k)
    keywords = ', '.join(keywords)

    date = ''
    m = re.search(r'Published(?:/Updated)?:?\**\s*(\d{4}-\d{2}-\d{2})', notes_raw)
    if m:
        date = m.group(1)

    row = {
        'Title': notes.get('title', ''),
        'Slug': slug,
        'Date': date,
        'Excerpt': dek,
        'Meta Description': notes.get('meta_description', ''),
        'Keywords': keywords,
        'Content': content,
    }
    return row, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', action='append', default=[])
    ap.add_argument('--batch2', action='store_true')
    ap.add_argument('-o', '--out', default='framer-import.csv')
    ap.add_argument('--check', action='store_true',
                    help='report and write nothing')
    args = ap.parse_args()

    slugs = args.slug or (BATCH2 if args.batch2 else [])
    if not slugs:
        print('nothing to do: pass --batch2 or --slug', file=sys.stderr)
        return 2

    rows, blocked = [], []
    for s in slugs:
        row, problems = row_for(s)
        if problems:
            blocked.append((s, problems))
            continue
        rows.append(row)
        internal = row['Content'].count('href="https://www.psfnetwork.com/blog/')
        relative = row['Content'].count('href="/blog/')
        print(f'  ok  {s}')
        print(f'      title {len(row["Title"])}  meta {len(row["Meta Description"])}  '
              f'content {len(row["Content"])} chars  '
              f'internal links {internal} absolute / {relative} relative')

    for s, problems in blocked:
        print(f'  SKIP {s}: {"; ".join(problems)}', file=sys.stderr)

    if not rows:
        print('\nno rows produced', file=sys.stderr)
        return 1

    print(f'\n{len(rows)} row(s) ready, {len(blocked)} skipped')
    print('Not in this CSV, set them in the CMS after importing: '
          'Hero Image, Author, Blog Categories, FAQ S, Featured.')

    if args.check:
        print('--check given, nothing written')
        return 1 if blocked else 0

    out = Path(args.out).expanduser()
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    print(f'written to {out}')
    return 1 if blocked else 0


if __name__ == '__main__':
    sys.exit(main())
