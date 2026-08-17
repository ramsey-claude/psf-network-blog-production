#!/usr/bin/env python3
"""
Build a Framer CMS import CSV for the FAQ collection, one row per question.

Why this is separate from framer_batch_csv.py: the article's FAQ does not live
in the article. A live Batch 1 page renders its FAQ as an accordion whose DOM
arrives server-rendered from a Framer component named FAQ_CMS, with no
client-side script building it, which means the questions are items in their
own collection that the article points at through its FAQ S multi-reference.
Leaving the FAQ inside the article body produces headings instead of an
accordion. Batch 2 has 94 questions across 15 articles, so entering them by
hand is not a realistic option.

What this does NOT do: link the items back to their articles. FAQ S is a
multi-reference, and an import into the FAQ collection cannot populate a
reference field on a different collection. The linking step is manual, or it
runs from the article side if the FAQ collection turns out to carry an Article
reference of its own, in which case the Article Slug column below is already
the value that field needs.

Column names are a guess and are meant to be edited. The FAQ collection's real
field names were not observable from the rendered page, only the fact that it
holds a question and an answer. Check them in the CMS and pass --question-field
and --answer-field if they differ, rather than renaming the header by hand each
time.

Both draft FAQ shapes are handled: the Batch 2 "### question" heading form, and
the Batch 1 "**Q: ...**" / "A: ..." pair form.

Usage:
    python3 workflow/framer_faq_csv.py --batch2 -o ~/Desktop/batch2-faq.csv
    python3 workflow/framer_faq_csv.py --slug reit-dividend-taxation
    python3 workflow/framer_faq_csv.py --batch2 --question-field Question \
        --answer-field Answer
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
    'framer_batch_csv', Path(__file__).resolve().parent / 'framer_batch_csv.py')
_fb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fb)

FAQ_SECTION = re.compile(
    r'^##\s*(?:Frequently Asked Questions|FAQ)[^\n]*\n(.*?)(?=^##\s|\Z)',
    re.MULTILINE | re.DOTALL | re.IGNORECASE)


def slugify(text: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return s[:80].rstrip('-')


def faq_pairs(body_md: str):
    """Return [(question, answer_plain), ...] for either draft shape."""
    m = FAQ_SECTION.search(body_md)
    if not m:
        return []
    block = m.group(1)
    pairs = []

    # Batch 2: "### Question?" followed by one or more paragraphs.
    parts = re.split(r'^###\s+(.+?)\s*$', block, flags=re.MULTILINE)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            q = _fb.plain(parts[i])
            body = parts[i + 1] if i + 1 < len(parts) else ''
            a = ' '.join(_fb.plain(p) for p in body.split('\n\n') if p.strip())
            if q and a:
                pairs.append((q, a.strip()))
        return pairs

    # Batch 1: "**Q: ...**" then a line starting "A:".
    for m2 in re.finditer(
            r'\*\*Q:\s*(.+?)\*\*\s*\n+A:\s*(.+?)(?=\n\s*\n\*\*Q:|\Z)',
            block, re.DOTALL):
        q, a = _fb.plain(m2.group(1)), _fb.plain(m2.group(2))
        if q and a:
            pairs.append((q, a))
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', action='append', default=[])
    ap.add_argument('--batch2', action='store_true')
    ap.add_argument('-o', '--out', default='framer-faq.csv')
    ap.add_argument('--question-field', default='Question')
    ap.add_argument('--answer-field', default='Answer')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    slugs = args.slug or (_fb.BATCH2 if args.batch2 else [])
    if not slugs:
        print('nothing to do: pass --batch2 or --slug', file=sys.stderr)
        return 2

    fields = [args.question_field, args.answer_field, 'Slug', 'Article Slug']
    rows, empty = [], []
    for s in slugs:
        src = BLOG / s / 'draft-v2-humanized.md'
        if not src.exists():
            src = BLOG / s / 'draft.md'
        if not src.exists():
            empty.append((s, 'no draft'))
            continue
        _, body = _fb._mpk.split_notes(src.read_text(encoding='utf-8'))
        pairs = faq_pairs(body)
        if not pairs:
            empty.append((s, 'no FAQ section found'))
            continue
        for q, a in pairs:
            rows.append({
                args.question_field: q,
                args.answer_field: a,
                # Framer identifies an item by slug, so give each question a
                # stable one derived from the article and the question. Without
                # it a re-import creates duplicates rather than updating.
                'Slug': f'{s}-{slugify(q)}'[:100],
                'Article Slug': s,
            })
        print(f'  ok  {s}: {len(pairs)} question(s)')

    for s, why in empty:
        print(f'  SKIP {s}: {why}', file=sys.stderr)

    if not rows:
        print('\nno rows produced', file=sys.stderr)
        return 1

    lens = [len(r[args.answer_field]) for r in rows]
    print(f'\n{len(rows)} question(s) from {len(slugs) - len(empty)} article(s)')
    print(f'answers {min(lens)} to {max(lens)} chars')
    print(f'columns: {", ".join(fields)}')
    print('Article Slug is a helper, not a Framer field. Map it only if the '
          'FAQ collection has a reference back to the article; otherwise leave '
          'it unmapped and link FAQ S from the article side.')

    if args.check:
        print('--check given, nothing written')
        return 0

    out = Path(args.out).expanduser()
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    print(f'written to {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
