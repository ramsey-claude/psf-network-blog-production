# Pipeline — Detailed Steps

Full decision tree for the psfnetwork blog production pipeline.

---

## Stage 1 — Expert Panel Discussion

**Input:** Draft blog post  
**Output:** Consolidated expert feedback + flagged issues list

1. Distribute draft to all 8 experts using `checklist/expert-review-template.md`
2. Each expert completes their domain checklist independently
3. Experts flag issues with severity: High / Med / Low
4. Panel consolidates feedback — conflicts between experts resolved by majority + domain authority
5. If 3 or more High severity issues found: content returns to writer for full rewrite before Stage 2
6. If fewer than 3 High issues: proceed to Stage 2 with revision notes

**Decision:**
- 3+ High issues → Back to writer (full rewrite)
- 0-2 High issues → Stage 2

---

## Stage 2 — Content Revision

**Input:** Draft + expert panel feedback  
**Output:** Revised draft + change log

1. Writer implements all required changes from Stage 1
2. Change log documents every flagged issue and how it was resolved
3. High severity fixes reviewed by the relevant expert before proceeding
4. Revised draft approved by SEO lead for keyword/GEO integrity

**Decision:**
- All High issues resolved + SEO lead approved → Stage 3
- Unresolved issues → Back to Stage 1

---

## Stage 3 — Localization Review

**Input:** Revised draft  
**Output:** Localized draft + localization change log

1. Localization specialist reviews using `checklist/localization-guide.md`
2. Market-specific language, tone, and references adjusted
3. Financial terms checked against the terminology rules in the localization guide
4. Localization change log completed — each change tagged with whether it triggers Stage 4 full review

**Decision:**
- No financial terms changed → Stage 4 targeted review
- Financial terms changed → Stage 4 full expert panel review
- No localization needed → Stage 5

---

## Stage 4 — Expert Re-check

**Input:** Localized draft + localization change log  
**Output:** Expert approval or revision request

1. Expert panel reviews localized content
2. Targeted review: only changed sections reviewed
3. Full review: all 8 experts re-run their domain checklists
4. If localization introduced new financial accuracy issues: content returns to Stage 2 (not Stage 1) with specific notes

**Decision:**
- No new issues → Stage 5
- New issues found → Stage 2 (with localization notes attached)

---

## Stage 5 — QA Gate

**Input:** Expert-approved localized draft  
**Output:** Published content or pipeline restart

1. QA reviewer works through `checklist/qa-gate.md` in full
2. Any single fail triggers a pipeline restart
3. Failure reason documented in `workflow/loop-log-template.md`
4. Restart goes to Stage 1 with failure context

**Decision:**
- All items pass → Publish
- Any item fails → Stage 1 (restart)

---

## Pipeline Diagram

```
DRAFT
  |
  v
[Stage 1] Expert Panel Discussion
  |-- 3+ High issues --> Writer (rewrite) --> Stage 1
  |
  v
[Stage 2] Content Revision
  |-- Unresolved issues --> Stage 1
  |
  v
[Stage 3] Localization Review
  |-- No localization needed --> Stage 5
  |
  v
[Stage 4] Expert Re-check
  |-- New issues found --> Stage 2
  |
  v
[Stage 5] QA Gate
  |-- Any fail --> Stage 1 (with failure log)
  |
  v
PUBLISHED
```
