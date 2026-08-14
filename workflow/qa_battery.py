#!/usr/bin/env python3
"""
Standing content QA battery. One command, every canonical draft, every rule.

Why this exists (2026-08-11): the Batch 2 go-live QA caught six "guaranteed"
uses, eight broken or missing metas, and one headline problem in content that
had already been delivered. Root cause was not any single missed check; it was
that the full check battery lived in ad-hoc per-batch scripts that were
rewritten from scratch each time, so coverage fluctuated between runs. This
file is the permanent, versioned home of the battery. If a check matters, it
lives here; if it lives here, CI runs it on every push.

What it checks, per article (canonical draft = draft-v2-humanized.md if
present, else draft-v2.md, else draft.md):

FAIL (exit 1, CI red):
  F1  em-dash or en-dash anywhere in the file
  F2  the word "guaranteed" in any form, including negation and quotes
  F3  production labels leaked into the body ("Answer capsule:", "Risk note")
  F4  meta description missing
  F5  meta description length outside 150-160 characters
  F6  Google-Docs CSS residue (style blocks, .cN class selectors)
  F7  title missing, or (YAML-format drafts) title length outside 55-60
  F8  declared slug (or canonical tail) does not match the folder name

WARN (reported, not blocking):
  W1  title length outside 55-60 on Production-Notes drafts (Batch 2 titles
      were authored before the length rule; enforce on touch, not in bulk)
  W2  hero alt text missing or outside 60-120 characters
  W3  fewer than 2 inline internal links (FAIL for content published
      2026-07 onward, where the rule was in force at authoring time)
  W4  fewer than 2 inline external authority links from the allowed domain
      list (same date scoping as W3)
  W5  FAQ question count outside 5-6
  W6  "Related" section link count != 3
  W7  substantive H2 not in question format

Lines carrying `<!-- check-rules: allow -->` are exempt from F1/F2 (same
pragma as check-rules.py).

Usage:
  python3 workflow/qa_battery.py                # all articles, table output
  python3 workflow/qa_battery.py slug1 slug2    # specific articles
  python3 workflow/qa_battery.py --details      # per-finding detail lines

Parsing is imported from make_paste_kit.py (split_notes/parse_notes/ALIASES)
so the battery and the paste kit can never disagree about field extraction.
"""
import argparse
import importlib.util
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BLOG = REPO_ROOT / 'blog'

_spec = importlib.util.spec_from_file_location(
    'make_paste_kit', Path(__file__).resolve().parent / 'make_paste_kit.py')
_mpk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mpk)

ALLOW_PRAGMA = re.compile(r'<!--\s*check-rules:\s*allow\s*-->')

# The external-link and 2-internal-link rules entered qa-gate on 2026-07-22
# scoped "Batch 3 onward". Content authored under the rule fails; earlier
# content warns. Scoping key: the draft's published date.
LINK_RULES_SINCE = date(2026, 7, 1)

ALLOWED_EXTERNAL = (
    'investor.gov', 'sec.gov', 'irs.gov', 'finra.org', 'fdic.gov',
    'federalreserve.gov', 'congress.gov',
)

BANNED_BODY_LABELS = [
    (re.compile(r'\*\*Answer capsule:?\*\*|^Answer capsule:', re.M), 'Answer capsule label'),
    (re.compile(r'\*\*Risk note:?\*\*|^#{2,4}\s*Risk note', re.M), 'Risk note label (must be Disclaimer)'),
    (re.compile(r'\bComparison spoke\b'), 'hub/spoke jargon'),
]

CSS_RESIDUE = re.compile(r'<style|\.c\d+\s*\{|font-family:\s*"')

TEMPLATE_H2S = {
    'quick answer (60 seconds)', 'the 60-second version',
    'frequently asked questions', 'faq', 'related reading', 'related',
    'disclaimer', 'sources', 'author', 'key numbers',
}

MD_LINK = re.compile(r'\[[^\]]+\]\(([^)\s]+)\)')


def canonical_draft(folder: Path):
    for name in ('draft-v2-humanized.md', 'draft-v2.md', 'draft.md'):
        p = folder / name
        if p.exists():
            return p
    return None


