# Working in this repository

PSFnetwork's blog production pipeline: research, drafting, humanization,
regulatory review, QA, publish, delivery, and the retrospective that feeds the
next run. Most changes here come from the pipeline itself. Human and agent
changes happen at the spec and rule level.

## Before you touch anything

```bash
python3 workflow/brain.py rules     # every rule in force, and why
python3 workflow/brain.py check     # is the operation's index current
```

The rules are not style preferences. Each one is the residue of a specific
failure, and the incident behind it is one command away
(`python3 workflow/brain.py search "<the rule>"`). Do not relax one without
reading what it cost. For an autonomous pipeline run this read is Stage -4 and
it is mandatory: the run halts rather than proceed without current rules.

## The four things that fail a commit

1. An em dash or an en dash, anywhere in a markdown file.
2. The word for a promised return, in any form, including negations and
   quotations. <!-- check-rules: allow -->
3. Any spelling of the brand other than PSFnetwork.
4. A brain index that no longer matches the repo it describes.

Lines that document a banned pattern on purpose carry
`<!-- check-rules: allow -->`. Use it for a ban list or an avoid column, never
to get prose past the linter.

## Where knowledge lives

| Question | Read |
|----------|------|
| What are the rules, and does anything check them | `brain/rules.md` |
| Why does it work this way | `brain/decisions.md` |
| What has gone wrong before | `brain/incidents.md` |
| How do I do this specific job | `brain/playbooks/` |
| Brand, product, compliance, machines, terms | `brain/canon/` |
| What has been published, and what is in flight | `brain/articles.md` |
| What is left to write | `brain/topics.md` |
| How the pipeline works, stage by stage | `workflow/pipeline.md` |
| What a trigger authorizes | `workflow/trigger-contract.md` |

Start at `brain/README.md`. It explains which of those pages a person maintains
and which the build regenerates.

## Commands

```bash
make setup                                  # venv from pinned requirements
make lint                                   # brand voice, punctuation, grammar
make test                                   # pytest
python3 workflow/qa_battery.py              # content battery, every article
python3 workflow/brain.py build             # rebuild the brain after a source change
python3 workflow/brain.py search "query"    # recall, with file and line
make status                                 # lint, slug stages, humanization status
```

Run `make lint && make test && python3 workflow/qa_battery.py && python3
workflow/brain.py check` before pushing. Those are the four CI jobs.

## Conventions

- Conventional commits: `feat(scope):`, `fix(scope):`, `chore(scope):`,
  `docs(scope):`.
- Source files own the facts. `brain/` files carrying a generated banner are
  rebuilt from those sources, so edit the source and run the build.
- Rules are cited by id (`R-content-quality-title`), decisions by number
  (`D-014`). Both are checked; a citation that does not resolve fails CI.
- Credentials live outside the repo. Never commit a token, never print one into
  an artifact or a log.
- Do not hand-edit a published draft to fix a systemic problem. Fix the brief or
  the checklist and re-run the stage.
- Do not bypass the pre-commit rule check.

## Autonomous runs

A trigger pre-authorizes every stage that follows, with no approval prompts
between them. A permission prompt is recovered from, not escalated: rewrite the
call first, narrow the allowlist second, never broaden it, and log what
happened. The stop conditions that do halt a run are listed in
`workflow/trigger-contract.md`, and every one of them writes its state first.

Stage 11 closes the loop at the end of a batch: retrospective, new incidents
into the log, `brain.py build`, commit. Skipping it breaks the learning loop for
the next run.
