# Batch 2 Audit: 15 Articles vs the Current QA Standard

Date: 2026-08-11
Method: deterministic checks over all 15 Batch 2 drafts (Production Notes format, FIXED v2 conventions: no Conclusion H2, body before FAQ, no standalone disclaimer block). Rule sources: `checklist/qa-gate.md`, `workflow/check-rules.py`, the editorial linter, `brand/personas.md`.
Scope: the June 2026 batch: debt-vs-equity-fractional, fractional-real-estate-ira, fractional-real-estate-vs-other-investments, how-to-choose-fractional-real-estate-platform, how-to-read-reg-a-offering-circular, legal-tax-guide-fractional-real-estate, proptech-future-of-real-estate, proptech-trends-2026, real-estate-as-an-asset-class, real-estate-etfs-vs-fractional, real-estate-vs-index-funds-retirement, reit-dividend-taxation, single-family-vs-multifamily-fractional, tokenized-vs-traditional-fractional, what-happens-when-fractional-property-is-sold.
Context: run the same day the four round-2 feedback docs were applied (commit e41397e). Companions: `workflow/batch1-audit-2026-08-11.md`, `workflow/live-site-audit-2026-08-11.md`. None of Batch 2 is currently live.

> **CLIENT APPROVED, 2026-08-16.** The operator relayed the client's sign-off on Batch 1 and Batch 2. Batch 2 is cleared for publication. Two corrections were applied after the approval and are not a reopening of it: the author byline moved to `Youssef Kholeif, CMO` across all 15 articles per the standing byline directive of the same date, and the standing internal-link rule was recorded as absolute (Batch 2 already complied). Batch 2 becomes frozen under the published-batches rule the moment its articles go live, not on approval.

## Verdict in one paragraph

Brand and compliance are clean: zero BLOCKING check-rules findings across all 15, personas consistent, persona-anchor uniqueness holds, internal links healthy (2 to 12 per body, zero dead targets), and the operator-held risky framings (vs high-yield savings, vs direct rental, vs vacation rental) are confirmed absent from the alternatives article. The real catches: one article's Production Notes target a different slug than its folder and its inbound links, one article is missing its meta title, meta description, and hero alt entirely, 10 hero alts exceed the 120-character cap, and five banned-phrase or soft-compliance flags were found and fixed in this pass.

## Finding 1: Slug collision on the exit-mechanics article (HIGH)

`blog/what-happens-when-fractional-property-is-sold/draft.md` carries Production Notes that say `Slug: how-to-sell-fractional-real-estate` with a matching canonical and the meta title "How to Sell Fractional Real Estate: Exit Options". The repo folder, the ROADMAP topic (item 23), and two inbound internal links (from real-estate-vs-index-funds-retirement and single-family-vs-multifamily-fractional) all use `what-happens-when-fractional-property-is-sold`.

Pasted into Framer as-is, the article would publish under the `how-to-sell` slug and orphan both inbound links. Nothing anywhere links to the `how-to-sell` slug.

**Action:** operator picks the slug. If `how-to-sell-fractional-real-estate` wins (it is the stronger commercial keyword), rename the repo folder and update the two inbound links in the same commit. If the folder slug wins, correct the draft's Slug, Canonical, and meta title. Until then this article must not be delivered.

Same file, small extra: its FAQ heading reads "Frequently asked questions", the only lowercase variant in the repo.

## Finding 2: IRA article shipped without SEO metadata (HIGH, fixed in this pass)

`fractional-real-estate-ira/draft.md` had no Meta title, no Meta description, and no Hero alt in its Production Notes: the only Batch 2 draft missing them. The live site's empty-meta-description problem starts at the source for this one; there was nothing to paste.

**Fixed in this audit:** added all three fields within length rules (title 57, description 158, alt 107 chars). Review wording at next read-through.

## Finding 3: Hero alt over 120 characters on 10 of 15 (MEDIUM)

128 to 162 chars: debt-vs-equity (148), vs-other-investments (137), proptech-future (140), proptech-trends (132), asset-class (135), etfs (128), index-funds (162), reit-dividend (138), tokenized (155), property-is-sold (140). Same defect class Batch 3 QA trimmed to 120 and the Batch 1 audit flagged on 4 articles.

**Action:** trim in the next Drive re-delivery pass, one edit per file.

## Finding 4: Meta length drift (MEDIUM)

- Five meta titles under the 55-char floor (47 to 48): debt-vs-equity, how-to-choose, proptech-trends, asset-class, proptech-future. The three "Title tag (SEO)" variants measure 48 to 59.
- Meta descriptions: asset-class at 182 (over 160), vs-other-investments at 166 (marginal).

**Action:** rebalance alongside Finding 3 in the same pass.

## Finding 5: Zero inline external authority links in all 15 bodies (MEDIUM, known class)

Every Batch 2 body carries exactly one external link (the PSFnetwork homepage CTA); authority URLs live only in Sources lists. The 2+ inline authority link rule is formally "Batch 3 onward", so this is the same retrofit decision already teed up for Batch 1 in `workflow/live-sync-2026-08-11.md`.

**Action:** decide the retrofit for Batch 1 and Batch 2 together, one method, one pass.

## Finding 6: Production Notes label drift (LOW)

Three drafts use "Title tag (SEO)" where the rest use "Meta title (SEO)" (etfs, proptech-future, vs-other-investments); some condense fields onto shared lines. Harmless to humans, hostile to tooling; this audit's first parser pass misread 4 files because of it.

**Action:** standardize labels next time each file is touched; consider a `brief-required-sections` style spec for Production Notes.

## Fixed during this audit

| File | Fix |
|---|---|
| legal-tax-guide-fractional-real-estate | Banned FAQ opener "It depends on the structure" reworded |
| real-estate-etfs-vs-fractional | "The right choice depends on" reworded |
| real-estate-vs-index-funds-retirement | "The right choice depends on" reworded |
| proptech-future-of-real-estate | "Best for" table column relabeled "Best suited to" |
| single-family-vs-multifamily-fractional | "Best for" table row relabeled "Best suited to" |
| fractional-real-estate-ira | Missing meta title, meta description, hero alt written (Finding 2) |

## What is clean

- check-rules.py: 0 BLOCKING across all 15 (31 heuristic WARNs, long-sentence and comma-splice tier)
- Editorial linter: 0 banned phrases and 0 compliance flags after the fixes above; brand casing flags are all URL false positives
- Personas: Maya Reyes on 14, Youssef Kholeif on asset-class per today's round-2 doc, Daniel Cho reviewer on all 15; persona-anchor uniqueness tests pass (the June Priya fix holds)
- Internal links: 2 to 12 per body, all 148-link-era targets resolve to real repo slugs, zero dead
- Structure: single H1, Quick Answer, FAQ with 5+ entries, Sources with 3+ URLs on all 15 (parser-case caveat on the one lowercase FAQ heading)
- Canonicals: www host and folder-matching slug on 14 of 15 (Finding 1 is the exception)
- The alternatives article covers only approved comparisons; the operator-held framings from the 2026-05-26 exclusion are absent
- Round-2 feedback: 4 articles current as of today's e41397e
- Repo tests: 43 of 43 pass

## Priority order

1. Resolve the slug collision (Finding 1); the article is undeliverable until then
2. Review the three IRA meta fields written today (Finding 2)
3. Trim the 10 hero alts and rebalance metas (Findings 3, 4) in one pass per file
4. Fold the authority-link retrofit decision into the Batch 1 canonicalization decision
5. Standardize Production Notes labels opportunistically
