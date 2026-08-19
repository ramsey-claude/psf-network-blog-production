# Playbook: customer feedback

Feedback about a delivered article has one path in and one path out. Spec:
`checklist/customer-feedback-intake.md`. This exists because a customer once
found grammar and formatting problems in a document Stage 7 had cleared, and
nothing said what should happen next (D-009).

## In scope

Feedback from the PSFnetwork team about a specific article or a pattern across
articles, an internal review finding, or a Stage 10 regression. New topic
requests are not feedback; those go to Stage -2.

## The five steps

1. **Capture verbatim.** New entry in `workflow/incident-log.md`, using the
   template at the top of that file, classified `customer-feedback`. Paste the
   words as written. Do not summarise a complaint into something more
   comfortable.
2. **Classify** as content quality, formatting, compliance, or process.
3. **Route:**

   | Class | Route | Output |
   |-------|-------|--------|
   | Content quality, voice | Stage 2.5 re-run, then 3, 4, 7, 9 | new humanized draft, new QA report, new Drive doc |
   | Content quality, factual | Stage 1 for the claim, then Stage 4 | updated evidence, revised draft |
   | Formatting | Stage 4 targeted, then Stage 7 | revised draft, QA report |
   | Compliance | Stage 3 single reviewer, then Stage 4 | updated review file, revised draft |
   | Process | Stage 11 handling, checklist or spec update | incident entry, updated checklist |

4. **Bound it with a version label** (v2, v3) before starting. The label is the
   contract: when the customer asks whether it is fixed, the answer is a
   version number.
5. **Close the loop.** Reply with the new document link, one line on what
   changed, and a pointer to the audit trail file in the repo.

## Sweep, do not spot-check

The 2026-08-11 round found two unresolved comments only because someone swept
every folder in the batch. When a comment surfaces on one article, check the
others in its batch before declaring the round closed.

## Then rebuild the brain

A feedback entry changes the incident log, which changes two registries:

```bash
python3 workflow/brain.py build
```

If the entry produced a standing decision, add it to
[../decisions.md](../decisions.md) with the next D number and the evidence.
D-014 is the model: a customer comment, a positioning fix, and a rule about
wording that outlives the article it came from.
