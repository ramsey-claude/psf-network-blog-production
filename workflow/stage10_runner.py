#!/usr/bin/env python3
"""
Stage 10 post-publish QA runner. Standalone — does not require a Claude session.

For each published post in the PSFnetwork repo:
1. Check if the live URL (psfnetwork.com/blog/[slug]) responds 200.
2. If live and Stage 10 not already done, run the automatable checks:
   - HTTP status 200
   - JSON-LD schema presence (Article, FAQ, Breadcrumb)
   - Canonical URL matches
   - Title tag and meta description present
3. Write `post-publish-report.md` to the repo for that slug.
4. Update `pipeline-state.json` with `flags.post_publish_qa.completed_at` and per-check results.
5. Push both files as a single commit.

Items that require an LLM (AI citation testing in Perplexity/ChatGPT, GSC indexing
submission) are documented in the report as "manual follow-up" but not blocked.

Configuration via env vars:
- PSFNETWORK_GITHUB_TOKEN: GitHub PAT for ramsey-claude/psf-network-blog-production
- PSFNETWORK_SITE_BASE: live site base URL (default https://psfnetwork.com)
- PSFNETWORK_REPO: GitHub repo (default ramsey-claude/psf-network-blog-production)

Designed to be idempotent. Re-running on an already-checked post is a no-op.

Invocation (typically by launchd or manually):
    .venv/bin/python3 workflow/stage10_runner.py
"""
import base64
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

SENTINEL_DIR = Path('/Users/onur/.psfnetwork-drive')
RETRY_BACKOFF = [2, 8, 30]  # seconds; max 3 attempts on transient failure


def _resolve_github_token():
    token = os.environ.get('PSFNETWORK_GITHUB_TOKEN', '')
    if token:
        return token
    token_file = os.environ.get('PSFNETWORK_GITHUB_TOKEN_FILE', '')
    if token_file and Path(token_file).exists():
        return Path(token_file).read_text().strip()
    return ''


GITHUB_TOKEN = _resolve_github_token()
SITE_BASE = os.environ.get('PSFNETWORK_SITE_BASE', 'https://psfnetwork.com')
REPO = os.environ.get('PSFNETWORK_REPO', 'ramsey-claude/psf-network-blog-production')
GH_API = f'https://api.github.com/repos/{REPO}'
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
      'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15')


def _write_auth_broken(reason):
    """Write auth-broken-github sentinel and exit. Used on hard auth failures."""
    SENTINEL_DIR.mkdir(parents=True, exist_ok=True)
    (SENTINEL_DIR / 'auth-broken-github').write_text(json.dumps({
        'reason': reason,
        'detected_by': 'stage10_runner.gh_request',
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'remediation': 'Run bash workflow/rotate-github-token.sh to install a new PAT.',
    }, indent=2) + '\n')


def gh_request(method, path, body=None, accept='application/vnd.github+json'):
    """GitHub API call with retry on 5xx/429 and sentinel-on-401."""
    url = f'{GH_API}{path}' if path.startswith('/') else path
    data = json.dumps(body).encode('utf-8') if body is not None else None

    last_err = None
    for attempt, backoff in enumerate([0] + RETRY_BACKOFF):
        if backoff:
            print(f'  gh_request retry {attempt}/{len(RETRY_BACKOFF)} after {backoff}s '
                  f'({method} {path}): {last_err}', file=sys.stderr)
            time.sleep(backoff)
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header('Authorization', f'Bearer {GITHUB_TOKEN}')
        req.add_header('Accept', accept)
        if data is not None:
            req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body_bytes = resp.read()
                if not body_bytes:
                    return {}
                if accept.endswith('json') or 'json' in resp.headers.get('Content-Type', ''):
                    return json.loads(body_bytes)
                return body_bytes
        except urllib.error.HTTPError as e:
            if e.code == 401:
                _write_auth_broken(f'401 from {method} {path}')
                print(f'GitHub returned 401 — token revoked/expired. Sentinel written. '
                      f'Exit 5.', file=sys.stderr)
                sys.exit(5)
            if e.code == 429 or 500 <= e.code < 600:
                last_err = f'HTTP {e.code}'
                continue  # retry
            raise  # other 4xx: real client error, no retry
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = f'network {e}'
            continue  # retry

    # Exhausted retries
    raise RuntimeError(f'gh_request {method} {path} failed after retries: {last_err}')


