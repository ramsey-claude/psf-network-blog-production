#!/usr/bin/env python3
"""
Brief preflight check.

Stage 2 (Draft generation) refuses to start if the brief does not have all
required sections per `checklist/brief-required-sections.md`. This script
is the automated enforcement.

Usage:
    python3 workflow/brief_preflight.py blog/<slug>/brief.md

Exit codes:
    0  brief is ready for Stage 2
    1  brief is missing required sections; do not start Stage 2
    2  invocation error (file not found, bad args)
"""
import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    'Metadata',
    'Target Keywords',
    'ICP',
    'Content Angle',
    'Human Anchors',
    'Competitor Gap',
    'Regulatory Flags',
]

HUMAN_ANCHOR_SUBFIELDS = [
    'Real Story',
    'POV Anchor',
    'Contrarian Note',
]

PLACEHOLDER_TOKENS = ['TODO', 'TBD', '[insert', '[fill', 'XXX', 'PLACEHOLDER']

MIN_ANCHOR_WORDS = 40


def check_brief(path: Path) -> list[str]:
    """Return a list of failure reasons. Empty list = pass."""
    if not path.exists():
        return [f'Brief file not found: {path}']

    text = path.read_text(encoding='utf-8')
    failures = []

    # 1. Required sections present (as ## headers)
    for section in REQUIRED_SECTIONS:
        # Match `## Section` allowing trailing chars
        pattern = re.compile(r'^##\s+' + re.escape(section), re.MULTILINE)
        if not pattern.search(text):
            failures.append(f'Missing required section: ## {section}')

    # 2. Human Anchors sub-fields (A. Real Story, B. POV Anchor, C. Contrarian Note)
    ha_match = re.search(
        r'^##\s+Human Anchors.*?(?=^##\s+|\Z)',
        text,
        re.MULTILINE | re.DOTALL,
    )
    if ha_match:
        ha_text = ha_match.group(0)
        for sub in HUMAN_ANCHOR_SUBFIELDS:
            pattern = re.compile(r'^###\s+[A-C]?\.?\s*' + re.escape(sub), re.MULTILINE)
            if not pattern.search(ha_text):
                failures.append(f'Missing Human Anchor sub-field: ### {sub}')
            else:
                # Check word count and placeholder absence
                sub_match = re.search(
                    r'^###\s+[A-C]?\.?\s*' + re.escape(sub) + r'.*?(?=^###|\Z)',
                    ha_text,
                    re.MULTILINE | re.DOTALL,
                )
                if sub_match:
                    sub_body = sub_match.group(0)
                    # Strip the header line and count words
                    body_lines = sub_body.split('\n')[1:]
                    body_text = ' '.join(body_lines).strip()
                    word_count = len(body_text.split())
                    if word_count < MIN_ANCHOR_WORDS:
                        failures.append(
                            f'Human Anchor {sub} too short '
                            f'({word_count} words, need >= {MIN_ANCHOR_WORDS})'
                        )
                    for token in PLACEHOLDER_TOKENS:
                        if token.lower() in body_text.lower():
                            failures.append(
                                f'Human Anchor {sub} contains placeholder token: {token!r}'
                            )

        # Source field must be populated
        if not re.search(r'^###\s+Source', ha_text, re.MULTILINE):
            failures.append('Missing Human Anchors ### Source attribution')

    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('brief_path', help='Path to blog/<slug>/brief.md')
    ap.add_argument('--quiet', action='store_true',
                    help='Only print on failure')
    args = ap.parse_args()

    path = Path(args.brief_path)
    failures = check_brief(path)

    if failures:
        print(f'\nBRIEF PREFLIGHT FAILED: {path}', file=sys.stderr)
        for f in failures:
            print(f'  - {f}', file=sys.stderr)
        print('\nResolve every item before Stage 2 starts.', file=sys.stderr)
        print('See checklist/brief-required-sections.md for the spec.', file=sys.stderr)
        return 1

    if not args.quiet:
        print(f'BRIEF PREFLIGHT PASS: {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
