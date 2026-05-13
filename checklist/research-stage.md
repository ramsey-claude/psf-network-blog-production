# Stage 1 - Research Checklist

Stage 1 produces the evidence base for the draft. Nothing enters Stage 2 unless it appears in `evidence.md`.

## Tooling

Stage 1 uses only the built-in `WebSearch` and `WebFetch` tools. No paid SERP API (Semrush, SerpAPI, etc.) is invoked from the pipeline. Rationale: keep token cost on Anthropic side only and avoid burning external API quota during high-volume runs.

- `WebSearch` for keyword and question discovery (returns a result list)
- `WebFetch` for full-page reads of primary sources, competitor pages, and federal agency docs

GSC-based cannibalization is **deferred** until psfnetwork has 100 or more posts published. The site is not live yet; there is no useful GSC data to query. Until that threshold, cannibalization is a repo scan only.

## Sub-tasks

### 1. SERP snapshot

Capture current state of search for the focus keyword.

- [ ] Top 10 organic results (URL, title, snippet) - via `WebSearch` on the focus keyword
- [ ] People Also Ask approximation - run `WebSearch` on the 3 most likely question variants ("what is X", "how does X work", "is X a good Y") and record top results
- [ ] AI Overview text if surfaced by `WebSearch` results, copied verbatim
- [ ] Featured snippet if any result clearly carries one (best-effort, may not be reliably detectable through `WebSearch`)
- [ ] Related searches - best-effort from `WebSearch` output

Limitations: `WebSearch` returns a result list, not the rich Google SERP HTML. People Also Ask, AI Overview, and featured snippet detection are best-effort. Mark each as `[best-effort]` or `[not detected]` rather than fabricating.

**Output:** `serp-snapshot.md`

### 2. Cannibalization check (repo-only until 100 posts)

- [ ] Search `blog/` for any existing post targeting the same focus keyword
- [ ] Search for any existing post with overlapping secondary keywords (>50% overlap on the brief's keyword table)
- [ ] If a conflict exists: write `cannibalization-conflict.md` with the conflict details, halt pipeline

When the published-post count reaches 100, this section gains a GSC step: query the GSC API for the focus keyword and check whether an existing live URL already ranks. Until then, repo scan is sufficient because there is no live ranking signal to conflict with.

### 3. Claim inventory

List every claim in `outline.md` that needs a source. Categories:

- Numerical claims (rates, returns, AUM figures, minimums, dates)
- Regulatory claims (what an agency does, requires, allows)
- Comparative claims ("Platform A is X compared to Platform B")
- Historical claims (when something happened, what the law said)
- Named-entity claims (platform exists, person holds title)

**Output:** `claim-inventory.md`

### 4. Source verification

For each claim, find a primary source. Each entry becomes a row in `evidence.md`.

**Acceptable primary sources:**

- US federal agency sites: sec.gov, irs.gov, frb.gov, occ.gov, fdic.gov, finra.org, cfpb.gov, cftc.gov, treasury.gov
- SEC EDGAR filings (offering circulars, 10-Ks, Form D, Form 1-A)
- Government statistical bureaus (BLS, Census, Federal Reserve data releases)
- Peer-reviewed research (with DOI)
- Official platform disclosures (offering documents, audited financials)
- Court decisions, statutes, regulations
- National statistical agencies of target markets (TUIK for TR, DLD for UAE, INSEE for FR)

**Not acceptable as primary source:**

- Other blogs, content marketing sites
- LLM-generated summaries
- Wikipedia (acceptable as a pointer to the primary source only, never the citation itself)
- Press releases without supporting filings or data

**`evidence.md` row schema:**

| Field | Required |
|-------|----------|
| Claim | Yes |
| Source URL | Yes |
| Source publisher | Yes |
| Source date | Yes |
| Exact quote or data point | Yes |
| Accessed date | Yes |
| Confidence (high / medium / low) | Yes |

### 5. Outline reconciliation

- [ ] Every claim has an `evidence.md` row, OR has been removed from `outline.md`
- [ ] Removed or replaced claims are noted in `evidence.md` under "reconciliation notes"

## Gate

Stage 1 is complete when:

- `evidence.md` exists and covers every sourceable claim in `outline.md`
- `serp-snapshot.md` exists
- No cannibalization conflict
- `claim-inventory.md` exists

If any of these are missing, Stage 1 is not complete and Stage 2 must not start.

## Failure modes

| Failure | Action |
|---------|--------|
| A claim cannot be sourced and has no acceptable replacement | Remove it from outline. If removal breaks a section, flag and halt with `unsourceable-claim`. |
| Cannibalization conflict | Halt with `cannibalization-conflict.md`. |
| SERP fetch fails | Retry once. If still failing, proceed with a manual note and flag in state. |