def fetch_url(url):
    """GET a URL with a browser-like UA. Returns (status, body_bytes) or (status, None) on error."""
    req = urllib.request.Request(url)
    req.add_header('User-Agent', UA)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def list_published_slugs():
    """List slugs under blog/ that have a published pipeline-state.json."""
    tree = gh_request('GET', '/contents/blog')
    slugs = []
    for entry in tree:
        if entry.get('type') != 'dir':
            continue
        slug = entry['name']
        try:
            state_raw = gh_request('GET', f'/contents/blog/{slug}/pipeline-state.json')
        except urllib.error.HTTPError:
            continue
        try:
            content = base64.b64decode(state_raw['content']).decode('utf-8')
            state = json.loads(content)
        except Exception:
            continue
        if state.get('stage') == 'published':
            slugs.append((slug, state, state_raw['sha']))
    return slugs


def already_done(state):
    return bool(state.get('flags', {}).get('post_publish_qa', {}).get('completed_at'))


SCHEMA_RE = re.compile(
    r'<script[^>]+type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel=[\'"]canonical[\'"][^>]*href=[\'"]([^\'"]+)[\'"]',
    re.IGNORECASE,
)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(
    r'<meta[^>]+name=[\'"]description[\'"][^>]+content=[\'"]([^\'"]+)[\'"]',
    re.IGNORECASE,
)


def run_checks(slug, state):
    """Run automatable Stage 10 checks for a slug. Returns a report dict."""
    canonical_expected = state.get('flags', {}).get('canonical') or \
        f'{SITE_BASE}/blog/{slug}'
    url = canonical_expected if canonical_expected.startswith('http') \
        else f'{SITE_BASE}/blog/{slug}'

    status, body = fetch_url(url)
    report = {
        'url': url,
        'http_status': status,
        'checks': {},
    }
    if status != 200 or not body:
        report['live'] = False
        report['notes'] = f'URL not live (status {status}); deferring'
        return report

    report['live'] = True
    html = body.decode('utf-8', errors='replace')

    # Canonical
    canon_match = CANONICAL_RE.search(html)
    canon = canon_match.group(1) if canon_match else None
    report['checks']['canonical_present'] = bool(canon)
    report['checks']['canonical_matches'] = canon == canonical_expected
    report['checks']['canonical_value'] = canon

    # Title and meta description
    title_match = TITLE_RE.search(html)
    title = title_match.group(1).strip() if title_match else None
    report['checks']['title_present'] = bool(title)
    report['checks']['title_length_ok'] = bool(title and 50 <= len(title) <= 65)
    report['checks']['title_value'] = title

    desc_match = META_DESC_RE.search(html)
    desc = desc_match.group(1) if desc_match else None
    report['checks']['meta_description_present'] = bool(desc)
    report['checks']['meta_description_length_ok'] = bool(desc and 140 <= len(desc) <= 170)

    # JSON-LD schemas
    schemas_found = []
    schema_types = set()
    for m in SCHEMA_RE.finditer(html):
        raw = m.group(1).strip()
        try:
            parsed = json.loads(raw)
        except Exception:
            continue
        items = parsed if isinstance(parsed, list) else [parsed]
        for item in items:
            if isinstance(item, dict):
                t = item.get('@type')
                if isinstance(t, list):
                    for tt in t:
                        schema_types.add(tt)
                elif t:
                    schema_types.add(t)
                schemas_found.append(item.get('@type'))
    report['checks']['schemas_found'] = sorted(schema_types)
    report['checks']['has_article_schema'] = any(
        s in schema_types for s in ('Article', 'BlogPosting', 'NewsArticle')
    )
    report['checks']['has_faq_schema'] = 'FAQPage' in schema_types
    report['checks']['has_breadcrumb_schema'] = 'BreadcrumbList' in schema_types

    return report


def write_report(slug, report):
    """Build the markdown post-publish-report content."""
    completed_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    lines = [
        f'# Post-publish Report - {slug}',
        '',
        f'| Field | Value |',
        f'|-------|-------|',
        f'| Completed at | {completed_at} |',
        f'| Live URL | {report["url"]} |',
        f'| HTTP status | {report["http_status"]} |',
        f'| Live | {report["live"]} |',
        '',
    ]
    if not report['live']:
        lines += [f'**Note:** {report.get("notes", "URL not live yet")}.', '',
                  'The runner will retry on the next scheduled run.']
        return '\n'.join(lines) + '\n'

    checks = report['checks']
    lines += [
        '## Automated checks',
        '',
        '| Check | Result |',
        '|-------|--------|',
        f'| HTTP 200 | {"PASS" if report["http_status"] == 200 else "FAIL"} |',
        f'| Canonical present | {"PASS" if checks["canonical_present"] else "FAIL"} |',
        f'| Canonical matches expected | {"PASS" if checks["canonical_matches"] else "FAIL"} |',
        f'| Title tag present | {"PASS" if checks["title_present"] else "FAIL"} |',
        f'| Title 50-65 chars | {"PASS" if checks["title_length_ok"] else "FAIL"} |',
        f'| Meta description present | {"PASS" if checks["meta_description_present"] else "FAIL"} |',
        f'| Meta description 140-170 chars | {"PASS" if checks["meta_description_length_ok"] else "FAIL"} |',
        f'| Article-type schema | {"PASS" if checks["has_article_schema"] else "FAIL"} |',
        f'| FAQ schema | {"PASS" if checks["has_faq_schema"] else "FAIL"} |',
        f'| Breadcrumb schema | {"PASS" if checks["has_breadcrumb_schema"] else "FAIL"} |',
        '',
        f'**Schemas detected:** {", ".join(checks["schemas_found"]) or "(none)"}',
        '',
        '## Manual follow-up (not automated)',
        '',
        '- AI citation test: query the focus keyword in Perplexity and ChatGPT (with web). Confirm whether the post is cited.',
        '- Google AI Overview check (if surfaced for the focus keyword).',
        '- GSC URL inspection / index request.',
        '- Core Web Vitals via PageSpeed Insights (LCP / INP / CLS).',
        '',
        'These items require either an LLM with web access or live GSC/CWV API calls and are not yet wired into the runner.',
    ]
    return '\n'.join(lines) + '\n'


