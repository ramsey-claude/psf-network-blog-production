# psfnetwork blog production

End-to-end blog production pipeline for psfnetwork — from draft to published, with multi-expert regulatory review, localization, and QA gates.

## Overview

Every blog post goes through a structured pipeline before publication. The pipeline combines the SEO & GEO blog checklist with a financial regulatory review layer specific to psfnetwork's fractional real estate content.

```
Draft → Expert Panel Review → Revision → Localization → Expert Re-check → QA → Publish
                                                                               ↓ (fail)
                                                                         Back to Draft
```

## Pipeline Stages

### Stage 1 — Expert Panel Discussion
Eight US financial regulatory experts review the draft simultaneously, each from their own domain:

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

### Stage 2 — Content Revision
Draft is revised based on expert panel feedback. Flagged terms, claims, and structures are corrected. The revised draft is documented with a change log.

### Stage 3 — Localization Review
A localization specialist reviews the revised content for market-specific language, local references, and terminology alignment. For psfnetwork content this means:
- TR/EN/FR/AE market-specific terminology
- Local regulatory references where applicable
- Audience-appropriate tone and register

### Stage 4 — Expert Re-check
The localized content goes back through the expert panel. Localization must not introduce inaccurate financial terminology or weaken regulatory compliance language. If issues are found, content returns to Stage 2.

### Stage 5 — QA Gate
Final pre-publication checklist (see `checklist/qa-gate.md`). If any item fails, the pipeline restarts from Stage 1 with the failure reason documented.

## Repository Structure

```
psf-network-blog-production/
├── README.md                        This file
├── checklist/
│   ├── seo-geo-blog-checklist.md    Full SEO & GEO production checklist
│   ├── expert-review-template.md   Per-expert review form
│   ├── localization-guide.md        Localization rules and scope
│   └── qa-gate.md                   QA gate criteria and failure protocol
├── workflow/
│   ├── pipeline.md                  Detailed pipeline steps and decision trees
│   └── loop-log-template.md         Template for logging pipeline restarts
└── brand/
    └── tone-and-voice.md            psfnetwork brand voice for content producers
```

## Brand Notes

- Brand name is always written as **psfnetwork** — all lowercase, one word, no spaces
- Brand colors: Cream #F7F5F0 | Matte Black #1C1C1C | Orange #FF7141 | Blue #4F8FA3
- Font: Söhne (Kräftig, Halbfett, Buch)
- Visual/video assets: produced by Superclasico
- Written content: AI-generated, human-reviewed through this pipeline

## Related Repositories

- [psfnetwork-blog-template](https://github.com/ramsey-claude/psfnetwork-blog-template) — Blog template, brand guidelines, Framer components
- [GEO-SEO-Blog-Writing-](https://github.com/ramsey-claude/GEO-SEO-Blog-Writing-) — SEO & GEO blog checklist (source)
