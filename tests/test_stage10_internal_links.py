"""Regression: the 2026-07-21 live-site audit found zero internal links on
every published article because hyperlinks are dropped in the Google Doc to
Framer paste. Drafts passed qa-gate.md's "at least 2 internal links" rule while
the live pages had none, and the gap went unnoticed for eight weeks because
Stage 10 only checked the canonical tag. These tests pin the live-page count.
"""
import stage10_runner as runner


SLUG = 'how-fractional-real-estate-is-taxed'


def _page(*hrefs):
    body = ''.join(f'<a href="{h}">x</a>' for h in hrefs)
    return f'<html><body>{body}</body></html>'


def test_counts_distinct_other_posts_only():
    html = _page(
        'https://www.psfnetwork.com/blog/reits-vs-fractional-real-estate',
        'https://www.psfnetwork.com/blog/reits-vs-fractional-real-estate',  # dup
        '/blog/reg-a-vs-reg-d-for-fractional-investors',                      # relative
        'https://psfnetwork.com/blog/legal-tax-guide-fractional-real-estate/',  # no www, trailing slash
        f'https://www.psfnetwork.com/blog/{SLUG}',                           # self
        'https://www.psfnetwork.com/',                                        # not a post
        'https://www.irs.gov/blog/anything',                                  # external
    )
    n, targets = runner.count_internal_links(html, SLUG)
    assert n == 3
    assert targets == [
        'legal-tax-guide-fractional-real-estate',
        'reg-a-vs-reg-d-for-fractional-investors',
        'reits-vs-fractional-real-estate',
    ]


def test_zero_links_is_reported_not_crashed():
    n, targets = runner.count_internal_links(_page('https://www.psfnetwork.com/'), SLUG)
    assert (n, targets) == (0, [])


def test_report_flags_pages_below_two_links():
    """The qa-gate.md threshold is 2; one link must FAIL, two must PASS."""
    one = _page('/blog/reits-vs-fractional-real-estate')
    two = one + '<a href="/blog/what-is-proptech">y</a>'
    assert runner.count_internal_links(one, SLUG)[0] < 2
    assert runner.count_internal_links(two, SLUG)[0] >= 2
