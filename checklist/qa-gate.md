# QA Gate

Final pre-publication gate (Stage 5). If any item fails, the pipeline restarts from Stage 1.

---

## How to Use

Work through all items in order. Mark each as pass or fail. If any item is marked **fail**, stop, document the failure reason in the loop log, and restart the pipeline.

---

## QA Checklist

### A. Financial Accuracy

- [ ] All investment return claims include a risk disclosure
- [ ] No guaranteed return language anywhere in the content
- [ ] FDIC insurance limits stated correctly if referenced
- [ ] SEC, CFTC, FINRA, Fed references are factually accurate
- [ ] All statistics and data points are sourced
- [ ] No misleading comparisons between regulated and unregulated products

### B. SEO & GEO

- [ ] Title tag 55-60 characters, focus keyword in first third
- [ ] Meta description 150-160 characters, includes CTA and keyword
- [ ] H1 is unique and contains focus keyword
- [ ] H2s are in question format
- [ ] TL;DR / summary block present at top of content
- [ ] FAQ schema applied to H2 question-answer pairs
- [ ] Article schema complete (author, datePublished, headline)
- [ ] Canonical URL set
- [ ] At least 2 internal links to relevant pages
- [ ] All external links point to high-authority sources

### C. Technical

- [ ] All internal and external links tested — no broken links
- [ ] All images loading, alt texts populated
- [ ] Mobile layout tested — no formatting breaks
- [ ] Page speed tested (Core Web Vitals green)
- [ ] Schema markup passed Google Rich Results Test
- [ ] hreflang set if multilingual version exists

### D. Brand & Content Quality

- [ ] Brand name written as psfnetwork (all lowercase, one word) throughout
- [ ] Brand colors and typography consistent with brand guideline
- [ ] Tone matches psfnetwork brand voice (see `brand/tone-and-voice.md`)
- [ ] No contradictory statements within the content
- [ ] No orphaned sentences or incomplete paragraphs
- [ ] Author name and publication date visible on page

### E. Localization (if applicable)

- [ ] Financial terms not distorted by localization
- [ ] Register consistent throughout (siz / vous / formal)
- [ ] Local market references are accurate and current
- [ ] Currency formatting correct for target market

### F. GEO Final Check

- [ ] Content tested in Perplexity — brand/content cited correctly
- [ ] Content tested in ChatGPT — key facts extracted accurately
- [ ] Answer capsules (50-75 word H2 responses) are self-contained

---

## Failure Protocol

If any item fails:

1. Document the failure in `workflow/loop-log-template.md`
2. Identify which stage introduced the issue
3. Restart pipeline from **Stage 1** with the failure reason attached to the brief
4. Note: if the failure is isolated to localization (Section E), pipeline may restart from Stage 3 at the lead's discretion

---

## Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| SEO Lead | | | |
| Expert Panel Lead | | | |
| Localization | | | |
| Final approver | | | |
