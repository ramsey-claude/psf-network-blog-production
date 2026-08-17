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
  - FAQ S is a multi-reference and IS a column, holding the FAQ item slugs.
    Framer treats it and the FAQs collection's own Article reference as two
    independent fields, so importing the FAQ side alone leaves this empty.
  - Hero Image, Author and Blog Categories ARE columns, as an attempt rather
    than a certainty. Hero Image carries a Drive URL for Framer to fetch and
    Author carries the Author item's name for Framer to match. Whether the
    import maps either one is unverified, because it can only be answered in
    the import UI. If it will not, --no-refs drops all three and they go back
    to being set by hand; nothing else in the file changes.

The field split is not a guess. It was read off a live Batch 1 page
(what-is-proptech, fetched 2026-08-17) and matched against that article's
repo draft, which showed exactly which draft sections the template expects in
which CMS field:

  - The live body renders only the Quick Answer section and the article's
    question H2s. It contains no Sources heading and no FAQ heading.
  - TL;DR holds the Quick Answer prose, verbatim. Confirmed word for word
    against blog/what-is-proptech/draft.md.
  - Sources holds the source list as plain text; the template prints the
    "Sources:" label itself.
  - The FAQ is not in the body either. It lives in the FAQs collection and is
    reached through FAQ S; see below.

What is stripped from Content, and why:

  - The H1. Framer renders the Title field as the page heading, so leaving
    the markdown H1 in the body ships two competing H1s and costs the page
    its heading structure.
  - The [VISUAL-HERO-XX] placeholder. It is an instruction to a designer,
    not copy, and it would render as a literal paragraph of bracket text.
  - The Production Notes block, which is not part of the published body.
  - The Sources section, which moves to the Sources field. Leaving it in
    Content would print the sources inside the article body, where Batch 1
    does not have them.
  - The FAQ section, which moves to the FAQs collection.

What is deliberately kept in Content: the Quick Answer section, even though
its prose also goes into TL;DR. That is the live Batch 1 arrangement, not an
oversight.

The FAQ is removed from Content and lives only in the FAQs collection, reached
through FAQ S. Leaving it in shipped the questions twice on the first
published page, once as headings and once as the accordion.

One consequence, accepted by the operator on 2026-08-17: these articles ship
without FAQPage JSON-LD. The site builds that schema in the browser from
headings ending in a question mark, and a Batch 2 article's own H2s are
statements, so the FAQ headings were the only ones feeding it. The CMS has a
FAQ Schema field that looks like the place to put the schema instead, but the
operator reports it does not work, so it is not written to. Do not add it back
without testing it on a live page first.

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