def published_date(meta: dict, notes_block: str):
    m = re.search(r'[Pp]ublished:?\s*(\d{4})-(\d{2})-(\d{2})', notes_block)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def check_article(folder: Path):
    """Return (slug, fmt, fails, warns) where fails/warns are finding strings."""
    slug = folder.name
    draft = canonical_draft(folder)
    if draft is None:
        return slug, '-', [f'no draft file in {folder.name}/'], []

    text = draft.read_text(encoding='utf-8')
    lines = text.split('\n')
    exempt = {i for i, ln in enumerate(lines, 1) if ALLOW_PRAGMA.search(ln)}

    notes_block, body = _mpk.split_notes(text)
    meta = _mpk.parse_notes(notes_block) if notes_block else {}
    fmt = 'yaml' if text.startswith('---') else ('notes' if notes_block else 'bare')

    fails, warns = [], []

    # F1/F2: dashes and the banned word, pragma-aware
    for i, ln in enumerate(lines, 1):
        if i in exempt:
            continue
        if '—' in ln or '–' in ln:
            fails.append(f'F1 dash at line {i}')
        if re.search(r'\bguaranteed\b', ln, re.IGNORECASE):
            fails.append(f'F2 "guaranteed" at line {i}')

    # F3: leaked production labels
    for pat, desc in BANNED_BODY_LABELS:
        if pat.search(body):
            fails.append(f'F3 {desc}')

    # F4/F5: meta description
    md = meta.get('meta_description', '')
    if not md:
        fails.append('F4 meta description missing')
    elif not 150 <= len(md) <= 160:
        fails.append(f'F5 meta description {len(md)} chars (need 150-160)')

    # F6: Google-Docs CSS residue
    if CSS_RESIDUE.search(body):
        fails.append('F6 CSS residue in body')

    # F8: the draft's declared slug must match its folder name, and the
    # canonical URL must end in that same slug. A mismatch publishes the
    # article at an address nothing links to and orphans every inbound
    # internal link (found on article 13 three weeks after import; the link
    # test only checks that the target folder exists, so it passed).
    declared = meta.get('slug', '').strip().strip('/')
    if declared and declared != slug:
        fails.append(f'F8 slug "{declared}" does not match folder "{slug}"')
    canonical = meta.get('canonical', '').strip().rstrip('/')
    if canonical:
        tail = canonical.rsplit('/', 1)[-1]
        if tail != slug:
            fails.append(f'F8 canonical ends in "{tail}", folder is "{slug}"')

    # F7/W1: title
    title = meta.get('title', '')
    if not title:
        fails.append('F7 title missing')
    elif not 55 <= len(title) <= 60:
        finding = f'title {len(title)} chars (target 55-60)'
        (fails if fmt == 'yaml' else warns).append(
            ('F7 ' if fmt == 'yaml' else 'W1 ') + finding)

    # W2: hero alt
    alt = meta.get('hero_alt', '')
    if not alt:
        warns.append('W2 hero alt missing')
    elif not 60 <= len(alt) <= 120:
        warns.append(f'W2 hero alt {len(alt)} chars (target 60-120)')

    # W3/W4: inline links, date-scoped severity
    pub = published_date(meta, notes_block)
    strict_links = pub is not None and pub >= LINK_RULES_SINCE
    urls = MD_LINK.findall(body)
    internal = [u for u in urls if u.startswith('/blog/') or 'psfnetwork.com/blog' in u]
    external = [u for u in urls if any(d in u for d in ALLOWED_EXTERNAL)]
    if len(internal) < 2:
        (fails if strict_links else warns).append(
            ('W3 ' if not strict_links else 'F-W3 ') +
            f'{len(internal)} inline internal links (need 2+)')
    if len(external) < 2:
        (fails if strict_links else warns).append(
            ('W4 ' if not strict_links else 'F-W4 ') +
            f'{len(external)} inline external authority links (need 2+)')

    # W5: FAQ count. Two authoring styles: "**Q:**" bold labels and
    # "### question" headings under an FAQ H2.
    faq_q = len(re.findall(r'^\*\*Q:', body, re.M))
    m = re.search(r'^##\s*(Frequently Asked Questions|FAQ).*?(?=^##\s|\Z)',
                  body, re.M | re.S)
    if m:
        faq_q = max(faq_q, len(re.findall(r'^###\s', m.group(0), re.M)))
    if faq_q and not 5 <= faq_q <= 6:
        warns.append(f'W5 FAQ has {faq_q} questions (target 5-6)')
    elif faq_q == 0:
        warns.append('W5 no FAQ section detected')

    # W6: Related links
    m = re.search(r'^##\s*Related.*?(?=^##\s|\Z)', body, re.M | re.S)
    if m:
        n = len(MD_LINK.findall(m.group(0)))
        if n != 3:
            warns.append(f'W6 Related has {n} links (need exactly 3)')

    # W7: substantive H2s in question format
    for h2 in re.findall(r'^##\s+(.+)$', body, re.M):
        key = re.sub(r'[*_`]', '', h2).strip().lower()
        if key in TEMPLATE_H2S or any(key.startswith(t) for t in TEMPLATE_H2S):
            continue
        if not h2.rstrip().endswith('?'):
            warns.append(f'W7 non-question H2: "{h2.strip()[:60]}"')

    return slug, fmt, fails, warns


