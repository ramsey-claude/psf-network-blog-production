#!/usr/bin/env python3
"""
Brand voice and punctuation rule checker.

Same rules as `.githooks/pre-commit` and `checklist/ai-tells.md` Tier 0/2,
but as a standalone script so it can run in three places without local setup:

1. Inside Stage 8 (Publish) of the autonomous pipeline, before any commit.
   The pipeline is responsible for its own compliance; the operator does
   not need to install a local hook.

2. As a GitHub Action on every push to main. Server-side reactive backup.
   Catches anything the pipeline somehow let through.

3. As an optional local pre-commit hook (.githooks/pre-commit), for anyone
   editing the repo by hand who wants the same checks at commit time.

Exit codes:
  0  all checks pass
  1  one or more BLOCKING violations
  2  invocation error (bad args, missing files)

Usage:
  python3 workflow/check-rules.py                     # scan all .md files in repo
  python3 workflow/check-rules.py file1.md file2.md   # scan specific files
  python3 workflow/check-rules.py --staged            # scan only git-staged .md files
  python3 workflow/check-rules.py --diff-base SHA     # scan .md files changed since SHA

Default scope: every .md file in the repo excluding blog/**/draft.md (those go
through Stage 7 QA which has its own rules) and competitors/** (third-party
content notes). The full default scope is README.md, ROADMAP.md, checklist/,
workflow/, brand/. Override with explicit file args.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


BLOCKING = [
    # Tier 0: punctuation
    ('em-dash', re.compile(r'—'), 'literal em-dash character'),
    ('en-dash', re.compile(r'–'), 'literal en-dash character'),
    # Tier 2: brand voice
    ('guaranteed-return', re.compile(r'guaranteed\s+(return|yield|annual)', re.IGNORECASE),
     'guaranteed return language (bans even in negation)'),
    ('psfnetwork-casing', re.compile(r'\b(PSFnetwork|PSF\s+Network|PSFNETWORK|Psfnetwork)\b'),
     'psfnetwork casing variant (must be lowercase one word)'),
]

WARNING = [
    ('ai-tell-hype', re.compile(r'\b(unlock|leverage[sd]?|leveraging|robust|seamless|streamlined|synergy|harness|empower|myriad|plethora)\b', re.IGNORECASE),
     'HIGH-tier AI tell verb/adjective'),
    ('ai-tell-opener', re.compile(r'(in today.s rapidly evolving|now more than ever|when it comes to|in conclusion|at the end of the day)', re.IGNORECASE),
     'AI stock opener/closer phrase'),
]


def default_scope():
    files = []
    for pattern in ['README.md', 'ROADMAP.md']:
        p = REPO_ROOT / pattern
        if p.exists():
            files.append(p)
    for subdir in ['checklist', 'workflow', 'brand']:
        d = REPO_ROOT / subdir
        if d.is_dir():
            files.extend([p for p in d.rglob('*.md')])
    return sorted(set(files))


def staged_files():
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=AM'],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        return []
    return [REPO_ROOT / line for line in result.stdout.strip().split('\n')
            if line.endswith('.md') and (REPO_ROOT / line).exists()]


def diff_base_files(base_sha):
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=AM', base_sha, 'HEAD'],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        print(f'ERROR: git diff against {base_sha} failed: {result.stderr}', file=sys.stderr)
        sys.exit(2)
    return [REPO_ROOT / line for line in result.stdout.strip().split('\n')
            if line.endswith('.md') and (REPO_ROOT / line).exists()]


ALLOW_PRAGMA = re.compile(r'<!--\s*check-rules:\s*allow\s*-->')


def check_file(path):
    """Return (blocking_findings, warning_findings) for one file.

    Lines containing the pragma `<!-- check-rules: allow -->` are exempted
    from all checks. Use this on lines that legitimately document a banned
    pattern (e.g., the ban list itself, or a 'use/avoid' table).
    """
    try:
        text = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError) as e:
        return ([(f'read-error: {e}', 0, '')], [])

    lines = text.split('\n')
    allowed_lines = {i + 1 for i, line in enumerate(lines) if ALLOW_PRAGMA.search(line)}

    blocking = []
    warning = []
    for name, pattern, desc in BLOCKING:
        for m in pattern.finditer(text):
            line_no = text[:m.start()].count('\n') + 1
            if line_no in allowed_lines:
                continue
            blocking.append((name, line_no, m.group(0)[:60]))
    for name, pattern, desc in WARNING:
        for m in pattern.finditer(text):
            line_no = text[:m.start()].count('\n') + 1
            if line_no in allowed_lines:
                continue
            warning.append((name, line_no, m.group(0)[:60]))
    return (blocking, warning)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*', help='Explicit files to check. Empty = default scope.')
    ap.add_argument('--staged', action='store_true', help='Check only git-staged .md files')
    ap.add_argument('--diff-base', help='Check .md files changed since this SHA/ref')
    ap.add_argument('--quiet', action='store_true', help='Only print on findings')
    args = ap.parse_args()

    if args.staged:
        targets = staged_files()
    elif args.diff_base:
        targets = diff_base_files(args.diff_base)
    elif args.files:
        targets = [Path(f).resolve() for f in args.files]
    else:
        targets = default_scope()

    if not targets:
        if not args.quiet:
            print('No .md files in scope. Nothing to check.', file=sys.stderr)
        return 0

    total_blocking = 0
    total_warning = 0
    files_with_blocking = 0

    for path in targets:
        rel = path.relative_to(REPO_ROOT) if str(path).startswith(str(REPO_ROOT)) else path
        blocking, warning = check_file(path)
        if blocking:
            files_with_blocking += 1
            total_blocking += len(blocking)
            for name, ln, snippet in blocking:
                print(f'  [BLOCK] {rel}:{ln} {name}: {snippet!r}', file=sys.stderr)
        if warning:
            total_warning += len(warning)
            if not args.quiet:
                for name, ln, snippet in warning:
                    print(f'  [WARN ] {rel}:{ln} {name}: {snippet!r}', file=sys.stderr)

    if not args.quiet:
        print(
            f'\nScanned {len(targets)} files. '
            f'{total_blocking} BLOCKING ({files_with_blocking} files), '
            f'{total_warning} WARNING.',
            file=sys.stderr,
        )

    if total_blocking > 0:
        print(
            '\nBLOCKING findings present. Fix before commit/publish/merge.\n'
            'See checklist/ai-tells.md for the full rule set and replacement patterns.',
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
