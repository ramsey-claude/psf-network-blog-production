# Batch 1 Audit: 12 Articles vs the Current QA Standard

Date: 2026-08-11
Method: deterministic checks run locally against the canonical draft of each Batch 1 article. Rule sources: `checklist/qa-gate.md` (including the inline external authority link rule added 2026-07-22), `brand/template-structure.md`, `brand/personas.md`, `brand/tone-and-voice.md`, `workflow/check-rules.py`.
Scope: the 12 Batch 1 articles per `workflow/visuals-tracker.md`. Canonical draft is `draft.md` for 10 of them; `draft-v2-humanized.md` for best-fractional-real-estate-platforms and fractional-real-estate-investing.

Why now: Batch 2 was re-synced with 148 internal links and brand feedback applied. Batch 3 shipped born-compliant with the inline external authority link rule. Batch 1, the oldest batch, has never been re-checked against the standard that evolved after it shipped. This audit closes that gap.

> **CLIENT APPROVED, 2026-08-16.** The operator relayed the client's sign-off on Batch 1 and Batch 2. Batch 1 is live and therefore frozen: the retrofit options this audit lays out below (internal and external link retrofit, hero alt trims, canonicalization) stay open decisions and are not executed as a sweep. The author byline on the live Batch 1 articles was corrected in Framer by the operator; the repo drafts still show the retired persona because frozen means frozen, and that gap is recorded debt rather than something to fix in place.

---

## Verdict in one paragraph

No brand or compliance violations: `check-rules.py` reports zero BLOCKING findings across all 12 drafts, personas are consistent, every structural block is present, and all 43 repo tests pass. The batch's real gap is links: not one Batch 1 draft contains a single inline link in its body, which fails the current qa-gate internal link requirement and predates the external authority link rule entirely. Secondary findings: 8 Related blocks point at the still-unpublished REIT comparison article, 4 hero alts exceed the 120-character cap, 5 disclaimers are not verbatim, and 2 titles plus 2 meta descriptions are outside their length windows.

---

## Finding 1: Zero inline body links in all 12 drafts (HIGH)

Every Batch 1 draft carries exactly 3 internal links, all inside the Related block, and zero links of any kind inside the article body. Sources sections list URLs as plain text, not markdown links.

Against the current qa-gate section B this fails two items batch-wide:

| Rule | Requirement | Batch 1 state |
|---|---|---|
| Internal links | 2+ in-body links to posts that exist in the repo | 0 in all 12 |
| External authority links | 2+ inline in body, allowed-domain list, rule active Batch 3 onward | 0 in all 12 |

Context: Batch 2 drafts carry 148 internal links after the 2026-07 re-sync. Batch 3 articles shipped with 4 to 7 inline external authority links and 2 to 5 internal links each. Batch 1 is now the only batch with none. The external authority rule is formally scoped "Batch 3 onward," so this is a retrofit decision for the operator, not a rule breach; the internal link item has no such scoping and is a straight FAIL under the current gate.

**Action:** run a link retrofit pass over all 12 articles, mirroring the Batch 3 method (internal links at natural mention points from the existing hub-and-spoke map, external links only from the allowed authority domains). Then re-deliver to Drive and re-paste or API-sync to Framer. Note the live-site audit already showed links do not survive the Doc-to-Framer paste, so the retrofit only pays off together with that delivery fix.

## Finding 2: 8 Related blocks point at the unpublished REIT article (HIGH, known root cause)

8 of the 12 Batch 1 drafts list `/blog/reits-vs-fractional-real-estate` in Related: best-fractional-real-estate-platforms, fractional-real-estate-investing, how-fractional-real-estate-is-taxed, how-to-build-passive-income-with-real-estate, how-to-invest-in-real-estate-with-100, real-estate-crowdfunding-vs-fractional, square-foot-real-estate-ownership-explained, what-is-proptech.

The target exists in the repo (so this passes the repo-existence check) but is still absent from the live sitemap per `workflow/live-site-audit-2026-07-21.md`. Combined with the 10 Batch 2 links already counted there, publishing this one article closes 18 dead links across the site. Its visual is produced and waiting (see `workflow/visuals-tracker.md`).

