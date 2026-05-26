# Security policy

## Reporting a vulnerability

If you discover a security issue in this repository (leaked credentials,
exploitable script behavior, auth bypass in the delivery pipeline, etc.),
do not open a public issue. Email the operator directly and wait for
acknowledgment before any disclosure.

## What is in scope

- Anything under `workflow/` (delivery, drive, render, check-rules scripts)
- `.github/workflows/` (CI configurations)
- The git history and committed contents

## What is out of scope

- The Drive folders themselves (managed by the operator's Google account
  permissions, not by this repo)
- The Railway / external infrastructure that hosts the live psfnetwork site
- Third-party platform pages referenced from blog drafts

## Known sensitive paths

These paths must NEVER be committed to the repo:

- `/Users/onur/.psfnetwork-drive/token.json` (Drive OAuth refresh token)
- `/Users/onur/.psfnetwork-drive/github-token` (PAT for git/API operations)
- Any `ghp_…`, `ya29.…`, or `client_secret_*` value

If any of the above appears in a diff: revert immediately, rotate the
credential, and add an incident-log entry. The 2026-05-14 entry in
`workflow/incident-log.md` documents the canonical recovery procedure
for a leaked GitHub token.

## Secret-scanning

A future CI step will run gitleaks on every push. Until that lands,
operators must visually verify diffs before pushing.

## Token rotation

GitHub PATs rotate per `workflow/rotate-github-token.sh`. Drive tokens
auto-refresh per `workflow/drive_cli.py get_service()` and write a
sentinel at `/Users/onur/.psfnetwork-drive/auth-broken-drive` on refresh
failure. The sentinel is picked up by the next pipeline run, which halts
with `auth-broken-drive` rather than running blind.
