#!/usr/bin/env python3
"""
Daily GitHub PAT expiry check.

Reads the token file, makes a minimal authenticated request, and inspects:
- HTTP 401 -> token revoked/expired NOW. Write `auth-broken-github` sentinel
  in /Users/onur/.psfnetwork-drive/ for downstream scripts to detect.
- `github-authentication-token-expiration` response header -> compute days
  remaining; if <= 7, write `token-warning-github` sentinel with the date.
- Healthy -> remove any old sentinels.

This script is standalone (stdlib only) and runs from the daily launchd cron.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path


TOKEN_FILE = Path('/Users/onur/.psfnetwork-drive/github-token')
SENTINEL_DIR = Path('/Users/onur/.psfnetwork-drive')
REPO = 'ramsey-claude/psf-network-blog-production'
WARNING_DAYS = 7


def write_sentinel(name, payload):
    p = SENTINEL_DIR / name
    p.write_text(json.dumps(payload, indent=2) + '\n')


def clear_sentinel(name):
    p = SENTINEL_DIR / name
    if p.exists():
        p.unlink()


def main():
    if not TOKEN_FILE.exists():
        print(f'Token file missing at {TOKEN_FILE}', file=sys.stderr)
        write_sentinel('auth-broken-github', {
            'reason': 'token file missing',
            'checked_at': datetime.now(timezone.utc).isoformat(),
        })
        sys.exit(2)

    token = TOKEN_FILE.read_text().strip()

    req = urllib.request.Request(f'https://api.github.com/repos/{REPO}')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', 'psfnetwork-token-check')

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            expiry_header = resp.headers.get('github-authentication-token-expiration')
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print('Token returns 401 - revoked or expired.', file=sys.stderr)
            write_sentinel('auth-broken-github', {
                'reason': '401 from /repos/{REPO}',
                'checked_at': datetime.now(timezone.utc).isoformat(),
            })
            sys.exit(1)
        print(f'GitHub returned HTTP {e.code}: {e.reason}', file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f'Network error: {e}', file=sys.stderr)
        sys.exit(3)

    if status != 200:
        print(f'Unexpected status {status}', file=sys.stderr)
        sys.exit(3)

    # Healthy. Clear any old broken sentinel.
    clear_sentinel('auth-broken-github')

    if not expiry_header:
        # Classic PAT (no expiry exposed) or fine-grained without header.
        # No warning to issue. Clear the warning sentinel.
        clear_sentinel('token-warning-github')
        print('Token healthy; no expiry header (classic PAT or fine-grained without header).')
        return

    # Parse "Mon, 29 May 2026 12:00:00 GMT" style date
    try:
        expiry = datetime.strptime(expiry_header, '%Y-%m-%d %H:%M:%S %Z')
    except ValueError:
        try:
            from email.utils import parsedate_to_datetime
            expiry = parsedate_to_datetime(expiry_header)
        except Exception:
            print(f'Could not parse expiry header: {expiry_header}', file=sys.stderr)
            return

    days_left = (expiry - datetime.now(timezone.utc)).days
    print(f'Token expires at {expiry.isoformat()} ({days_left} days from now).')

    if days_left <= WARNING_DAYS:
        write_sentinel('token-warning-github', {
            'expiry': expiry.isoformat(),
            'days_left': days_left,
            'checked_at': datetime.now(timezone.utc).isoformat(),
            'action': 'run bash workflow/rotate-github-token.sh to install a new PAT',
        })
        print(f'WARNING: {days_left} days until expiry. Sentinel written.')
    else:
        clear_sentinel('token-warning-github')


if __name__ == '__main__':
    main()