# Cover images live only in Drive, one per article folder, named
# cover-<slug>-1200x630.webp (see workflow/visuals-tracker.md). Hero Image is
# an asset field, so a CSV can only offer Framer a URL to fetch. Whether it
# fetches one is untested: drive.google.com is blocked from the cloud session
# that wrote this, so the URLs below were built from verified file IDs but the
# fetch itself has to be confirmed in the import UI.
#
# Every one of these files is currently shared as "anyone: writer", which is
# what makes an unauthenticated fetch possible at all. That is also broader
# than the job needs, and it is flagged in visuals-tracker.md.
#
# If Framer rejects the default URL form, --hero-url-style offers the two
# other shapes Drive serves images through, so the retry does not need a code
# change.
HERO_FILE_IDS = {
    'debt-vs-equity-fractional': '1qfLSF3_eykRt9csDyPKhMyF2Mcblydwb',
    'fractional-real-estate-ira': '154dHiuk1r36A9FrMr5cTQXl8y5c0p-dh',
    'fractional-real-estate-vs-other-investments': '1aH0BEOUnwDgFJ9IwYkBGwsUdqDiCSl2b',
    'how-to-choose-fractional-real-estate-platform': '1hCtqouxtlCOqRdCVRgKQs8OOG-6EPlGQ',
    'how-to-read-reg-a-offering-circular': '1T1m-IhmgDkpRec4M3H8hgxgMlFhwsEmm',
    'legal-tax-guide-fractional-real-estate': '1KUhv3XusWgoYQLADv7hlAyA4I5s2XxuJ',
    'proptech-future-of-real-estate': '1uH-HuDoC6vwwVByIrhJQFa2aJHy5rvSg',
    'proptech-trends-2026': '1j1VlHsf4iLjYFVFxOdMJGgb81RzC3lO4',
    'real-estate-as-an-asset-class': '1Se9E_vf3QiFV93ubdYPqVG3jKY5FYUMm',
    'real-estate-etfs-vs-fractional': '1J5_RodWgP_VKqIWz4sLqs_pIzoXrCju7',
    'real-estate-vs-index-funds-retirement': '1RrL8yY0RtK3jvWkGFRZZvqe1Cy09w4aT',
    'reit-dividend-taxation': '1oTFNB1lqlxiPyLbvGzUrSmkD2YUHlWPZ',
    'single-family-vs-multifamily-fractional': '1gsvNfrVdQSdlceKD33OgaTNHsoUwmTAe',
    'tokenized-vs-traditional-fractional': '19f2izxyc3FaSCDZtHlYVXxkgwkHaLYbH',
    'how-to-sell-fractional-real-estate': '1poxF2es7J_c-MTllDWfNr0okPSPQ7wSD',
}

HERO_URL_STYLES = {
    'download': 'https://drive.google.com/uc?export=download&id={id}',
    'view': 'https://drive.google.com/uc?export=view&id={id}',
    'lh3': 'https://lh3.googleusercontent.com/d/{id}',
}

# The Author collection item's name, read off the live Batch 1 page, where the
# byline renders as "Youssef Kholeif" with the title in a separate line. A
# reference is matched by that name, so the CMS string is the bare name even
# though brand/personas.md records the byline as "Youssef Kholeif, CMO".
AUTHOR_NAME = 'Youssef Kholeif'

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

# The skill's framer_export.py stops at Content. TL;DR and Sources are added
# here because the live Batch 1 page proves the template renders both as their
# own blocks, and an import that leaves them empty ships a blank TL;DR box and
# no Sources block. Every reference and asset field stays out, per that
# script: importing one as plain text either fails or blanks the reference.
FIELDS = ['Title', 'Slug', 'Date', 'Excerpt', 'Meta Description', 'Keywords',
          'TL;DR', 'Sources', 'Content', 'Hero Image', 'Author',
          'Blog Categories', 'FAQ S']

HERO_PLACEHOLDER = re.compile(r'^\s*\[VISUAL-[A-Z0-9-]+\]\s*$', re.MULTILINE)
H1 = re.compile(r'^#\s+.*$', re.MULTILINE)
QUICK_ANSWER = re.compile(
    r'^##\s*(?:Quick Answer|The 60-Second Version)[^\n]*\n(.*?)(?=^##\s)',
    re.MULTILINE | re.DOTALL | re.IGNORECASE)
SOURCES = re.compile(r'^##\s*Sources[^\n]*\n(.*?)(?=^##\s|\Z)',
                     re.MULTILINE | re.DOTALL | re.IGNORECASE)
FAQ_SECTION = re.compile(
    r'^##\s*(?:Frequently Asked Questions|FAQ)[^\n]*\n(.*?)(?=^##\s|\Z)',
    re.MULTILINE | re.DOTALL | re.IGNORECASE)


# The risk paragraph that closes a Quick Answer is italic in the Batch 1
# drafts and plain prose in several Batch 2 ones, so an italics test alone
# lets it through into TL;DR. Batch 1's live TL;DR does not carry it, and a
# summary field is the wrong place for boilerplate: the page has its own
# Disclaimer block.
#
# Matched on phrases that only ever appear in the disclaimer, never in the
# analysis. Deliberately NOT a sentence-anchored pattern: the boilerplate runs
# to two or three sentences and only the first carries a marker, so anchoring
# to the whole paragraph matched nothing. "carry risk" is written out in full
# rather than as a stem, so analytical prose like "equity carries more risk"
# is left alone. Applied only inside the Quick Answer section, where the
# disclaimer is a known closing paragraph.
RISK_MARKERS = re.compile(
    r'\b(loss of principal|past performance|projections do not predict|'
    r'investments? carry risk|carry risk, including|involves? risk, including|'
    r'not tax advice|not investment advice)\b', re.IGNORECASE)


