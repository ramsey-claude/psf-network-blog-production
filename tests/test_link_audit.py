"""Regression: 2026-05-26 audit found broken IRS K-1 + FDIC URLs propagating
across 13 files. These tests pin the URL patterns to known-good values so a
future bulk edit cannot silently reintroduce the 404s.
"""
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BLOG = REPO_ROOT / 'blog'


# URLs that returned 404 in the audit, never to be reintroduced.
BANNED_URLS = [
    'https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1065',
    'https://www.fdic.gov/resources/deposit-insurance/what-is-deposit-insurance/index.html',
    'https://www.fdic.gov/resources/deposit-insurance/what-is-deposit-insurance/',
]


def _all_md_files():
    return [p for p in BLOG.rglob('*.md')]


def test_banned_urls_not_present_in_any_blog_file():
    """Any of the 404 URLs from the 2026-05-26 audit must not appear."""
    offenders = []
    for path in _all_md_files():
        text = path.read_text(encoding='utf-8')
        for url in BANNED_URLS:
            if url in text:
                offenders.append((str(path.relative_to(REPO_ROOT)), url))
    assert offenders == [], (
        'Banned (known-404) URLs found in blog/. The 2026-05-26 audit '
        'replaced these with working alternatives. Do not reintroduce:\n'
        + '\n'.join(f'  {p}: {u}' for p, u in offenders)
    )


def test_irs_k1_uses_instructions_url():
    """Posts that reference Schedule K-1 must point to the i1065sk1 page."""
    correct = 'https://www.irs.gov/instructions/i1065sk1'
    refers_to_k1 = []
    for path in _all_md_files():
        text = path.read_text(encoding='utf-8')
        if 'Schedule K-1' in text and 'irs.gov' in text:
            refers_to_k1.append(path)
    # Every K-1-referencing file with an IRS URL should use the correct one
    bad = []
    for path in refers_to_k1:
        text = path.read_text(encoding='utf-8')
        urls = re.findall(r'https://www\.irs\.gov/[^\s,)\]"]+', text)
        cleaned = [u.rstrip('.,;:)') for u in urls]
        if cleaned and not any(u == correct or u.startswith('https://www.irs.gov/forms-pubs/about-form-1065') for u in cleaned):
            bad.append((str(path.relative_to(REPO_ROOT)), cleaned))
    assert bad == [], f'Files referencing Schedule K-1 with non-canonical IRS URL: {bad}'


def test_internal_links_resolve_to_existing_slugs():
    """Every /blog/[slug] internal link must point to a slug that exists."""
    existing_slugs = {d.name for d in BLOG.iterdir() if d.is_dir()}
    bad = []
    for path in _all_md_files():
        text = path.read_text(encoding='utf-8')
        for slug in re.findall(r'\]\(/blog/([a-z0-9-]+)\)', text):
            if slug not in existing_slugs:
                bad.append((str(path.relative_to(REPO_ROOT)), slug))
    assert bad == [], f'Internal links pointing to non-existent slugs: {bad}'
