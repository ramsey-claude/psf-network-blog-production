# Internal link map: Batch 1

Closes finding 2 of `live-site-audit-2026-07-21.md` ("zero internal links on every published article", HIGH) for the 12 Batch 1 articles. Batch 2 had its links re-applied in Framer at publish time; Batch 1 never did, so the pages that carried every AI citation the site has earned linked to nothing while receiving 39 inbound links from Batch 2. That one-way graph is the leading explanation for the AI citation drop of Sep 7 to 14, 2026 (see the master dashboard).

## What changed

- The 12 Batch 1 drafts now carry the 54 links below (41 on existing anchor text, 13 as one added sentence each), so the repo copy matches what should be live.
- `workflow/stage10_runner.py` now counts internal links on the **served** page and fails the post-publish report below 2 (the qa-gate.md threshold). This is the check that would have caught the gap in July.
- `tests/test_stage10_internal_links.py` pins that behaviour.

## How to apply in Framer

The links exist only in the repo until they are re-applied in the Framer CMS editor (hyperlinks do not survive the Doc to Framer paste). The working checklist with anchor sentences and progress tracking is the Internal Link Map artifact. Priority: the first three pages below carried every citation; do them first. Expect Perplexity to need two to three weekly scans to re-evaluate.

Note: the repo slug `what-happens-when-fractional-property-is-sold` publishes as `/blog/how-to-sell-fractional-real-estate`. Always link the live slug.

## The map

7 source/target pairs from the original plan were dropped because no safe anchor exists in the text (marked "not applied"). Every page still has at least 3 links, above the qa-gate threshold of 2. Links live only in the article body, never in front matter, headings, lists, tables, Sources, Author, Disclaimer, CTA or Related.

### fractional-real-estate-investing

- best-fractional-real-estate-platforms (anchor: "platform")
- how-fractional-real-estate-is-taxed (anchor: "tax")
- reits-vs-fractional-real-estate (anchor: "REITs")
- square-foot-real-estate-ownership-explained (anchor: "square-foot")
- how-to-choose-fractional-real-estate-platform (added sentence)
- legal-tax-guide-fractional-real-estate (anchor: "legal")

### best-fractional-real-estate-platforms

- how-to-choose-fractional-real-estate-platform (added sentence)
- reg-a-vs-reg-d-for-fractional-investors (anchor: "Reg A")
- fractional-real-estate-investing (not applied: no safe anchor in the text)
- square-foot-real-estate-ownership-explained (anchor: "square-foot")
- how-to-invest-in-real-estate-with-100 (anchor: "$100")

### how-fractional-real-estate-is-taxed

- legal-tax-guide-fractional-real-estate (anchor: "due diligence")
- reg-a-vs-reg-d-for-fractional-investors (anchor: "Regulation A")
- reit-dividend-taxation (anchor: "1099-DIV")
- reits-vs-fractional-real-estate (anchor: "REIT")
- best-fractional-real-estate-platforms (anchor: "platform")

### reits-vs-fractional-real-estate

- fractional-real-estate-vs-other-investments (added sentence)
- how-fractional-real-estate-is-taxed (anchor: "tax treatment")
- reit-dividend-taxation (anchor: "REIT dividend")
- best-fractional-real-estate-platforms (anchor: "platforms")
- fractional-real-estate-investing (anchor: "Fractional real estate investing")

### reg-a-vs-reg-d-for-fractional-investors

- legal-tax-guide-fractional-real-estate (anchor: "legal")
- how-to-read-reg-a-offering-circular (anchor: "offering circular")
- how-fractional-real-estate-is-taxed (anchor: "tax")
- best-fractional-real-estate-platforms (anchor: "platform")
- real-estate-crowdfunding-vs-fractional (anchor: "crowdfunding")

### square-foot-real-estate-ownership-explained

- fractional-real-estate-investing (not applied: no safe anchor in the text)
- best-fractional-real-estate-platforms (anchor: "platform")
- how-fractional-real-estate-is-taxed (anchor: "tax")
- reg-a-vs-reg-d-for-fractional-investors (anchor: "Reg A")

### how-to-build-passive-income-with-real-estate

- fractional-real-estate-investing (not applied: no safe anchor in the text)
- reits-vs-fractional-real-estate (anchor: "REIT")
- best-fractional-real-estate-platforms (anchor: "platforms")
- how-to-invest-in-real-estate-with-100 (added sentence)
- how-fractional-real-estate-is-taxed (anchor: "tax")

### how-to-invest-10k-in-real-estate

- fractional-real-estate-investing (added sentence)
- how-to-invest-in-real-estate-with-100 (anchor: "$100")
- reits-vs-fractional-real-estate (anchor: "REIT")
- best-fractional-real-estate-platforms (anchor: "platform")
- how-fractional-real-estate-is-taxed (anchor: "tax")

### how-to-invest-in-real-estate-with-100

- fractional-real-estate-investing (not applied: no safe anchor in the text)
- how-to-invest-10k-in-real-estate (added sentence)
- best-fractional-real-estate-platforms (anchor: "platforms")
- reits-vs-fractional-real-estate (anchor: "REIT")
- how-fractional-real-estate-is-taxed (anchor: "K-1")

### real-estate-crowdfunding-vs-fractional

- fractional-real-estate-vs-other-investments (added sentence)
- reg-a-vs-reg-d-for-fractional-investors (anchor: "Regulation A")
- best-fractional-real-estate-platforms (anchor: "platforms")
- reits-vs-fractional-real-estate (anchor: "REIT")
- how-fractional-real-estate-is-taxed (not applied: no safe anchor in the text)

### what-is-proptech

- proptech-trends-2026 (added sentence)
- proptech-future-of-real-estate (added sentence)
- 90-percent-millionaires-real-estate (added sentence)
- real-estate-as-an-asset-class (added sentence)
- fractional-real-estate-investing (not applied: no safe anchor in the text)
- best-fractional-real-estate-platforms (anchor: "platforms")

### 90-percent-millionaires-real-estate

- what-is-proptech (added sentence)
- real-estate-as-an-asset-class (not applied: no safe anchor in the text)
- fractional-real-estate-investing (added sentence)
- how-to-invest-in-real-estate-with-100 (anchor: "$100")
- best-fractional-real-estate-platforms (anchor: "platform")

## Process rule going forward

Every publish to Framer is followed by the Stage 10 runner, which now reports the live internal-link count. A FAIL on that row means the paste dropped the links again: re-apply them in the CMS editor before closing the slug. Until content reaches Framer through the CMS API instead of a manual paste, this check is the only thing standing between a linked draft and an unlinked page.