def is_risk_boilerplate(par: str) -> bool:
    # The length gate is a backstop: a genuine analytical paragraph that
    # mentions principal loss should survive, and disclaimers are short.
    return bool(RISK_MARKERS.search(par)) and len(par) <= 400


def plain(md: str) -> str:
    """Flatten inline markdown to plain text for the plain-text CMS fields."""
    md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', md)
    md = re.sub(r'\*\*([^*]+)\*\*', r'\1', md)
    md = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'\1', md)
    return re.sub(r'\s+', ' ', md).strip()


def quick_answer_prose(body_md: str) -> str:
    """The Quick Answer section's prose, minus its stat cards and disclaimer.

    Batch 1's live TL;DR is exactly this text. The stat cards are a bulleted
    list and the risk line is italic; both are furniture around the summary
    rather than part of it, and TL;DR is a plain-text field that cannot show
    either as anything but run-on prose.
    """
    m = QUICK_ANSWER.search(body_md)
    if not m:
        return ''
    keep = []
    for para in m.group(1).split('\n\n'):
        s = para.strip()
        if not s:
            continue
        if s.startswith(('-', '*', '>')) or re.match(r'^\*\*Stat cards', s, re.I):
            continue
        if re.match(r'^\*[^*].*\*$', s):          # italic risk/disclaimer line
            continue
        if re.match(r'^\*\*Key (numbers|figures)', s, re.I):
            continue
        if is_risk_boilerplate(s):
            continue
        keep.append(plain(s))
    return ' '.join(keep).strip()


def sources_plain(body_md: str) -> str:
    """The Sources list as plain text, one entry per line, links kept as URLs.

    Batch 1's Sources field reads "Publisher, "Title", https://..." per entry.
    The Batch 2 drafts write the URL as a markdown link whose anchor text is
    the URL itself, so the anchor is dropped and the href kept, which would
    otherwise print every address twice.
    """
    m = SOURCES.search(body_md)
    if not m:
        return ''
    out = []
    for line in m.group(1).split('\n'):
        s = line.strip()
        if not s or s.startswith('---'):
            continue
        s = re.sub(r'^\d+\.\s*', '', s)
        s = re.sub(r'^-\s*', '', s)
        # [https://x](https://x) -> https://x, and [Link](https://x) -> https://x
        s = re.sub(r'\[[^\]]*\]\((https?://[^)]+)\)', r'\1', s)
        s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
        s = re.sub(r'\s+', ' ', s).strip().rstrip('.')
        if s:
            out.append(s)
    return '\n'.join(out)


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


def _faq_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'framer_faq_csv', Path(__file__).resolve().parent / 'framer_faq_csv.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def faq_slugs_for(slug: str, body_md: str, sep: str = ', ') -> str:
    """The FAQ item slugs this article's questions were exported under.

    FAQ S is a multi-reference on Articles, and Article is a reference on FAQs.
    Framer treats those as two independent fields rather than two ends of one
    relation, so importing the FAQ side leaves FAQ S empty, which is what the
    first pass produced. Filling it needs the same slugs framer_faq_csv.py
    writes, so that module is the single source of the slug rule and is
    imported here lazily: it imports this one at module level, and a top-level
    import in both directions would not load.
    """
    faq = _faq_module()
    slugs = [f'{slug}-{faq.slugify(q)}'[:100] for q, _ in faq.faq_pairs(body_md)]
    return sep.join(slugs)


