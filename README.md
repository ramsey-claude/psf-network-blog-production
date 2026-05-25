# psfnetwork blog production

End-to-end blog production pipeline for psfnetwork, from draft to published, with humanization, multi-expert regulatory review, localization, and QA gates.

## Overview

Every blog post goes through a structured pipeline before publication. The pipeline combines the SEO & GEO blog checklist with a humanization pass and a financial regulatory review layer specific to psfnetwork's fractional real estate content.

```
Draft → Humanization Pass → Expert Panel Review → Revision → Localization → Expert Re-check → QA → Publish
           ↑                                                                                       ↓ (fail)
           └──── rewrite ──── Back to Draft ──────────────────────────────────────────────────────┘
```

## Pipeline Stages

### Stage 1: Humanization Pass
A dedicated reviewer rewrites the draft to sound like a person wrote it. This is the only stage with the explicit mandate to break AI cadence and inject human signal. Six steps:

1. AI tells sweep (per `checklist/ai-tells.md` ban list)
2. Human anchor injection (real story, POV, contrarian note, sourced from the brief)
3. Rhythm and cadence rewrite (sentence and paragraph length variance)
4. De-listification (at least 40% narrative H2s)
5. Voice consistency (second person throughout)
6. Specificity audit (named subjects, dollar figures, dates, no generic claims)

The draft cannot enter Stage 2 with any HIGH-tier AI tell unresolved, all three Human Anchors missing, or a failed cadence/voice check. See `checklist/humanization-pass.md`.

### Stage 2: Expert Panel Discussion
Eight US financial regulatory experts review the humanized draft simultaneously, each from their own domain:

| Expert | Domain | Focus in psfnetwork content |
|--------|--------|----------------------------|
| SEC | Securities Markets | Investment offering language, securities disclaimers |
| CFTC | Futures & Derivatives | Derivative product references, commodity language |
| Fed | Monetary Policy | Interest rate commentary, monetary policy claims |
| OCC | National Banks | Banking product comparisons, lending references |
| FDIC | Deposit Insurance | Deposit product language, insurance claim accuracy |
| CFPB | Consumer Protection | Consumer-facing claims, fee disclosures |
| FINRA | Broker-Dealers | Brokerage comparisons, investment return claims |
| FSOC | Systemic Risk | Macro-financial risk statements |

Each expert flags issues in their domain. The panel reaches consensus on required revisions before the content moves forward.

### Stage 3: Content Revision
Draft is revised based on expert panel feedback. Flagged terms, claims, and structures are corrected. The revised draft is documented with a change log. Voice changes from this stage that risk re-introducing AI tells trigger a targeted humanization re-pass.

### Stage 4: Localization Review
A localization specialist reviews the revised content for US English voice and US market-specific language. psfnetwork operates exclusively in the US market with English-only content (`target_markets: ["EN-US"]`). Localization covers:
- US English register and tone (en-US, no UK spellings)
- US regulatory terminology alignment (SEC, FINRA, IRS, state bodies)
- US conventions: USD currency, MM/DD/YYYY dates, imperial units for real estate

### Stage 5: Expert Re-check
The localized content goes back through the expert panel. Localization must not introduce inaccurate financial terminology or weaken regulatory compliance language. If issues are found, content returns to Stage 3.

### Stage 6: QA Gate
Final pre-publication checklist (see `checklist/qa-gate.md`). If any item fails, the pipeline restarts from Stage 1 with the failure reason documented.

## Repository Structure

```
psf-network-blog-production/
├── README.md                              This file
├── checklist/
│   ├── ai-tells.md                        Ban list of AI-generated language tells
│   ├── humanization-pass.md               Stage 1 humanization spec
│   ├── brief-required-sections.md         Brief format including Human Anchors
│   ├── seo-geo-blog-checklist.md          Full SEO & GEO production checklist
│   ├── expert-review-template.md          Per-expert review form
│   ├── editorial-review.md                Editorial reviewer checklist (Stage 2)
│   ├── localization-guide.md              Localization rules and scope (US/EN only)
│   └── qa-gate.md                         QA gate criteria and failure protocol
├── workflow/
│   ├── pipeline.md                        Detailed pipeline steps and decision trees
│   └── loop-log-template.md               Template for logging pipeline restarts
└── brand/
    ├── tone-and-voice.md                  psfnetwork brand voice for content producers
    ├── personas.md                        Target audience personas
    └── voice-samples/                     Reference writing samples from psfnetwork team
```

## Brand Notes

- Brand name is always written as **psfnetwork**: all lowercase, one word, no spaces
- Brand colors: Cream #F7F5F0 | Matte Black #1C1C1C | Orange #FF7141 | Blue #4F8FA3
- Font: Söhne (Kräftig, Halbfett, Buch)
- Visual/video assets: produced by Superclasico
- Written content: AI-drafted, humanization-reviewed, regulator-cleared

## Related Repositories

- [psfnetwork-blog-template](https://github.com/ramsey-claude/psfnetwork-blog-template), Blog template, brand guidelines, Framer components
- [GEO-SEO-Blog-Writing-](https://github.com/ramsey-claude/GEO-SEO-Blog-Writing-), SEO & GEO blog checklist (source)
