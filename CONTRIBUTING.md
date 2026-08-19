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

## The brain

`brain/` indexes what this operation knows. Half of it is written by hand and
half is generated.

Generated files carry a banner naming the build command. Do not edit them:
change the source (`workflow/incident-log.md`, `ROADMAP.md`, an article's state
file), then rebuild and commit the result.

```bash
python3 workflow/brain.py build     # regenerate the registries
python3 workflow/brain.py check     # what CI runs; fails on drift
```

Curated pages take hand edits: `brain/decisions.md` for a standing decision,
`brain/canon/` for brand, product, compliance, systems, or vocabulary facts,
`brain/playbooks/` for a job you had to work out and will do again. Cite rules
by id (`R-content-quality-title`) and decisions by number (`D-014`); CI fails on
a citation that does not resolve.

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

Read `CLAUDE.md` first, then `brain/README.md`. Ask the brain before reading
everything: `python3 workflow/brain.py search "your question"` returns the file
and line that answers it. `README.md` has the high-level pipeline,
`workflow/pipeline.md` the stage-by-stage spec, and `workflow/incident-log.md`
the history of what has broken and why the current guardrails exist.
