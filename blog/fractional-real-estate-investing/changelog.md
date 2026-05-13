# Stage 4 Revision Changelog

Input: `draft.md` v1 + `expert-reviews/stage3-moderator-consensus.md`
Output: `draft.md` v2 (this revision)
Date: 2026-05-14
Loop count: 0

## Issues applied (8 of 8 consolidated)

### 1. Stat card "$20 minimum" reframing - MED
Issue raised by: SEC, FINRA, CFPB, Editorial (unanimous)
**Before:** "$20 - Minimum investment on some regulated US platforms"
**After:** "$20 - Per-share minimum on some regulated US platforms (e.g., Ark7)"
Body change: Added clarifying sentence in QuickAnswer: "A single share on some regulated US platforms (such as Ark7) costs as little as $20; a meaningful position typically requires aggregating multiple shares."
Reason: Headline "minimum investment" could be misread as the floor for a complete investment position. Clarifying the per-share nature and the need to aggregate addresses SEC's precision concern, FINRA's suitability concern, CFPB's consumer-expectation concern, and Editorial's credibility concern in one fix.

### 2. CTA rewrite with offering circular + risk inline - MED
Issue raised by: SEC (solicitation), CFPB (proximity)
**Before:** "Ready to look at a property? Browse psfnetwork's current offerings, view the square-foot breakdown, and read the full risk disclosures before you invest."
**After:** "Ready to look at a property? psfnetwork's offerings are made only under qualified offering documents. Review the offering circular and risk factors before you invest. All investments involve risk, including the possible loss of principal."
Reason: Adds the qualified-offering condition (SEC: protects against general-solicitation issues if Reg D 506(b) applies; harmless if Reg A or 506(c) applies) and the inline risk line (CFPB: disclosure adjacent to the action).

### 3. Stat card risk-line footer - MED
Issue raised by: FINRA, Editorial
**Before:** No risk line directly under the stat cards.
**After:** Added italic line below the stat cards: "Past performance does not predict future results. All investments carry risk including loss of principal."
Reason: Return claim in stat-card form needs adjacent risk disclosure for both compliance and credibility.

### 4. K-1 complexity flag for consumers - MED
Issue raised by: CFPB, Editorial
**Before:** "...distributions are typically reported on a Schedule K-1 (Form 1065) because the LLC is usually a pass-through entity. When the property is sold..."
**After:** "...distributions are typically reported on a Schedule K-1 (Form 1065) because the LLC is usually a pass-through entity. K-1 reporting can be more complex than a standard 1099 and may delay your tax filing; consult a tax advisor before investing. When the property is sold..."
Reason: First introduction of K-1 should flag that it is materially different from a 1099 for consumer expectations.

### 5. Square-foot example caveats (illustration only + LLC reframing) - MED
Issue raised by: SEC, FINRA
**Before:** "...buying 50 square feet means a $20,000 stake representing 4.17% of the property and its income."
**After:** "...buying 50 square feet means a $20,000 stake representing 4.17% of the property and its income. These figures are for illustration only; actual property pricing varies, and the security itself remains an LLC membership interest priced per square foot."
Reason: Both reviewers' concerns fixed in one sentence: SEC's LLC framing concern and FINRA's anchor-effect concern.

### 6. Hook rewrite - MED
Issue raised by: Editorial
**Before:** "A few years ago, owning rental property meant a down payment of $20,000 or more, a mortgage application, and a long list of repairs you would learn about at 2 a.m."
**After:** "The minimum stake in a US rental property used to be a $20,000 down payment. Now it can be $20."
Reason: Sharper contrast in the first sentence. AI-extractable, share-worthy.

### 7. "What you will get" payoff added to Opening - LOW
Issue raised by: Editorial
**Before:** Opening paragraph 2 ended at "share-based platforms."
**After:** Appended: "By the end, you will know whether fractional real estate fits your situation and how to evaluate any platform before you commit."
Reason: Explicit reader payoff promise.

### 8. Platform shutdown FAQ realism - LOW
Issue raised by: FINRA, CFPB
**Before:** "Finding a replacement servicer can take time, however, and disputes can drag. Read the operating agreement to understand the backup servicer arrangement before investing."
**After:** "Finding a replacement servicer can take time, however, and disputes can take months or years to resolve. Full recovery is not assured. Read the operating agreement's backup-servicer language before investing, not after."
Reason: Sharpens realism per both reviewers' notes. Specifies the time scale and the not-assured-recovery point.

## Bonus LOW fixes applied

### B1. H2 wording trim
**Before:** "How does fractional real estate investing work, step by step?"
**After:** "How does fractional real estate investing work?"
Reason: Editorial flag #3. Shorter H2, "step by step" moved into the capsule.

### B2. Sources section: SEC abbreviation
**Before:** "U.S. Securities and Exchange Commission, ..." three times in a row.
**After:** First mention spells out "U.S. Securities and Exchange Commission (SEC)"; subsequent rows use "SEC, ...".
Reason: Editorial flag #4. Readability.

## Issues NOT applied

None. All 8 consolidated issues + 2 bonus LOWs were applied. The Related anchor verification (Editorial flag #5) remains a pre-publish QA item, not a revision item, because the linked slugs are not yet published; anchors are provisional and will be re-verified at publish time of each spoke.

## Stage 4 self-check: capsule length compliance

Per `brand/template-structure.md`, every answer capsule must be 50-75 words and self-contained. Post-revision word counts:

| H2 | Word count v2 (initial) | Action | Word count v2 (final) |
|----|------------------------|--------|----------------------|
| What is fractional real estate investing? | 76 | Tighten | 67 |
| How does fractional real estate investing work? | 76 | Tighten | 62 |
| How does fractional ownership compare to owning a whole property? | 53 | None | 53 |
| What is the square-foot ownership model? | 100 (caveat in capsule) | Split caveat to body | 59 |
| Is fractional real estate a good investment? | 73 | None | 73 |
| How do you choose a fractional real estate platform? | 46 (under floor) | Expand | 69 |

All 6 capsules now within 50-75 word range.

## Word count

v1: approximately 1,650 words (body, excluding frontmatter and sources)
v2 (final): approximately 1,720 words

## Result

Draft v2 ready for Stage 7 (Pre-publish QA). Stages 5 and 6 are no-ops under default `target_markets: ["EN-US"]`.
