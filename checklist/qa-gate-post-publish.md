# Post-publish QA Gate

Stage 9. Runs after the page is live. Items here require a live URL. Failures trigger remediation tasks rather than a pipeline restart.

## Checklist

### A. Live URL hygiene

- [ ] URL responds 200
- [ ] Canonical URL set correctly
- [ ] hreflang set correctly if multilingual
- [ ] Robots meta allows indexing
- [ ] OG and Twitter tags render in a social preview check

### B. Schema validation

- [ ] Article schema present and valid via Google Rich Results Test
- [ ] FAQ schema present and valid
- [ ] Breadcrumb schema present and valid
- [ ] All schema entities reference the canonical URL

### C. Performance

- [ ] Core Web Vitals: LCP, INP, CLS all in green per PageSpeed Insights (mobile and desktop)
- [ ] Mobile layout passes Google Mobile-Friendly Test

### D. AI citation test

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
