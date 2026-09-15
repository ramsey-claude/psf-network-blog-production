#!/usr/bin/env python3
"""
Curl-verify every external link in the drafts and report what is dead.

Why this exists as a script instead of a shell one-liner: the cloud session
that produced most of this repo's recent work cannot reach the federal
domains at all. Its egress proxy answers 403 to CONNECT for sec.gov,
irs.gov, investor.gov, ecfr.gov and federalreserve.gov, so `curl` there
returns 000 for every URL and proves nothing. Verification has to run from a
machine with open egress, and when it does it should produce the same report
every time rather than whatever ad-hoc pipeline someone types that day.

Two checks run per URL:

  1. HTTP status, following redirects, with a browser User-Agent. sec.gov
     rejects default curl agents (incident-log 2026-05-14), so the agent
     string is not optional.
  2. Whether the final URL differs from the requested one. A 200 reached
     after a redirect still means the URL in the draft is stale: it works
     today because the publisher is being generous, and it breaks the day
     they stop.

Findings are grouped so that the interesting case is impossible to miss:
when two different URLs in the repo point at the same concept and only one
of them resolves, both appear together.

Usage:
    python3 workflow/verify_external_links.py                  # every draft
    python3 workflow/verify_external_links.py --batch2         # the 15 Batch 2 slugs
    python3 workflow/verify_external_links.py --slug reit-dividend-taxation
    python3 workflow/verify_external_links.py --batch2 --md report.md

Exit status is 1 when any URL is dead, so this can gate a delivery step.
"""
import argparse
import collections
import concurrent.futures
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOG = REPO / 'blog'

# Batch 2, by folder name. Kept explicit rather than derived from a date
# field: the whole point of a verification pass is that it does not depend on
# metadata that might itself be wrong.
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

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')

URL_RE = re.compile(r'https?://[^\s\)\]\>"\']+')

# Own-domain links are checked by tests/test_link_audit.py against the repo's
# folder list, which is stricter than a status code: an internal link can
# return 200 from the SPA shell while the article does not exist.
SKIP_HOSTS = ('psfnetwork.com',)

# URLs that share a concept. When one member resolves and another does not,
# the report says so instead of listing them fifty lines apart. Each entry is
# (label, substring that identifies a member).
CONCEPT_GROUPS = [
    ('Regulation A', ['exempt-offerings/regulation-a', 'exempt-offerings/regulation']),
    ('Regulation Crowdfunding', ['smallbusiness/exemptofferings/regcrowdfunding',
                                 'exempt-offerings/regulation-crowdfunding']),
    ('EDGAR entry point', ['sec.gov/edgar/search', 'sec.gov/search-filings']),
    ('Reg A forms', ['form1-a.pdf', 'form1-k.pdf']),
]


def concept_of(url):
    """Return the concept label for a URL, or None.

    Longest match wins so that '.../regulation-a' is not swallowed by the
    '.../regulation' prefix that is also a real, separate URL in the repo.
    """
    best = None
    for label, members in CONCEPT_GROUPS:
        for m in members:
            if m in url and (best is None or len(m) > best[1]):
                best = (label, len(m))
    return best[0] if best else None


def collect(slugs):
    """Return {url: {slug: [(line_no, in_sources)]}}."""
    found = collections.defaultdict(lambda: collections.defaultdict(list))
    for slug in slugs:
        for name in ('draft-v2-humanized.md', 'draft-v2.md', 'draft.md'):
            draft = BLOG / slug / name
            if draft.exists():
                break
        else:
            print(f'  skip, no draft: {slug}', file=sys.stderr)
            continue
        lines = draft.read_text(encoding='utf-8').split('\n')
        src_at = next((i for i, l in enumerate(lines)
                       if l.strip().lower().startswith('## sources')), len(lines))
        for i, line in enumerate(lines):
            for url in URL_RE.findall(line):
                url = url.rstrip('.,;')
                if any(h in url for h in SKIP_HOSTS):
                    continue
                found[url][slug].append((i + 1, i >= src_at))
    return found


