# Systems canon

The machines this operation runs on: what each one does, what it needs, and how
it fails. Paths below are the operator's macOS machine, which is where the
pipeline runs.

## Scripts

| Script | Job | Notes |
|--------|-----|-------|
| `workflow/brain.py` | Index and recall over everything the operation knows | `build`, `check`, `search`, `rules`, `stats` |
| `workflow/check-rules.py` | Brand voice, punctuation, and grammar linting | Runs pre-commit in Stage 8, in CI on every push, and optionally as a local hook |
| `workflow/qa_battery.py` | Full content battery over every canonical draft | Seven FAIL checks, seven WARN checks, shares field parsing with the paste kit |
| `workflow/brief_preflight.py` | Blocks Stage 2 until the brief has its required sections | Exit 1 means the brief is missing something, usually a Human Anchor |
| `workflow/make_paste_kit.py` | Turns a draft into the operator's paste-ready package | Owns `split_notes`, `parse_notes`, and the field aliases everything else imports |
| `workflow/render-for-drive.py` | Draft to styled .docx via pandoc | Prepends the Production Notes block |
| `workflow/deliver.py` | Stage 9 delivery with the QA gate enforced | Refuses to upload without a PUBLISH qa-report that lists no FAILs |
| `workflow/drive_cli.py` | Drive REST operations: list, delete, upload-as-gdoc | Writes the drive auth sentinel on refresh failure |
| `workflow/drive_auth.py` | One-shot interactive OAuth to mint the Drive token | Run by hand, once |
| `workflow/stage10_runner.py` | Post-publish QA against the live URL | Idempotent, retries transient failures, writes the github auth sentinel on 401 |
| `workflow/token_expiry_check.py` | Daily token probe | See D-005 for why its warning path cannot currently fire |
| `workflow/render_visual.py` | Article visual to PNG and WebP under a size budget | Shared styling in `workflow/visual-base.css` |
| `workflow/rotate-github-token.sh` | Operator path to clear a broken GitHub credential | Clears the sentinel |
| `push.sh` | Commit and push helper | Reads the token from its file, never from source |

## Schedules

Two launchd jobs, both installed under `~/Library/LaunchAgents/`.

| Job | Plist | When |
|-----|-------|------|
| Post-publish QA | `com.psfnetwork.stage10.plist` | 03:13, 09:13, 15:13, 21:13 local |
| Token check | `com.psfnetwork.token-check.plist` | 09:07 daily, ahead of the first Stage 10 |

## Credentials and sentinels

Credentials live outside the repo (D-002). Never commit a token value, and
never print one into a log or an artifact.

| Path | Holds |
|------|-------|
| `/Users/onur/.psfnetwork-drive/github-token` | GitHub PAT, read by push.sh, stage10_runner, token check |
| `/Users/onur/.psfnetwork-drive/token.json` | Drive OAuth token, auto-refreshing |
| `/Users/onur/.psfnetwork-drive/auth-broken-github` | Sentinel. Present means halt anything needing GitHub |
| `/Users/onur/.psfnetwork-drive/auth-broken-drive` | Sentinel. Present means halt anything needing Drive |
| `/Users/onur/.psfnetwork-drive/token-warning-github` | Advisory, expiry approaching |

A sentinel present at run start halts the run with `auth-broken` and its
reason. The operator clears it with `workflow/rotate-github-token.sh` or
`workflow/drive_auth.py`. Rule: `R-auth-infrastructure-auth-sentinels`.

## Continuous integration

`.github/workflows/lint-content.yml` runs four jobs on every push and pull
request to main:

1. **check-rules** against changed files, or the default scope when there is no
   diff base. Blocking violations fail the build.
2. **qa-battery** across every article, because diff-mode linting only sees
   touched files and that is how legacy violations stayed dormant until a human
   found them (D-013).
3. **tests**, the pytest suite.
4. **brain**, `brain.py check`, which fails when the indexes no longer match the
   repo they describe.

## State

| File | Holds |
|------|-------|
| `blog/[slug]/pipeline-state.json` | Stage, completed and pending steps, loop count, panel, flags, evidence and QA summaries |
| `workflow/incident-log.md` | Active rules and every incident behind them |
| `workflow/qa-baseline.txt` | Known legacy content debt, remove-only ratchet |
| `workflow/visuals-tracker.md` | One row per article visual, produced and placed |
| `brain/*.md` | The generated indexes over all of the above |

Twelve of the 36 article folders carry a state file. The rest were produced by
the earlier system and synced in, so their status has to be read from the
artifacts on disk. [../articles.md](../articles.md) marks which is which.

## Delivery target

```
My Drive/
└── psfnetwork/
    └── [slug]/
        └── [Title]        native Google Doc, one per slug
```

Stage 9 deletes what is in the slug folder before uploading, so a re-run leaves
one clean document rather than a pile of versions. Batch 3 delivery flattened
the layout into a month root, per the July run.

## Local setup

```bash
make setup     # venv from pinned requirements
make lint      # brand voice and punctuation over the default scope
make test      # pytest
make brain     # rebuild the brain
make status    # lint, article stages, humanization status
```

`brain.py` itself needs nothing but the standard library, which is why the CI
job can run it without installing dependencies.
