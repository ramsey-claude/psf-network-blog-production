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


def test_irs_urls_are_live_paths():
    """Every irs.gov URL used in drafts must be one of the known-working paths.

    The 2026-05-26 audit found /forms-pubs/about-schedule-k-1-form-1065 returns
    404. This test enforces that any irs.gov URL in a draft falls under a
    directory known to have live content. Add new paths to the allow-list
    only after curl-verifying they return 200.
    """
    ALLOW_PREFIXES = (
        'https://www.irs.gov/instructions/',
        'https://www.irs.gov/publications/',
        'https://www.irs.gov/taxtopics/',
        'https://www.irs.gov/newsroom/',
        'https://www.irs.gov/retirement-plans/',
        'https://www.irs.gov/forms-pubs/about-form-1065',
        'https://www.irs.gov/forms-pubs/about-form-',
        'https://www.irs.gov/forms-pubs/about-schedule-e',
    )
    # Known-404 URLs that must never appear. Overrides ALLOW_PREFIXES.
    KNOWN_404 = (
        'https://www.irs.gov/newsroom/one-big-beautiful-bill-business-tax-provisions-youtube-video-text-script',
    )
    bad = []
    for path in _all_md_files():
        text = path.read_text(encoding='utf-8')
        for url in re.findall(r'https://www\.irs\.gov/[^\s,)\]"]+', text):
            cleaned = url.rstrip('.,;:)')
            if cleaned in KNOWN_404 or not any(cleaned.startswith(p) for p in ALLOW_PREFIXES):
                bad.append((str(path.relative_to(REPO_ROOT)), cleaned))
    assert bad == [], (
        'IRS URL not on the known-live allow-list. Verify with curl before '
        'adding a new prefix to ALLOW_PREFIXES:\n'
        + '\n'.join(f'  {p}: {u}' for p, u in bad)
    )


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
