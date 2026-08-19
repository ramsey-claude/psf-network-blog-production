# The brain

Everything this operation knows, in one place you can search, with a machine
that keeps it honest.

The knowledge was always here. It was just spread across twenty checklists, a
349-line pipeline spec, a 238-line incident log, a roadmap, four brand files,
ten competitor notes, and 36 article folders. Nothing indexed it, so answering
"what did we decide about X" meant reading everything, and the cost of that is
already recorded in the incident log: rules get re-discovered mid-run instead of
read upfront.

## Two halves, and the difference matters

**Curated pages** hold knowledge with no other home. Someone wrote them by
hand, and when one is wrong it stays wrong until a person fixes it.

| Page | Holds |
|------|-------|
| [decisions.md](decisions.md) | Standing decisions, with the evidence behind each one |
| [canon/brand.md](canon/brand.md) | Brand law: name, voice, terminology, disclosure, personas |
| [canon/product.md](canon/product.md) | What PSFnetwork is, and what content may claim about it |
| [canon/compliance.md](canon/compliance.md) | Regulatory posture, sourcing rules, banned language |
| [canon/systems.md](canon/systems.md) | The machines: scripts, crons, credentials, CI, state |
| [canon/glossary.md](canon/glossary.md) | Every term this operation uses in its own particular way |
| [playbooks/](playbooks) | Runbooks for the jobs that recur |

**Generated registries** are rebuilt from the files that already own the facts.
They carry a banner, never take hand edits, and CI fails when they drift from
their sources.

| Registry | Source of truth |
|----------|-----------------|
| [index.md](index.md) | The repo itself, walked at build time |
| [rules.md](rules.md) | `workflow/incident-log.md`, Active rules section |
| [incidents.md](incidents.md) | `workflow/incident-log.md`, dated entries and open issues |
| [articles.md](articles.md) | `blog/*/pipeline-state.json` and each canonical draft |
| [topics.md](topics.md) | `ROADMAP.md` Step 2, matched against what shipped |

The direction of travel is one way. Fix the source, rebuild the brain. A fix
applied to a generated page is gone at the next build.

## Using it

```bash
python3 workflow/brain.py search "drive delivery gate"   # ranked recall, with file:line
python3 workflow/brain.py rules --category tooling       # what is in force right now
python3 workflow/brain.py rules --grep dash              # find the rule about a thing
python3 workflow/brain.py stats                          # what the brain holds
python3 workflow/brain.py build                          # rebuild the registries
python3 workflow/brain.py check                          # CI gate: index still matches repo
```

`make brain`, `make brain-check`, and `make brain-search Q="..."` wrap the same
commands.

## Rule ids and the enforcement claim

Every active rule gets an id derived from its category and label, such as
`R-tooling-charts`. Cite the id in reviews, commit messages, and code.

Any file can claim it enforces a rule by carrying a `brain-rule` marker naming
the id in a comment. The rules registry reads those claims back, so its
**Enforced by** column is a real answer to "does anything actually check this,
or are we relying on whoever runs the pipeline having read the log". Most rules
are still in the second group. `python3 workflow/brain.py stats` prints the
current split, and moving one rule out of it is always worth doing.

```python
AUTH_BROKEN_SENTINEL = SENTINEL_DIR / 'auth-broken-drive'  # brain-rule: R-auth-infrastructure-drive-token
```

## What keeps it honest

`python3 workflow/brain.py check` runs in CI on every push and fails on:

- a generated registry that no longer matches its source
- a rule id cited anywhere under `brain/` or in `CLAUDE.md` that does not exist
- a decision id cited outside the register that is not in it
- a relative link in any brain page pointing at a file that is not there
- a duplicate rule id, meaning two rules in the log share a label
- a curated page carrying a generated banner, or a generated page missing one

It warns, without failing, on a rule that nothing automated checks and on an
article folder with no draft in it.

## What the brain cannot tell you

It holds what the repo records. Where the repo is silent, the brain says so
rather than filling the gap: an unexplained revert stays marked unexplained, a
topic matched to an article by word overlap says exactly that, and a gap number
that no longer points where it used to is reported as stale instead of quietly
followed. Treat any line here as a pointer to its source, and open the source
before acting on something expensive.

## Updating

- A new rule, a new incident: edit `workflow/incident-log.md`, then rebuild.
- A new standing decision: add it to [decisions.md](decisions.md) with its date
  and evidence, and give it the next D number.
- A new fact about brand, product, compliance, or the machines: the matching
  `canon/` page, with a pointer to the file that proves it.
- A job you had to work out from scratch and will do again: a playbook.
- Stage 11 of every batch run rebuilds the registries and commits them, so the
  next run's Stage -4 reads a current brain. See
  [playbooks/add-a-rule.md](playbooks/add-a-rule.md).