**Action:** unchanged from the live-site audit: publish reits-vs-fractional-real-estate in Framer, place its visual in the same edit.

**Update, later the same day:** the article is now live, so the 404 side of this finding is closed. The publish skipped the visual and carried its own defects; see `workflow/live-site-audit-2026-08-11.md` Finding 2.

## Finding 3: Frontmatter length drift on 6 articles (MEDIUM)

| Article | Field | Actual | Target |
|---|---|---|---|
| how-to-invest-10k-in-real-estate | title | 53 chars | 55 to 60 |
| real-estate-crowdfunding-vs-fractional | title | 61 chars | 55 to 60 |
| square-foot-real-estate-ownership-explained | meta_description | 144 chars | 150 to 160 |
| how-to-invest-10k-in-real-estate | meta_description | 147 chars | 150 to 160 |
| real-estate-crowdfunding-vs-fractional | hero_visual_alt | 135 chars | 60 to 120 |
| 90-percent-millionaires-real-estate | hero_visual_alt | 131 chars | 60 to 120 |
| how-fractional-real-estate-is-taxed | hero_visual_alt | 160 chars | 60 to 120 |
| reg-a-vs-reg-d-for-fractional-investors | hero_visual_alt | 189 chars | 60 to 120 |

These predate the hard-count discipline added after the 2026-05-15 incidents; Batch 3 QA trimmed identical hero-alt overruns to 120. Also related: the live-site audit found the site-wide " - PSFnetwork" title suffix pushes several live titles past 60, which is a CMS-side fix, not a draft fix.

**Action:** trim the 4 hero alts and rebalance the 2 titles and 2 metas in the same retrofit pass as Finding 1, so Drive and Framer are touched once, not twice.

## Finding 4: Disclaimer not verbatim on 5 articles (MEDIUM)

Canonical text per `brand/tone-and-voice.md` reads "Fractional real estate investing involves risk." Five articles drift:

- Generic wording ("Real estate investing involves risk," missing "Fractional"): how-to-invest-10k-in-real-estate, real-estate-crowdfunding-vs-fractional, 90-percent-millionaires-real-estate
- Extended variants adding tax or legal advice language: how-fractional-real-estate-is-taxed (adds tax advice and CPA sentence), reg-a-vs-reg-d-for-fractional-investors (adds legal, regulatory, and accreditation sentence)

The extended variants are arguably better suited to their topics than the canonical text. The qa-gate item as written ("text matches the canonical disclaimer") makes them a FAIL anyway.

**Action:** operator decision: either align all 5 to canonical, or bless topic-specific extended variants in `brand/tone-and-voice.md` and keep them. The 3 generic ones should gain "Fractional" either way.

## Finding 5: Canonical host spec disagrees with the live site (LOW)

The live site 301-redirects to `www.psfnetwork.com` and its canonical tags carry the www host (verified today against the live what-is-proptech page). The spec in `checklist/qa-gate.md` and `brand/template-structure.md` mandates `https://psfnetwork.com/blog/[slug]` without www. Drafts are split repo-wide: 13 without www (including 11 of 12 Batch 1), 10 with www (fractional-real-estate-investing v2 plus Batch 3).

Live pages are unaffected (Framer sets the real canonical), so this is a documentation consistency issue, not a live SEO issue.

**Action:** update the two spec files to the www form and normalize draft frontmatter opportunistically when a draft is next touched.

## Finding 6: check-rules warnings, no blockers (INFO)

Zero BLOCKING findings across all 12 canonical drafts: no em or en dashes, no casing violations, no banned language. 30 WARNs, all heuristic tier:

