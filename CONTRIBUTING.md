# Contributing

This repository is the PSFnetwork blog production pipeline. Most changes
come from the autonomous pipeline itself; human contributions happen at
the spec-and-rule level (checklists, brand voice, pipeline structure).

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the linter manually:

```bash
.venv/bin/python workflow/check-rules.py        # default scope
.venv/bin/python workflow/check-rules.py --staged  # only git-staged .md files
```

Run the test suite:

```bash
.venv/bin/pytest tests/
```

## Commit rules

Every commit that touches `.md` files is checked by `check-rules.py` via
`.github/workflows/lint-content.yml`. A commit cannot land on `main` with
any BLOCKING violation. See `checklist/ai-tells.md` for the rule set.

Commit messages follow conventional-commits style:

- `feat(scope):` new capability
- `fix(scope):` bug fix or violation cleanup
- `chore(scope):` housekeeping
- `docs(scope):` documentation only

Co-Authored-By trailer for AI-assisted commits is encouraged but not
required:

```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

## Workflow changes

Changes to `workflow/pipeline.md`, `checklist/qa-gate.md`, or
`checklist/ai-tells.md` are high-impact and should be reviewed against
the incident log (`workflow/incident-log.md`) before commit. Many
existing rules trace back to a specific past failure; do not relax a
rule without understanding the failure that produced it.

## Blog content changes

Blog drafts (`blog/[slug]/draft.md`, `draft-v2-humanized.md`) go through
the pipeline. Direct hand-edits to a draft are discouraged; prefer to
update the brief or the relevant checklist and re-run the pipeline.

## When in doubt

Read `README.md` for the high-level pipeline. Read `workflow/pipeline.md`
for the detailed stage-by-stage spec. Read `workflow/incident-log.md` for
the history of what has broken and why the current guardrails exist.