def probe(url, timeout):
    """Return (status, final_url, error). status is '000' when curl failed."""
    try:
        out = subprocess.run(
            ['curl', '-sS', '-L', '-o', '/dev/null',
             '-w', '%{http_code}\t%{url_effective}',
             '--max-time', str(timeout), '-A', UA, url],
            capture_output=True, text=True, timeout=timeout + 10)
    except subprocess.TimeoutExpired:
        return '000', '', 'timed out'
    parts = out.stdout.strip().split('\t')
    status = parts[0] if parts else '000'
    final = parts[1] if len(parts) > 1 else ''
    err = out.stderr.strip().split('\n')[-1] if status == '000' else ''
    return status, final, err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', action='append', default=[],
                    help='check one article; repeatable')
    ap.add_argument('--batch2', action='store_true',
                    help='check the 15 Batch 2 articles')
    ap.add_argument('--timeout', type=int, default=25)
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--md', help='also write a markdown report to this path')
    args = ap.parse_args()

    if args.slug:
        slugs = args.slug
    elif args.batch2:
        slugs = BATCH2
    else:
        slugs = sorted(p.name for p in BLOG.iterdir() if p.is_dir())

    found = collect(slugs)
    if not found:
        print('no external URLs found')
        return 0
    urls = sorted(found)
    print(f'{len(urls)} unique external URLs across {len(slugs)} articles\n')

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futures = {ex.submit(probe, u, args.timeout): u for u in urls}
        for n, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            u = futures[fut]
            results[u] = fut.result()
            status = results[u][0]
            mark = 'ok  ' if status.startswith('2') else 'DEAD'
            print(f'  [{n:>2}/{len(urls)}] {mark} {status}  {u}')

    dead, moved, ok = [], [], []
    for u in urls:
        status, final, err = results[u]
        if not status.startswith('2'):
            dead.append(u)
        elif final and final.rstrip('/') != u.rstrip('/'):
            moved.append(u)
        else:
            ok.append(u)

    blocked = [u for u in dead if results[u][0] == '000']

    # A 403 from these hosts is anti-bot, not a broken URL. sec.gov rejects
    # automated agents from any machine regardless of User-Agent
    # (incident-log 2026-05-14), and ecfr.gov answers with a
    # unblock.federalregister.gov interstitial. curl cannot decide whether
    # such a URL is live, so the report must not call it dead: a human has to
    # open it in a real browser. Learned the hard way on 2026-08-17, when a
    # verification run from an unblocked machine returned 403 for all 14
    # sec.gov URLs and the raw output read as fourteen broken links.
    ANTIBOT_HOSTS = ('sec.gov', 'ecfr.gov')
    unverifiable = [u for u in dead
                    if results[u][0] == '403'
                    and any(h in u for h in ANTIBOT_HOSTS)]
    dead = [u for u in dead if u not in unverifiable]

    def report(w):
        w('# External link verification\n')
        w(f'{len(urls)} unique URLs, {len(slugs)} articles. '
          f'{len(ok)} clean, {len(moved)} redirected, {len(dead)} dead, '
          f'{len(unverifiable)} unverifiable by machine.\n')
        if blocked:
            w('\n**Every dead result below is status 000, which means curl never '
              'reached the host.** That is a local network problem, not a broken '
              'link. Re-run from a machine with open egress before believing it.\n')
        for title, group, note in (
            ('Dead', dead, 'fix or replace these'),
            ('Redirected', moved,
             'these resolve today only because the publisher redirects them; '
             'update the draft to the final URL'),
            ('Unverifiable by machine', unverifiable,
             'the host blocks automated agents, so a 403 here says nothing '
             'about whether the page exists. Open each one in a real browser'),
        ):
            if not group:
                continue
            w(f'\n## {title} ({len(group)}) - {note}\n')
            for u in group:
                status, final, err = results[u]
                w(f'\n### `{u}`\n')
                w(f'- Status: {status}{" (" + err + ")" if err else ""}\n')
                if final and final.rstrip('/') != u.rstrip('/'):
                    w(f'- Lands on: `{final}`\n')
                c = concept_of(u)
                if c:
                    w(f'- Concept: {c}\n')
                for slug, hits in sorted(found[u].items()):
                    where = 'Sources' if all(s for _, s in hits) else 'BODY'
                    # A markdown link written as [url](url) puts the same URL
                    # on one line twice; report the line once.
                    ln = ', '.join(str(n) for n in sorted({n for n, _ in hits}))
                    w(f'- `{slug}` line {ln} ({where})\n')

        conflicts = []
        for label, _ in CONCEPT_GROUPS:
            members = [u for u in urls if concept_of(u) == label]
            if len(members) < 2:
                continue
            good = [u for u in members if u in ok]
            bad = [u for u in members if u not in ok]
            if good and bad:
                conflicts.append((label, good, bad))
        if conflicts:
            w('\n## Same concept, different URLs\n')
            w('\nThe repo cites one thing at more than one address and they do '
              'not agree. Standardise on the working one.\n')
            for label, good, bad in conflicts:
                w(f'\n**{label}**\n')
                for u in good:
                    w(f'- keep: `{u}`\n')
                for u in bad:
                    w(f'- replace: `{u}` ({results[u][0]})\n')

    lines = []
    report(lines.append)
    text = ''.join(lines)
    print('\n' + '=' * 72)
    print(text)
    if args.md:
        Path(args.md).write_text(text, encoding='utf-8')
        print(f'written to {args.md}')

    return 1 if dead else 0


if __name__ == '__main__':
    sys.exit(main())