BASELINE_FILE = REPO_ROOT / 'workflow' / 'qa-baseline.txt'


def normalize(finding: str) -> str:
    return re.sub(r' at line \d+', '', finding)


def load_baseline():
    """Known legacy findings that do not fail CI.

    The ratchet: entries may only be REMOVED (after a backfill fixes the
    content), never added for new content. Every entry is a debt marker,
    not a permission. Format: slug<TAB>normalized finding.
    """
    if not BASELINE_FILE.exists():
        return set()
    out = set()
    for ln in BASELINE_FILE.read_text().split('\n'):
        ln = ln.strip()
        if ln and not ln.startswith('#') and '\t' in ln:
            slug, finding = ln.split('\t', 1)
            out.add((slug, finding))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slugs', nargs='*', help='Article slugs. Empty = all of blog/.')
    ap.add_argument('--details', action='store_true', help='Print every finding')
    ap.add_argument('--no-baseline', action='store_true',
                    help='Report baselined legacy findings as FAIL too')
    args = ap.parse_args()
    baseline = set() if args.no_baseline else load_baseline()

    folders = ([BLOG / s for s in args.slugs] if args.slugs
               else sorted(p for p in BLOG.iterdir() if p.is_dir()))
    for f in folders:
        if not f.is_dir():
            print(f'ERROR: no such article folder: {f}', file=sys.stderr)
            return 2

    rows = []
    for f in folders:
        slug, fmt, fails, warns = check_article(f)
        base = [x for x in fails if (slug, normalize(x)) in baseline]
        fails = [x for x in fails if (slug, normalize(x)) not in baseline]
        rows.append((slug, fmt, fails, warns, base))
    total_fail = sum(len(r[2]) for r in rows)
    total_warn = sum(len(r[3]) for r in rows)
    total_base = sum(len(r[4]) for r in rows)

    print(f'| {"Article":45} | Fmt   | FAIL | WARN | BASE |')
    print(f'|{"-"*47}|-------|------|------|------|')
    for slug, fmt, fails, warns, base in rows:
        print(f'| {slug:45} | {fmt:5} | {len(fails):4} | {len(warns):4} | {len(base):4} |'
              + ('' if not fails else '  <- FAIL'))
    print(f'\n{len(rows)} articles, {total_fail} FAIL, {total_warn} WARN, '
          f'{total_base} baselined legacy findings (workflow/qa-baseline.txt).')

    if args.details or total_fail:
        print()
        for slug, fmt, fails, warns, base in rows:
            shown = fails + (warns + base if args.details else [])
            if shown:
                print(f'{slug}:')
                for f_ in fails:
                    print(f'  [FAIL] {f_}')
                if args.details:
                    for b in base:
                        print(f'  [base] {b}')
                    for w in warns:
                        print(f'  [warn] {w}')

    return 1 if total_fail else 0


if __name__ == '__main__':
    sys.exit(main())
