# Customer Feedback Intake

How customer-reported issues enter the pipeline and which stage they trigger. Added 2026-05-26 after a customer review surfaced grammar and mobile formatting issues on a Stage-7-cleared v2 document, with no documented path for what should happen next.

## When this applies

- Operator (Onur) receives feedback from the psfnetwork team that references a specific delivered article or a category of issues across articles.
- Internal review surfaces an issue on a published or delivered article (live URL or Drive Doc).
- Auto-monitoring (Stage 10) flags a regression.

Out of scope: brand-new topic requests, content-strategy questions, brief generation for new posts. Those go through Stage -2.

## Intake protocol

1. **Capture verbatim.** Paste the feedback into a new entry in `workflow/incident-log.md`. Format: see "Incident-log entry template" at the top of that file.

2. **Classify.** One of:
   - **Content quality** (humanization, grammar, voice, factual)
   - **Formatting** (mobile, render, schema, image)
   - **Compliance** (regulatory phrasing, disclaimer drift, link validity)
   - **Process** (pipeline let something through that should have failed)

3. **Route to the right stage:**

   | Classification | Route to | Output |
   |----------------|----------|--------|
   | Content quality (voice/humanization) | Stage 2.5 re-run on the slug, then Stages 3, 4, 7, 9 | new `draft-vN+1-humanized.md` + new `qa-report-vN+1.md` + new Drive doc |
   | Content quality (factual) | Stage 1 re-run for the affected claim, then Stage 4 | updated `evidence.md` + revised draft |
   | Formatting | Stage 4 (Revision) targeted, then Stage 7 QA | revised draft + qa-report-vN |
   | Compliance | Stage 3 single-reviewer re-touch, then Stage 4 | updated `expert-reviews/` + revised draft |
   | Process | Stage 11 incident handling + checklist/spec update | incident-log entry + checklist update |

4. **Bound the work.** Set an explicit version label (v2, v3) for the customer-visible artifact before starting. The version label is the contract: when the customer asks "is this fixed yet" the operator points to the version number.

5. **Close the loop.** When the fix delivers, reply to the customer with:
   - The new Drive doc link
   - A one-line summary of what changed
   - A pointer to the relevant audit trail file in the repo (e.g., `draft-v2-humanization-log.md`)

## "We did not have time to read it yet" feedback

If the customer says "I have not looked at all articles yet but the first one has issues," do not extrapolate to all articles. Wait for them to call out each one. The intake protocol applies per article, not per batch.

## "This is not humanized" feedback

This is the most common shape after 2026-05-26. Verify which version they reviewed. If it was a v1 (pre-humanization), the response is "you reviewed the pre-humanized version, here is the humanized one." If it was a v2 (humanized), audit the humanization log for which steps PASSED, then re-run the failing steps.

## What never goes through this intake

- Trivial typos the operator can fix in one edit and re-deliver. These get a one-line incident-log note and a direct Stage 9 redelivery.
- Em-dashes or other check-rules.py-detectable items. Those should have been caught by CI; investigate the rule, not the article.
- Anything that requires legal counsel. That escalates to the operator's legal contact, not into this pipeline.
