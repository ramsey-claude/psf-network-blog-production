#!/usr/bin/env python3
"""
Gated Drive delivery wrapper.

Enforces the pipeline rule that Stage 9 (Drive delivery) only runs after
Stage 7 (Pre-publish QA) passes. The error this guards against is delivering
a draft to Drive without a corresponding qa-report-vN.md that records a
PUBLISH verdict. This was a real incident on 2026-05-26 (see incident log).

Usage:
    .venv/bin/python3 workflow/deliver.py \\
        --slug best-fractional-real-estate-platforms \\
        --version v2-humanized \\
        --folder-id 1jKP0k2m8tg6QeRKQEtzvx9jRWiuvwWqY \\
        --title "[v2 Humanized] Best Fractional Real Estate Platforms in 2026"

The wrapper:
1. Locates `blog/<slug>/draft-<version>.md` and `blog/<slug>/qa-report-<version>.md`.
   Both must exist. For unversioned (v1) deliveries pass --version v1 and
   the wrapper looks for `draft.md` + `qa-report.md`.
2. Reads the qa-report. Requires the verdict line to contain "PUBLISH".
   FAIL or HALT verdicts refuse delivery.
3. Renders the draft to docx via render-for-drive.py.
4. Uploads via drive_cli.py upload-as-gdoc.

Bypassing: do not. If you genuinely need an out-of-band delivery, write
the qa-report first.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path('/Users/onur/psfnetwork-pipeline')
PY = REPO / '.venv' / 'bin' / 'python3'
RENDER = REPO / 'workflow' / 'render-for-drive.py'
DRIVE_CLI = REPO / 'workflow' / 'drive_cli.py'

PUBLISH_RE = re.compile(r'(?:^|\W)(PUBLISH|publish)(?:\W|$)')
FAIL_VERDICT_RE = re.compile(r'(?:^|\W)(FAIL|HALT|REJECT|MANUAL-REVIEW-REQUIRED)(?:\W|$)')


def find_artifacts(slug, version):
    slug_dir = REPO / 'blog' / slug
    if not slug_dir.is_dir():
        sys.exit(f'ERROR: slug folder not found at {slug_dir}')

    if version == 'v1':
        draft = slug_dir / 'draft.md'
        qa = slug_dir / 'qa-report.md'
    else:
        draft = slug_dir / f'draft-{version}.md'
        qa = slug_dir / f'qa-report-{version}.md'

    missing = [str(p) for p in (draft, qa) if not p.exists()]
    if missing:
        sys.exit(
            f'ERROR: delivery refused. Missing required files:\n  ' +
            '\n  '.join(missing) +
            '\n\nStage 9 requires both a draft and a corresponding qa-report. '
            'Run Stage 7 before delivery.'
        )
    return draft, qa


def check_qa(qa_path):
    text = qa_path.read_text()

    # Support two formats for the verdict:
    # (a) Markdown header "## Recommendation\n\n<verdict>"
    # (b) Inline label "RECOMMENDATION: <verdict>"
    rec = None
    header_match = re.search(
        r'(?im)^##\s*Recommendation\s*\n+(.+?)$', text, flags=re.MULTILINE
    )
    if header_match:
        rec = header_match.group(1).strip()
    else:
        inline_match = re.search(r'(?im)^RECOMMENDATION:\s*(.+?)$', text)
        if inline_match:
            rec = inline_match.group(1).strip()

    summary_match = re.search(
        r'(?im)^##\s*Summary\s*\n(.+?)(?=^##|\Z)', text, flags=re.MULTILINE | re.DOTALL
    )

    if not rec:
        sys.exit(
            f'ERROR: delivery refused. {qa_path} has no "## Recommendation" '
            'header or "RECOMMENDATION:" line. Stage 7 requires an explicit verdict.'
        )
    if FAIL_VERDICT_RE.search(rec):
        sys.exit(
            f'ERROR: delivery refused. {qa_path} verdict is "{rec}". '
            'Only PUBLISH verdicts may proceed to Stage 9.'
        )
    if not PUBLISH_RE.search(rec):
        sys.exit(
            f'ERROR: delivery refused. {qa_path} verdict "{rec}" does not '
            'contain PUBLISH. Reject and re-run Stage 7.'
        )

    # Also scan summary for any 0-FAIL guarantee
    if summary_match:
        if re.search(r'\b[1-9]\d*\s+FAIL', summary_match.group(1)):
            sys.exit(
                f'ERROR: delivery refused. {qa_path} summary lists FAILs. '
                'Resolve them and re-run QA before delivery.'
            )

    return rec


def render_docx(draft_path):
    docx_path = Path('/tmp') / f'{draft_path.stem}.docx'
    result = subprocess.run(
        [str(PY), str(RENDER), str(draft_path), '--output', str(docx_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f'ERROR: render-for-drive failed:\n{result.stderr}')
    return docx_path


def upload(docx_path, folder_id, title):
    result = subprocess.run(
        [str(PY), str(DRIVE_CLI), 'upload-as-gdoc', str(docx_path), folder_id, title],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f'ERROR: upload failed:\n{result.stderr}')
    return json.loads(result.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', required=True)
    ap.add_argument('--version', required=True, help='e.g. v1 or v2-humanized')
    ap.add_argument('--folder-id', required=True)
    ap.add_argument('--title', required=True)
    args = ap.parse_args()

    draft, qa = find_artifacts(args.slug, args.version)
    verdict = check_qa(qa)
    print(f'QA gate: PASS ({verdict})', file=sys.stderr)

    docx = render_docx(draft)
    print(f'Rendered: {docx}', file=sys.stderr)

    result = upload(docx, args.folder_id, args.title)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
