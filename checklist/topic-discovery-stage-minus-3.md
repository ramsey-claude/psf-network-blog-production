# Stage -3 - Auto Gap Discovery (Topic Pool Refresh)

Runs only when Stage -2 reports `topic-generation-exhausted` (the ROADMAP Step 2 gap pool has fewer than 3 unused items). Stage -3 auto-discovers new gap candidates by scanning competitor content and SERP, then appends them to ROADMAP Step 2. After Stage -3 runs, Stage -2 has fresh pool to draw from and the batch resumes.

Stage -3 is the final fallback before halting. If Stage -3 itself returns `discovery-failed`, the batch halts and the operator must seed the pool manually.

## Inputs

- Current `ROADMAP.md` Step 2 pool (to avoid re-discovering already-listed gaps).
- Competitor list from `ROADMAP.md` Step 1 (Ark7, Arrived, Fundrise, Mogul, Realbricks, Lofty, Groundfloor, plus any others added).
- All existing `blog/*/brief.md` keyword tables (to avoid re-discovering already-covered topics).
- Operating scope: US-only audience, English-only content.

## Sub-steps

### 1. Competitor blog scan

For each competitor in Step 1, list their published blog URLs (via WebFetch on the blog index or sitemap). Collect titles and lead keywords.

Output: `discovery-scan.md` listing per-competitor article inventory.

### 2. Gap identification

For each competitor article, check whether PSFnetwork has covered the topic:
- If focus keyword is the focus of an existing brief: covered. Skip.
- If overlapping but distinct angle exists: weak gap.
- If not covered at all: strong gap. Add to candidate pool.

For each candidate, write:
- Topic title
- Why it's a gap (which competitor owns it, traffic estimate if available)
- Estimated KD and Volume (from SERP signals or "TBD")
- US-only fit check

### 3. SERP-based keyword expansion

WebSearch each strong gap candidate's primary keyword + the cluster's anchor terms ("fractional real estate", "real estate investing", "REIT") and capture related questions / "People Also Ask" patterns. Each surfaced question is a candidate sub-topic.

### 4. Filter and rank

Apply the same filters as Stage -2:
- US-only scope.
- No cannibalization with existing briefs (2+ keyword overlap).
- Brand fit (does PSFnetwork's per-square-foot or fractional angle naturally appear).

Rank by: KD / Volume score, brand fit, novelty (not already in ROADMAP pool).

### 5. Append to ROADMAP

For the top N (default 10) candidates, append to ROADMAP Step 2 with the row schema. Commit the updated ROADMAP.

Commit message: `feat(roadmap): Stage -3 auto-discovery added N gap candidates`.

### 6. Loop back to Stage -2

After ROADMAP is updated, Stage -2 has fresh seeds. Continue the batch.

## Halt conditions

- `discovery-failed`: Stage -3 could not surface any new candidates after a full competitor scan. Operator must seed Step 2 manually (e.g., from external keyword research).
- `competitor-fetch-failed`: too many competitor blogs failed to fetch (network, anti-bot). Operator intervention needed.

## Why this exists

Stage -2 can only pick from existing ROADMAP gaps. Without auto-discovery, a long batch run (50+ blogs) would exhaust the manual seed pool. Stage -3 makes the pool self-replenishing within the SERP signals the operator has already implicitly chosen by tracking competitors in ROADMAP Step 1.

## What Stage -3 does NOT do

- Invent topics outside the competitor frame (no random topic generation).
- Bypass cannibalization or US-only filters.
- Modify ROADMAP Step 1 (competitor list) - that is operator-curated.
- Author brief.md or outline.md - those are Stage -2's job.
