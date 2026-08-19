# Playbook: starting a session

For a person or a Claude session picking this repo up cold. Five minutes here
saves a run.

## 1. Load the rules

```bash
python3 workflow/brain.py rules
```

Twenty rules, each one the residue of something that broke. This is the same
content Stage -4 requires you to read from `workflow/incident-log.md`, indexed.
Reading it is not optional before an autonomous run: the trigger contract halts
the run if the log is unreachable, for the same reason.

## 2. Check the brain is current

```bash
python3 workflow/brain.py check
```

Failures mean an index no longer matches its source, usually because the
incident log or an article changed without a rebuild. Fix with
`python3 workflow/brain.py build` and commit the result.

## 3. See where the work is

```bash
make list-blog                        # every slug and its stage
python3 workflow/brain.py stats       # rules, incidents, articles, topics
```

Open questions live in [../incidents.md](../incidents.md) under open issues,
and unmatched gap topics in [../topics.md](../topics.md).

## 4. Find what you need

```bash
python3 workflow/brain.py search "answer capsule length"
python3 workflow/brain.py search "drive token refresh" --scope code
python3 workflow/brain.py rules --grep dash
```

Search returns file and line. Open the source before acting on anything
expensive; the brain is an index, not an authority.

## 5. Know the four things that will fail your commit

1. An em dash or en dash anywhere in a markdown file.
2. The word that means a promised return, in any form. <!-- check-rules: allow -->
3. Any spelling of the brand other than PSFnetwork.
4. A stale brain index.

Run `make lint && make test && python3 workflow/brain.py check` before you push
and none of them will surprise you.

## What not to do

- Do not hand-edit a file under `brain/` that carries a generated banner.
- Do not relax a rule without reading the incident behind it. Every one of them
  cost something.
- Do not hand-edit a published draft to fix a systemic problem. Fix the brief or
  the checklist and re-run the stage, per `CONTRIBUTING.md`.
