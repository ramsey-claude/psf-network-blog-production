# Playbook: producing an article

The full path from trigger to delivered document. The authoritative spec is
`workflow/pipeline.md`; this is the operator's view of it with the commands.

## Trigger

| Say this | Get this |
|----------|----------|
| `psf network için yeni blog yaz` | The pipeline picks the topic (Stage -1 runs) |
| `psf network için yeni blog yaz: [slug or topic]` | Your topic, Stage -1 skipped |
| `psf network [slug] devam et` | Resume from the stage in `pipeline-state.json` |

The trigger pre-authorizes every stage that follows. No approval prompts
between stages. What exactly it authorizes is in `workflow/trigger-contract.md`.

## The run

1. **Stage -4, pre-flight.** Read the active rules. Halt if the log is
   unreachable. `python3 workflow/brain.py rules` gives you the same set.
2. **Stages -3 to -1, only when needed.** Refill the topic pool, generate a
   brief and outline, select a slug. Skip whatever the trigger already answered.
3. **Stage 1, research.** SERP snapshot, cannibalization check against the repo,
   claim inventory, a primary source for every claim in `evidence.md`. No claim
   proceeds without a row.
4. **Stage 2, draft.** Preflight the brief first:
   ```bash
   make brief-preflight SLUG=[slug]
   ```
   Then write to the component order in `brand/template-structure.md`, with
   title at 55 to 60 characters and meta description at 150 to 160. Both are
   produced here, not retrofitted in QA. Rule: `R-content-quality-title`.
5. **Stage 2.5, humanization.** Six gated steps: ban-list sweep, all three human
   anchors in the body, rhythm rewrite, de-listification, second person
   throughout, specificity audit. The log has to record PASS on every step. A
   FAIL sends the draft back to Stage 2, three cycles maximum.
6. **Stage 3, panel.** SEC, FINRA, CFPB, Editorial, plus whoever the subject
   pulls in per [../canon/compliance.md](../canon/compliance.md). Moderator
   writes consensus. Three or more HIGH findings loops back to Stage 2.
7. **Stage 4, revision.** Apply every HIGH, most MED, judgment on LOW. Numbered
   changelog naming the reviewer behind each change. Revise sections, never
   delete them.
8. **Stages 5 and 6.** No-ops under the US-only posture (D-006), but they still
   write their artifacts.
9. **Stage 7, QA gate.** Work `checklist/qa-gate.md` A through E. Machine subset:
   ```bash
   python3 workflow/qa_battery.py [slug] --details
   python3 workflow/check-rules.py blog/[slug]/draft.md
   ```
   Section E wants zero blocking findings and zero grammar warnings. Route
   failures by type; do not restart from Stage 1 out of habit.
10. **Stage 8, publish.** Run the rule check over staged files, then commit
    every artifact. Never bypass the hook.
11. **Stage 9, delivery.** See [delivery.md](delivery.md).
12. **Stage 10, post-publish.** The cron picks it up once the URL is live.
13. **Stage 11, retrospective.** Once per batch, not per article. See
    [add-a-rule.md](add-a-rule.md).

## Halt conditions worth memorising

Loop count over three, a cannibalization conflict, an unsourceable claim with
no replacement, a missing incident log, an auth sentinel, a failed meta-QA. Each
one writes its state and stops rather than improvising.

## After the run

```bash
python3 workflow/brain.py build     # article registry and topic pool pick up the new slug
git add brain/ && git commit -m "chore(brain): rebuild after [slug]"
```