def update_state(state, report):
    state.setdefault('flags', {})
    state['flags']['post_publish_qa'] = {
        'completed_at': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'live': report['live'],
        'http_status': report['http_status'],
        'checks': report.get('checks', {}),
    }
    state['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    # Replace stage10 pending step
    pending = state.get('pending_steps', [])
    state['pending_steps'] = [
        s for s in pending if not s.startswith('stage10-post-publish-qa')
    ]
    completed = state.get('completed_steps', [])
    if 'stage10-post-publish-qa' not in completed:
        completed.append('stage10-post-publish-qa')
    state['completed_steps'] = completed
    return state


def push_files(slug, report_md, state_obj, parent_sha):
    """Push post-publish-report.md and updated pipeline-state.json as one commit."""
    main_ref = gh_request('GET', '/git/ref/heads/main')
    main_sha = main_ref['object']['sha']
    main_commit = gh_request('GET', f'/git/commits/{main_sha}')
    base_tree = main_commit['tree']['sha']

    # Create blobs
    def make_blob(content_str):
        blob = gh_request(
            'POST', '/git/blobs',
            body={'content': base64.b64encode(content_str.encode('utf-8')).decode('ascii'),
                  'encoding': 'base64'},
        )
        return blob['sha']

    report_sha = make_blob(report_md)
    state_sha = make_blob(json.dumps(state_obj, indent=2) + '\n')

    tree_items = [
        {'path': f'blog/{slug}/post-publish-report.md', 'mode': '100644',
         'type': 'blob', 'sha': report_sha},
        {'path': f'blog/{slug}/pipeline-state.json', 'mode': '100644',
         'type': 'blob', 'sha': state_sha},
    ]
    new_tree = gh_request('POST', '/git/trees',
                          body={'base_tree': base_tree, 'tree': tree_items})
    commit = gh_request('POST', '/git/commits', body={
        'message': f'chore(stage10): post-publish QA for {slug} - auto-runner',
        'tree': new_tree['sha'],
        'parents': [main_sha],
    })
    gh_request('PATCH', '/git/refs/heads/main',
               body={'sha': commit['sha'], 'force': False})
    return commit['sha']


def main():
    # Check for known auth-broken sentinels written by other components.
    for name in ('auth-broken-github', 'auth-broken-drive'):
        s = SENTINEL_DIR / name
        if s.exists():
            print(f'Halting: {name} sentinel present.', file=sys.stderr)
            print(f'  {s.read_text().strip()}', file=sys.stderr)
            sys.exit(4)

    if not GITHUB_TOKEN:
        print('PSFNETWORK_GITHUB_TOKEN not set; aborting.', file=sys.stderr)
        sys.exit(2)

    slugs = list_published_slugs()
    print(f'Found {len(slugs)} published slugs.', file=sys.stderr)

    processed = 0
    for slug, state, _state_sha in slugs:
        if already_done(state):
            print(f'  {slug}: already done, skipping.', file=sys.stderr)
            continue
        print(f'  {slug}: running checks...', file=sys.stderr)
        report = run_checks(slug, state)
        if not report['live']:
            print(f'  {slug}: not live (status {report["http_status"]}); deferring.',
                  file=sys.stderr)
            continue
        report_md = write_report(slug, report)
        new_state = update_state(state, report)
        try:
            commit_sha = push_files(slug, report_md, new_state, None)
            print(f'  {slug}: pushed commit {commit_sha}.', file=sys.stderr)
            processed += 1
        except Exception as e:
            print(f'  {slug}: push failed: {e}', file=sys.stderr)

    print(f'Done. Processed {processed} slugs.', file=sys.stderr)


if __name__ == '__main__':
    main()
