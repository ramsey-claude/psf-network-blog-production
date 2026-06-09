# Evidence - how-to-build-passive-income-with-real-estate

Captured: 2026-05-14
Tools: WebSearch + curl with browser UA for federal sources (per `checklist/research-stage.md` Tooling section).

## Confidence legend

| Level | Meaning |
|-------|---------|
| high | Canonical federal source URL; rule directly retrieved or federally codified |
| medium | Source corroborated by multiple third-party guides + platform disclosures |
| low | Single-aggregator or self-reported; do not point-cite |

---

## E1 - Schedule E (Form 1040) is used to report rental real estate income

- Claim refs: C5
- Source URL: https://www.irs.gov/forms-pubs/about-schedule-e-form-1040
- Source publisher: Internal Revenue Service (IRS)
- Source title: About Schedule E (Form 1040), Supplemental Income and Loss
- Source date: 2025 revision (page accessed 2026-05-14)
- Exact quote: "Use Schedule E (Form 1040) to report income or loss from rental real estate, royalties, partnerships, S corporations, estates, trusts, and residual interests in real estate mortgage investment conduits (REMICs)."
- Confidence: high
- Note: Page lists Form 8582 (Passive Activity Loss Limitations) as a related item, which supports C6.

## E2 - Rental real estate is generally a passive activity; Form 8582 limits passive losses

- Claim refs: C6
- Source URL: https://www.irs.gov/forms-pubs/about-schedule-e-form-1040 (related item link to Form 8582)
- Source publisher: IRS
- Source title: About Form 8582, Passive Activity Loss Limitations
- Source date: current
- Confidence: high
- Note: IRC Section 469 categorizes rental real estate as a passive activity by default. Material participation and real estate professional rules can change this; this post does not enter those edge cases.

## E3 - Schedule K-1 (Form 1065) is used by partnerships/LLCs to report each partner's share

- Claim refs: C7
- Source URL: https://www.irs.gov/instructions/i1065sk1
- Source publisher: IRS
- Source title: About Schedule K-1 (Form 1065)
- Source date: current
- Confidence: high
- Note: Cross-references hub post evidence E8.

## E4 - Most REITs distribute at least 90 percent (often closer to 100 percent) of taxable income

- Claim refs: C8
- Source URL: https://www.investor.gov/introduction-investing/investing-basics/investment-products/real-estate-investment-trusts-reits
- Source publisher: SEC Office of Investor Education (investor.gov)
- Source title: Real Estate Investment Trusts (REITs)
- Source date: current
- Exact quote: "Most REITS pay out at least 100 percent of their taxable income to their shareholders. The shareholders of a REIT are responsible for paying taxes on the dividends and any capital gains they receive in connection with their investment in the REIT."
- Confidence: high

## E5 - Non-traded REITs carry distinct liquidity, conflict-of-interest, and distribution-source risks

- Claim refs: C9
- Source URL: https://www.investor.gov/introduction-investing/investing-basics/investment-products/real-estate-investment-trusts-reits
- Source publisher: investor.gov / SEC
- Source title: Real Estate Investment Trusts (REITs)
- Exact quote: "Distributions May Be Paid from Offering Proceeds and Borrowings: Investors may be attracted to non-traded REITs by their relatively high dividend yields compared to those of publicly traded REITs. Unlike publicly traded REITs, however, non-traded REITs frequently pay distributions in excess of their funds from operations. To do so, they may use offering proceeds and borrowings. This practice, which is typically not used by publicly traded REITs, reduces the value of the shares and the cash available to the company to purchase additional assets."
- Confidence: high

## E6 - Real estate investments are not FDIC insured

- Claim refs: C10
- Source URL: https://www.fdic.gov/resources/deposit-insurance/
- Source publisher: FDIC
- Source date: current
- Confidence: high
- Note: Cross-reference to hub evidence E10.

## E7 - $350/year arithmetic on $5,000 at 7%

- Claim refs: C1
- Source: arithmetic (5000 * 0.07 = 350)
- Confidence: n/a (arithmetic, not a sourced claim; presented as illustrative)
- Note: Body labels this as "illustrative" and pairs it with "Returns vary by platform, vintage, and property; figures are illustrative, not promised."

## E8 - Platform-reported passive RE yields commonly in 4-10% range

- Claim refs: C2, C11
- Source URL (representative): https://www.concreit.com/blog/rental-property-vs-fractional-real-estate-investing
- Source publisher: Concreit (aggregator, used as a representative platform-perspective source)
- Source title: Rental Property vs. Fractional Real Estate Investing: How Much Cash Flow Can You Expect?
- Confidence: medium (aggregator; range varies by platform vintage)
- Use rule: cite as a range; never cite "average 7%" as a point claim.

## E9 - Cash-on-cash returns for leveraged single-family rentals typically reported 8-12%

- Claim refs: C12
- Source: aggregated industry guides
- Confidence: low
- Use rule: present with caveats about leverage, vintage, expenses. Do not put in a stat card.

## E10 - Fractional platforms (Fundrise, Arrived, Ark7, PSFnetwork) exist and operate under SEC frameworks

- Claim refs: C13
- Source: Cross-reference to hub evidence E13 (https://fundrise.com/, https://arrived.com/, https://ark7.com/, https://psfnetwork.com/).
- Confidence: high

---

## Reconciliation notes

| Original outline element | Decision | Reason |
|--------------------------|----------|--------|
| Stat card "7% Average target annual yield" | Replaced with "4 to 10% - Typical platform-reported annual yield range" | No audited 7% average; range is more defensible |
| Stat card "2,900 - Monthly searches for keyword" | Dropped, replaced with "$5,000 - Capital to generate ~$350/year at 7% (illustrative)" | SEO metric is internal, not useful to reader |
| Cash-on-cash 8-12% direct rental | Caveat heavily, do not use in stat cards | Leverage assumption is large and varies |

## Summary

- Claims inventoried: 13
- Claims sourced (rows above): 10 (some cover multiple refs)
- Claims dropped or softened: 2 (yield average, SEO stat card)
- Confidence distribution: 6 high, 2 medium, 1 low (capped to qualitative use), 1 arithmetic
