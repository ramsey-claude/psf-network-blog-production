# Playbook: teaching the system something

A lesson that stays in one person's head is not learned. This is how something
the operation discovered becomes something it cannot forget.

## 1. Write the incident, not just the fix

New entry at the top of the incident history in `workflow/incident-log.md`,
using the template at the top of that file. Every field earns its place:

- **Symptom** is what the operator or customer actually saw, in their words.
- **Root cause** is what was broken, not what you changed. The 2026-08-11 entry
  lists four causes in order of depth, and only the deepest one produced the
  standing rule.
- **Fix** is what changed in this incident.
- **Rule** is the sentence that outlives it, or the honest "no new rule,
  one-off".
- **Tests** is the regression test, if there is one.

## 2. Promote it, if it is permanent

A rule that applies to every future run goes into the Active rules section
under its category: Tooling, Auth and infrastructure, Content quality, or
Process. Rule ids are derived from category and label, so the label is the
name the rest of the system will use. Keep it short and unique. Two rules
sharing a label collide their ids and fail `brain.py check`.

State the scope in the same line: all content, or batch N onward. A scoped rule
leaves debt behind, and that debt goes into `workflow/qa-baseline.txt` the same
day rather than waiting to be discovered (D-013).

## 3. Give it a machine, if you can

A rule nobody checks depends on the next person having read this page. Where
the rule is mechanical, add a check:

- A content pattern belongs in `check-rules.py` BLOCKING or WARNING.
- An article-level check belongs in `qa_battery.py`, as a FAIL or a WARN.
- A structural or behavioural rule belongs in a test under `tests/`.

Then claim it, so the registry can report the rule as enforced:

```python
AUTH_BROKEN_SENTINEL = SENTINEL_DIR / 'auth-broken-drive'  # brain-rule: R-auth-infrastructure-drive-token
```

`python3 workflow/brain.py stats` prints how many rules currently have a check
and how many do not. Most do not. Each one you convert is one fewer thing that
depends on somebody remembering.

## 4. Rebuild and commit

```bash
python3 workflow/brain.py build
python3 workflow/brain.py check
make lint && make test
```

Stage 11 does this once per batch and commits the result, so the next run's
Stage -4 reads current rules. A rule added without a rebuild is a rule the next
session's brain does not list.

## 5. Decide whether it is also a decision

Rules say what to do. Decisions say what was chosen and why, and they outlive
the rule that implements them. If someone six months from now would ask "why do
we do it this way", it belongs in [../decisions.md](../decisions.md) with the
next D number and the evidence behind it.