def row_for(slug: str, hero_style='download', category='', faq_sep=', '):
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
    faq_s = faq_slugs_for(slug, body_md, faq_sep)
    tldr = quick_answer_prose(body_md)
    sources = sources_plain(body_md)
    # Sources and FAQ move to their own fields, so drop both sections from the
    # body. Leaving the FAQ in shipped it twice on the first published page:
    # once as headings from Content and once as the accordion from FAQ S.
    body_md = SOURCES.sub('', body_md)
    body_md = FAQ_SECTION.sub('', body_md)
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
    if re.search(r'>Sources<', content):
        problems.append('a Sources heading survived into Content')
    if not tldr:
        problems.append('no Quick Answer section found, TL;DR would ship empty')
    if not sources:
        problems.append('no Sources section found')

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
        'TL;DR': tldr,
        'Sources': sources,
        'Content': content,
        'Hero Image': (HERO_URL_STYLES[hero_style].format(id=HERO_FILE_IDS[slug])
                       if slug in HERO_FILE_IDS else ''),
        'Author': AUTHOR_NAME,
        'Blog Categories': category,
        'FAQ S': faq_s,
    }
    if slug not in HERO_FILE_IDS:
        problems.append('no cover image recorded for this slug')
    if not faq_s:
        problems.append('no FAQ questions found, FAQ S would ship empty')
    return row, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', action='append', default=[])
    ap.add_argument('--batch2', action='store_true')
    ap.add_argument('-o', '--out', default='framer-import.csv')
    ap.add_argument('--check', action='store_true',
                    help='report and write nothing')
    ap.add_argument('--hero-url-style', choices=sorted(HERO_URL_STYLES),
                    default='download',
                    help='URL shape for the Drive cover image; try another if '
                         'Framer will not fetch the default')
    ap.add_argument('--faq-sep', default=', ',
                    help='separator between FAQ slugs in the FAQ S column; '
                         'change it if the import reads the list as one value')
    ap.add_argument('--no-refs', action='store_true',
                    help='drop the Hero Image, Author and Blog Categories '
                         'columns, for when the import will not map them')
    ap.add_argument('--category', default='',
                    help='value for Blog Categories, applied to every row. '
                         'Left empty by default: the Batch 2 drafts carry no '
                         'category field, and guessing one would invent a '
                         'taxonomy')
    args = ap.parse_args()

    slugs = args.slug or (BATCH2 if args.batch2 else [])
    if not slugs:
        print('nothing to do: pass --batch2 or --slug', file=sys.stderr)
        return 2

    rows, blocked = [], []
    for s in slugs:
        row, problems = row_for(s, args.hero_url_style, args.category,
                                args.faq_sep)
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
        print(f'      TL;DR {len(row["TL;DR"])} chars  '
              f'Sources {len(row["Sources"].splitlines())} entries  '
              f'FAQ S {len([x for x in row["FAQ S"].split(",") if x.strip()])} refs')

    for s, problems in blocked:
        print(f'  SKIP {s}: {"; ".join(problems)}', file=sys.stderr)

    if not rows:
        print('\nno rows produced', file=sys.stderr)
        return 1

    print(f'\n{len(rows)} row(s) ready, {len(blocked)} skipped')
    if not args.category:
        print('Blog Categories is empty: pass --category to fill it, or set it '
              'in the CMS.')
    print('Never in this CSV, always set in the CMS: Featured.')
    print('Hero Image and Author are URLs and names for Framer to resolve. '
          'If the import will not map them, clear them with --no-refs and set '
          'both by hand.')

    if args.check:
        print('--check given, nothing written')
        return 1 if blocked else 0

    fields = FIELDS
    if args.no_refs:
        drop = {'Hero Image', 'Author', 'Blog Categories', 'FAQ S'}
        fields = [f for f in FIELDS if f not in drop]
        rows = [{k: v for k, v in r.items() if k not in drop} for r in rows]

    out = Path(args.out).expanduser()
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    print(f'written to {out}')
    return 1 if blocked else 0


if __name__ == '__main__':
    sys.exit(main())
