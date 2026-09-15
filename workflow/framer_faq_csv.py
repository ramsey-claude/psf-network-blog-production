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

The collection is named FAQs and its fields were read off the CMS on
2026-08-17: Question, Answer, Slug, Status, and Article. That last one is a
reference back to the Articles collection, which means the link is importable
from this side and FAQ S does not have to be filled in by hand from the
article. The Article column carries the article's TITLE, because that is what
the reference renders in the CMS; --article-by slug switches it if the import
matches on slug instead.

Slugs are the one place this deviates from what the collection already
contains. The existing 73 items use a bare slugified question, with a numeric
suffix on collision (are-these-platforms-safe-2). Copying that convention
would risk a Batch 2 question slugifying onto an existing Batch 1 item's slug,
and Framer treats a slug match as an update, so a published Batch 1 FAQ would
be silently overwritten. The default here prefixes the article slug, which
cannot collide with anything already there. --slug-style bare reproduces the
existing convention, with in-batch collisions suffixed, for when matching the
convention matters more than the safety margin.

Status defaults to Draft. Importing 94 items straight to Live would publish
FAQ entries for articles that are not published yet.

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
    ap.add_argument('--article-field', default='Article')
    ap.add_argument('--article-by', choices=['title', 'slug'], default='slug',
                    help='what the Article reference is matched on. Default is '
                         'slug: the 2026-08-17 import sent titles and every '
                         'Article cell came back empty')
    ap.add_argument('--slug-style', choices=['prefixed', 'bare'],
                    default='prefixed',
                    help='prefixed cannot collide with the 73 items already in '
                         'the collection; bare copies their convention')
    ap.add_argument('--status', default=None,
                    help='NOT recommended. Framer does not map a Status column '
                         'onto its built-in publish state; the 2026-08-17 '
                         'import created a second, junk field called Status '
                         'instead, and the real state defaulted to Live. Omit '
                         'this and set the publish state in the CMS')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    slugs = args.slug or (_fb.BATCH2 if args.batch2 else [])
    if not slugs:
        print('nothing to do: pass --batch2 or --slug', file=sys.stderr)
        return 2

    fields = [args.question_field, args.answer_field, args.article_field,
              'Slug']
    if args.status:
        fields.append('Status')
    rows, empty, seen_slugs = [], [], {}
    for s in slugs:
        src = BLOG / s / 'draft-v2-humanized.md'
        if not src.exists():
            src = BLOG / s / 'draft.md'
        if not src.exists():
            empty.append((s, 'no draft'))
            continue
        notes, body = _fb._mpk.split_notes(src.read_text(encoding='utf-8'))
        title = _fb._mpk.parse_notes(notes).get('title', '').strip()
        if args.article_by == 'title' and not title:
            empty.append((s, 'no Title, cannot fill the Article reference'))
            continue
        pairs = faq_pairs(body)
        if not pairs:
            empty.append((s, 'no FAQ section found'))
            continue
        for q, a in pairs:
            # Framer identifies an item by slug. Prefixed slugs cannot hit an
            # existing item; bare ones can, so they are de-duplicated within
            # the batch the way the collection already does it.
            base = slugify(q) if args.slug_style == 'bare' else f'{s}-{slugify(q)}'
            base = base[:100]
            n = seen_slugs.get(base, 0) + 1
            seen_slugs[base] = n
            slug_val = base if n == 1 else f'{base}-{n}'
            rows.append({
                args.question_field: q,
                args.answer_field: a,
                args.article_field: title if args.article_by == 'title' else s,
                'Slug': slug_val,
                **({'Status': args.status} if args.status else {}),
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
    print(f'Article reference matched by {args.article_by}; '
          f'slug style={args.slug_style}; '
          f'Status column {"included" if args.status else "omitted"}')
    if args.slug_style == 'bare':
        print('WARNING: bare slugs can match an item already in the collection, '
              'which Framer treats as an update. Check against the existing 73 '
              'before importing.')

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
