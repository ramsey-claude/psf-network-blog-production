# Playbook: CI is red

Four jobs run on every push. Each one fails for a different reason and wants a
different fix.

## check-rules: brand voice and punctuation

```
[BLOCK] path/file.md:42 em-dash: 'literal em-dash character'
```

A blocking pattern in a markdown file. Four of them exist: em dash, en dash,
the word for a promised return in any form, and any spelling of the brand other
than PSFnetwork. <!-- check-rules: allow -->

Fix the prose. Do not add the pragma to make it pass unless the line genuinely
documents the banned pattern on purpose, which is true for the ban list itself
and for use-and-avoid tables:

```markdown
| target return | never the banned word | <!-- check-rules: allow -->
```

Reproduce locally with `make lint`, or against one file:

```bash
python3 workflow/check-rules.py path/to/file.md
```

In pull requests the job only reads changed files. That is deliberate and it is
also how legacy violations once stayed hidden, which is why the next job exists.

## qa-battery: content checks across every article

```bash
python3 workflow/qa_battery.py --details
python3 workflow/qa_battery.py [slug] --details
```

FAIL findings are blocking: dashes, the banned word, production labels leaked
into the body, a missing or wrong-length meta description, Google Docs CSS
residue, a missing or wrong-length title. WARN findings are reported and do not
fail.

Known legacy debt lives in `workflow/qa-baseline.txt` and is tolerated. The
baseline is remove-only: when a backfill fixes an article, delete its line.
Never add a line for content authored after its rule existed (D-013).

## tests: pytest

```bash
make test
python3 -m pytest tests/test_brain.py -v
```

Every test pins a rule that cost something to learn. A failing test is a
regression, not an obstacle to route around.

## brain: index drift

```
[FAIL] brain/rules.md has drifted from its sources. Run: python3 workflow/brain.py build
```

Almost always means the incident log, the roadmap, or an article changed and
nobody rebuilt. Fix:

```bash
python3 workflow/brain.py build
git add brain/ && git commit -m "chore(brain): rebuild"
```

Other failures from this job:

- A rule id cited in a brain page that no longer exists, usually because a rule
  label was renamed in the incident log. Update the citation, or restore the
  label.
- A relative link pointing at a file that moved or was deleted.
- Two rules in the log sharing a label, which collides their ids. Rename one.

## Before pushing

```bash
make lint && make test && python3 workflow/qa_battery.py && python3 workflow/brain.py check
```

Four commands, the same four jobs, no surprises.
