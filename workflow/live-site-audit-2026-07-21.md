# Live Site Audit: psfnetwork.com/blog

Date: 2026-07-21
Method: sitemap.xml enumeration, plus server-rendered HTML fetched per article with a browser User-Agent.
Scope: all 13 blog articles listed in the live sitemap.

Triggered by: operator request to verify why `/blog/reits-vs-fractional-real-estate` returns 404 when 10 Batch 2 articles link to it.

---

## Answer to the original question

`reits-vs-fractional-real-estate` is **not published**. It is absent from `sitemap.xml` entirely. This is not a slug mismatch; five alternate slug spellings were tested and all return 404.

The article exists as a Batch 1 draft in this repo and is linked from 10 Batch 2 articles. Until it is published in Framer, every one of those links is dead.

---

## Published inventory (from sitemap.xml)

Batch 1, live (11):
90-percent-millionaires-real-estate, best-fractional-real-estate-platforms,
fractional-real-estate-investing, how-fractional-real-estate-is-taxed,
how-to-build-passive-income-with-real-estate, how-to-invest-10k-in-real-estate,
how-to-invest-in-real-estate-with-100, real-estate-crowdfunding-vs-fractional,
reg-a-vs-reg-d-for-fractional-investors, square-foot-real-estate-ownership-explained,
what-is-proptech

Batch 1, NOT live (1):
reits-vs-fractional-real-estate

Batch 2, live (2):
how-to-choose-fractional-real-estate-platform, proptech-future-of-real-estate

Batch 2, NOT live (13):
everything else from the June 2026 batch

Other pages in the blog path: `/blog`, `/blog/getting-started`

---

## Finding 1: Two live Batch 2 articles carry un-fixed content (HIGH)

The two Batch 2 articles that are already public are exactly the two Youssef Kholeif left comments on. Both still show the content his 2026-07-14 feedback asked to change.

| Article | "Priya" | "Risk note" | "Comparison spoke" | hub/spoke jargon |
|---|---|---|---|---|
| how-to-choose-fractional-real-estate-platform | live | not present | live | live |
| proptech-future-of-real-estate | live | live | not applicable | not present |

The corrected versions exist in this repo and in Drive. They have not been pasted into Framer.

**Action:** update these two articles in Framer first. They are the only Batch 2 content a reader can currently reach.

---

## Finding 2: Zero internal links on every published article (HIGH)

Every one of the 13 live articles contains **no links to any other article**. Verified two ways: no matching `href` attributes, and the target slug strings do not appear anywhere in the served HTML.

The drafts do contain these links. Examples:

| Article | Internal links in draft | Internal links live |
|---|---|---|
| proptech-future-of-real-estate | 9 | 0 |
| how-to-choose-fractional-real-estate-platform | 12 | 0 |

Across the 15 re-synced Batch 2 drafts there are 148 internal links, none of which survive to the live site.

This directly answers Youssef's comment on the PropTech pillar table, "Are we hyperlinking all the articles here?" The answer is no, and it is not limited to that table.

**Root cause:** hyperlinks are lost in the Google Doc to Framer paste. The same class of loss was found earlier in the Drive-to-repo sync when `export-as-text` was used; that path was fixed by switching to HTML export.

**Action:** links must be re-applied inside Framer after pasting, or content must reach Framer through the CMS API rather than a manual paste.

---

## Finding 3: Meta description empty on all 13 articles (HIGH)

Every article serves:

```html
<meta name="description" content>
<meta property="og:description" content>
<meta name="twitter:description" content>
```

The attribute is present with no value. `og:title` is populated correctly, so the SEO fields are wired but the description input is empty in the CMS.

Each draft carries a written meta description in its Production Notes block. That value is not being entered into Framer.

**Action:** populate the description field for all 13 live articles from the drafts.

---

## Finding 4: Three H1 tags per page (MEDIUM)

Every article renders three `<h1>` elements:

1. The article title (correct)
2. "Start from square one" (CTA block)
3. "Start from square one" (repeated)

Only the first should be an H1. The CTA heading should be an H2 or lower.

This is a template-level issue, not a content issue, and matches the heading-hierarchy finding already recorded in the Framer audit notes. Fixing it in the template corrects all articles at once.

**Action:** retag the CTA block heading in the Framer blog template.

---

## Finding 5: Title tags over 60 characters (LOW)

Five articles exceed the 60-character guideline used by `checklist/qa-gate.md` section B2:

| Chars | Article |
|---|---|
| 90 | proptech-future-of-real-estate |
| 86 | how-to-choose-fractional-real-estate-platform |
| 84 | how-to-build-passive-income-with-real-estate |
| 83 | real-estate-crowdfunding-vs-fractional |
| 83 | square-foot-real-estate-ownership-explained |

The live title tag appends " - PSFnetwork" to the CMS title, which pushes several past the limit. The drafts' own titles are within range, so the overflow comes from the site-wide suffix.

**Action:** either shorten the CMS titles for these five, or drop the suffix on longer titles.

---

## What is working

- Canonical URL correct on all 13
- JSON-LD present on all 13: BlogPosting, ImageObject, Organization, Person
- `robots` meta present
- `og:title` populated correctly
- Heading structure below H1 is sensible (13 H2s on the sampled article)

---

## Priority order

1. Update the two live Batch 2 articles with the brand-feedback-corrected content
2. Publish `reits-vs-fractional-real-estate` to close 10 dead links
3. Fill meta descriptions for all 13 live articles
4. Re-apply internal links, or move to CMS API delivery so links survive
5. Retag the CTA H1 in the template
6. Trim the five long title tags