- 25 run-on flags (sentences of 40+ words with 3+ commas). Concentrated in how-to-invest-10k (4), real-estate-crowdfunding (3), 90-percent-millionaires (3), how-fractional-taxed (3), square-foot (3).
- 3 comma-splice flags (square-foot, 90-percent-millionaires, how-fractional-taxed x2).
- 2 "leverage" flags in how-to-build-passive-income, both false positives: "leveraged single-family" (adjective) and "market, leverage, and vacancy" (noun, standard finance usage). The rule bans the verb only. <!-- check-rules: allow -->

**Action:** none required for publish. Worth a light editing pass on the run-on clusters if these articles get the Finding 1 retrofit anyway.

## Finding 7: Answer capsules over the 75-word cap in 5 articles (INFO)

13 capsules measure 76 to 88 words: square-foot (4), how-to-invest-10k (3), 90-percent-millionaires (3), real-estate-crowdfunding (2), what-is-proptech (1). All other capsules across the batch are in range. Same drift class as the 2026-05-14 incident; the cap was enforced by count only from Batch 2 onward.

**Action:** trim opportunistically during the retrofit pass; not publish-blocking on its own.

## Not verifiable from this environment

External URL liveness. 51 unique external URLs were inventoried across the 12 Sources sections, but this sandbox's network policy denies CONNECT to all of them (only psfnetwork.com resolved), so none could be re-verified today. Last full verification was the repo-wide link audit in commit 6d26e2d. The inventory is reproducible with the extraction snippet in this audit's method; re-run the curl pass from the operator machine.

---

## What is clean

- check-rules.py: 0 BLOCKING on all 12 canonical drafts
- Personas: Maya Reyes author and Daniel Cho reviewer on all 12, no rogue names; persona uniqueness tests pass
- Structure: H1 unique, QuickAnswer with exactly 4 stat cards, FAQ with 5+ pairs, Sources, Author, Disclaimer, CTA, Related all present on all 12. The "The 60-second version" heading on best-fractional v2 is the QuickAnswer block under its QA-accepted humanized name (see `qa-report-v2.md`)
- Related blocks: exactly 3 links each, every target slug exists in the repo
- Repo test suite: 43 of 43 pass
- Visuals: 12 of 12 produced, 11 placed, per `workflow/visuals-tracker.md`

## Per-article summary

| Article (canonical draft) | Body words | Inline body links | Findings |
|---|---|---|---|
| square-foot-real-estate-ownership-explained | ~1,700 | 0 | meta 144; 4 capsules over; dead Related link |
| how-to-build-passive-income-with-real-estate | ~2,100 | 0 | dead Related link |
| reits-vs-fractional-real-estate | ~2,000 | 0 | itself unpublished (Finding 2) |
| best-fractional-real-estate-platforms (v2) | ~2,600 | 0 | dead Related link |
| fractional-real-estate-investing (v2) | ~2,200 | 0 | www canonical (matches live, not spec); dead Related link |
| how-to-invest-10k-in-real-estate | ~1,600 | 0 | title 53; meta 147; generic disclaimer; 3 capsules over |
| how-to-invest-in-real-estate-with-100 | ~1,900 | 0 | dead Related link |
| real-estate-crowdfunding-vs-fractional | ~1,400 | 0 | title 61; alt 135; generic disclaimer; 2 capsules over; dead Related link |
| 90-percent-millionaires-real-estate | ~1,500 | 0 | alt 131; generic disclaimer; 3 capsules over |
| how-fractional-real-estate-is-taxed | ~3,200 | 0 | alt 160; extended disclaimer; dead Related link |
| reg-a-vs-reg-d-for-fractional-investors | ~3,100 | 0 | alt 189; extended disclaimer |
| what-is-proptech | ~1,600 | 0 | 1 capsule over; dead Related link |

## Priority order

1. Publish reits-vs-fractional-real-estate in Framer with its visual (closes 18 dead links site-wide, unblocks the last Batch 1 visual)
2. Decide the Batch 1 link retrofit (Finding 1). If approved, fold Findings 3, 4, 6, and 7 into the same pass so every article is edited once
3. Reconcile the canonical host spec (Finding 5) in qa-gate.md and template-structure.md
4. Re-run the external URL liveness pass from a machine with open egress
