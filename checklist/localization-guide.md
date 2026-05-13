# Localization Guide

> **Current operating state (2026-05-14):** psfnetwork operates in the US market only and publishes English-only content. The default pipeline runs with `target_markets: ["EN-US"]`, which makes Stage 5 a no-op. The TR / FR / AE sections of this guide are retained for future expansion but are not invoked in current runs. To enable any non-US market, add it to `target_markets` in the brief's metadata before triggering the pipeline.

This guide defines the scope and rules for the localization review stage (Stage 5) in the psfnetwork blog production pipeline.

---

## Scope

The localization specialist reviews content **after** the expert panel revision (Stage 2) and **before** the expert re-check (Stage 4).

Localization covers:
- Market-specific language and references
- Audience tone and register
- Local terminology alignment
- Currency, date, and number formatting

Localization does **not** cover:
- Financial accuracy (that is the expert panel's job)
- SEO keyword changes (coordinate with SEO lead before changing any keyword)
- Brand voice (see `brand/tone-and-voice.md`)

---

## Target Markets

| Market | Language | Register | Notes |
|--------|----------|----------|-------|
| TR | Turkish | Formal (siz) | Default for psfnetwork TR audience |
| EN | English | Professional, accessible | International/global content |
| FR | French | Formal (vous) | FR market expansion |
| AE | English (Gulf) | Professional | UAE/Gulf fractional real estate market |

---

## Financial Terminology Rules

Financial terms must **not** be localized if doing so changes the legal or regulatory meaning. When in doubt, keep the original English term and add a parenthetical explanation.

Examples:

| Do this | Not this |
|---------|----------|
| fractional ownership (kesirli mülkiyet) | kesirli mülkiyet only — English term must appear |
| ROI (yatırım getirisi) | yatırım getirisi only |
| capital gains | not "kazanç" without qualification |
| SEC-registered | do not translate SEC to a local equivalent |

---

## Local References

For TR market content:
- Reference Turkish real estate market conditions where relevant (TUIK data, TCMB rates)
- Use TL for Turkish Lira, not TRY in body text (TRY acceptable in tables)
- Hitap biçimi: siz (formal) throughout — no sen unless specifically approved

For EN/AE content:
- Reference Dubai Land Department (DLD) for UAE property references
- Currency: AED for UAE, USD for international comparisons

---

## What Triggers a Stage 4 Re-check

The following localization changes automatically trigger a full expert panel re-check:

1. Any change to a financial term, product name, or regulatory body name
2. Addition or removal of a disclaimer or disclosure
3. Change to a numerical claim (rates, returns, limits)
4. Addition of a local regulatory reference not present in the original

If none of the above apply, Stage 4 is still recommended but the expert panel may do a targeted review of changed sections only.

---

## Localization Review Form

| Field | Value |
|-------|-------|
| Content title | |
| Target market | |
| Review date | |
| Localizer | |

### Changes Made

| # | Original text | Localized text | Reason | Triggers expert re-check? |
|---|--------------|----------------|--------|--------------------------|
| 1 | | | | Yes / No |
| 2 | | | | Yes / No |

### Verdict
- [ ] No financial terms changed — Stage 4 targeted review sufficient
- [ ] Financial terms changed — Stage 4 full expert panel review required
- [ ] No localization needed — content proceeds directly to Stage 5 QA
