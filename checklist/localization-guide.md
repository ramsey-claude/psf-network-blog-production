# Localization Guide

> **Operating scope:** PSFnetwork operates in the US market only and publishes English-only content. The pipeline runs with `target_markets: ["EN-US"]`. No other markets or languages are in scope.

This guide defines the scope and rules for the localization review stage (Stage 5) in the PSFnetwork blog production pipeline.

---

## Scope

The localization specialist reviews content **after** the expert panel revision (Stage 2) and **before** the expert re-check (Stage 4).

Localization covers:
- US English voice, tone, and register
- US market-specific language and references
- US regulatory terminology alignment
- Currency, date, and number formatting (USD, MM/DD/YYYY, US comma/decimal conventions)

Localization does **not** cover:
- Financial accuracy (that is the expert panel's job)
- SEO keyword changes (coordinate with SEO lead before changing any keyword)
- Brand voice (see `brand/tone-and-voice.md`)

---

## Target Market

| Market | Language | Register | Notes |
|--------|----------|----------|-------|
| US | English (en-US) | Professional, accessible | PSFnetwork operates exclusively in the US market |

---

## Financial Terminology Rules

Financial terms must use the standard US English form. Do not introduce translations, transliterations, or non-US regulatory equivalents.

Examples:

| Do this | Not this |
|---------|----------|
| fractional ownership | partial ownership, share-in-property |
| return on investment (ROI) | yield-on-capital, profit-rate |
| capital gains | gains, returns (without qualification) |
| SEC-registered | regulator-approved (without naming SEC) |

When a term has a non-obvious meaning to a US retail audience, add a short parenthetical or footnote, but the canonical US English term must appear first.

---

## US Market References

- Currency: USD throughout. Use `$1,234.56` formatting (comma thousands, period decimal).
- Dates: `May 14, 2026` in body text; `MM/DD/YYYY` in tables/forms.
- Real estate references: use US-recognized bodies, SEC, FINRA, state real estate commissions, county recorder offices, IRS for tax references.
- Avoid UK English spellings (use *organize* not *organise*, *color* not *colour*).
- Avoid metric units in property descriptions unless paired with imperial (e.g., square feet primary, square meters secondary).

---

## What Triggers a Stage 4 Re-check

The following localization changes automatically trigger a full expert panel re-check:

1. Any change to a financial term, product name, or regulatory body name
2. Addition or removal of a disclaimer or disclosure
3. Change to a numerical claim (rates, returns, limits)
4. Addition of a regulatory reference not present in the original

If none of the above apply, Stage 4 is still recommended but the expert panel may do a targeted review of changed sections only.

---

## Localization Review Form

| Field | Value |
|-------|-------|
| Content title | |
| Target market | US (en-US) |
| Review date | |
| Localizer | |

### Changes Made

| # | Original text | Localized text | Reason | Triggers expert re-check? |
|---|--------------|----------------|--------|--------------------------|
| 1 | | | | Yes / No |
| 2 | | | | Yes / No |

### Verdict
- [ ] No financial terms changed, Stage 4 targeted review sufficient
- [ ] Financial terms changed, Stage 4 full expert panel review required
- [ ] No localization needed, content proceeds directly to Stage 5 QA
