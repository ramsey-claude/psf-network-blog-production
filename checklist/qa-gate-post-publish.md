# Post-publish QA Gate

Stage 10. Runs after the page is live on psfnetwork.com. Failures trigger remediation tasks rather than a pipeline restart.

## Execution model

A launchd cron (`workflow/com.psfnetwork.stage10.plist`) runs `workflow/stage10_runner.py` daily at 09:13 local. The runner is idempotent and standalone (no Claude session needed):

- Reads each published `pipeline-state.json` from the repo.
- For each, fetches the live URL. 404 = defer (next day retries). 200 = run automated checks below.
- Writes `post-publish-report.md` and updates `pipeline-state.json`.
- Pushes both as a single commit (`chore(stage10): post-publish QA for [slug] - auto-runner`).

Automated check coverage and manual items are split below:

## Checklist

### A. Live URL hygiene (automated by runner)

- [x] URL responds 200 - automated
- [x] Canonical URL set correctly and matches expected - automated
- [x] Title tag present, 50-65 chars - automated
- [x] Meta description present, 140-170 chars - automated
- [ ] hreflang set correctly if multilingual - manual (single-locale today)
- [ ] Robots meta allows indexing - manual
- [ ] OG and Twitter tags render in a social preview check - manual

### B. Schema validation (automated by runner)

- [x] Article / BlogPosting / NewsArticle schema present (JSON-LD) - automated
- [x] FAQ schema present (FAQPage type) - automated
- [x] Breadcrumb schema present (BreadcrumbList type) - automated
- [ ] Schema validates against Google Rich Results Test - manual (until a Rich Results API is wired in)

### C. Performance (manual - not automated)

- [ ] Core Web Vitals: LCP, INP, CLS green per PageSpeed Insights (mobile + desktop)
- [ ] Mobile layout passes Google Mobile-Friendly Test

To automate: add a PageSpeed Insights API call to the runner (requires API key).

### D. AI citation test (manual - not automated)

For each query, record whether the post is cited, the cited passage, and the position in the answer.

- [ ] Focus keyword in Perplexity
- [ ] Focus keyword in ChatGPT (with web)
- [ ] Top 2 People Also Ask questions (from `serp-snapshot.md`) in Perplexity
- [ ] Top 2 People Also Ask questions in ChatGPT
- [ ] Google AI Overview check for the focus keyword (if AI Overview shows)

### E. Indexing

- [ ] Submit the URL to Google Search Console for indexing
- [ ] Confirm URL appears in `site:` search within 14 days (logged as follow-up task)

## Outputs

`post-publish-report.md` with:

- Per-item PASS/FAIL
- Citation transcripts for section D (the actual answers returned, copied verbatim)
- Performance scores and metrics
- Remediation list - one row per failed item with proposed fix and owner

## Remediation, not restart

Post-publish failures do not loop the production pipeline. They generate targeted fix tasks:

| Failure type | Remediation |
|--------------|-------------|
| Schema invalid | Fix template, redeploy, re-test |
| Core Web Vitals fail | Performance ticket against the Railway template |
| AI not citing | Revise answer capsules in a follow-up content edit, push as an update commit |
| Not indexed after 14 days | Investigate indexing signals, re-submit, check for noindex or canonical mismatches |
| Broken canonical or hreflang | Fix template, redeploy |

The slug's `pipeline-state.json` is updated with a `post_publish` block recording each test, but `stage` remains `published`.
