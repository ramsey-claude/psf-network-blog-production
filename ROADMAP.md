# PSFnetwork Blog Production - Master Roadmap

Last updated: May 2026

> **Operating scope:** PSFnetwork is a US-based fractional real estate company. All blog content is published in English for the US market. Multi-market localization is spec'd in `checklist/localization-guide.md` for future expansion but is not invoked by the default pipeline.

---

## Repository structure

Every blog post lives at:

```
blog/
└── [slug]/
    ├── brief.md                    Keyword targets, audience, angle, competitors
    ├── outline.md                  Section-by-section content plan
    ├── evidence.md                 Sourced facts and stats (Stage 1)
    ├── serp-snapshot.md            SERP capture (Stage 1)
    ├── claim-inventory.md          Claims to source (Stage 1)
    ├── draft.md                    Full content draft (Stage 2 output, revised in Stage 4)
    ├── changelog.md                Stage 4 revision log
    ├── qa-report.md                Stage 7 output
    ├── delivery-manifest.md        Stage 9 Drive upload manifest
    ├── pipeline-state.json         Persistent state, updated every stage
    ├── [slug]-chart.tsx            Framer-compatible TypeScript chart, if applicable
    └── expert-reviews/             One .md per reviewer for Stage 3 (and Stage 6 if triggered)
        ├── stage3-panel-selection.md
        ├── stage3-sec.md
        ├── stage3-finra.md
        ├── stage3-cfpb.md
        ├── stage3-editorial.md
        └── stage3-moderator-consensus.md
```

---

## Step 1 - Competitor Top Traffic Pages (Semrush, May 2026)

### Ark7 (most aggressive content player)
| URL | Traffic | Pattern |
|-----|---------|---------|
| ark7.com/ | 1,526 | Homepage |
| best-neighborhoods-to-invest-in-kingston-ny | 1,347 | City guide |
| best-neighborhoods-to-invest-in-monterey-ca | 668 | City guide |
| best-neighborhoods-to-invest-in-norwalk-ct | 523 | City guide |
| best-neighborhoods-to-invest-in-sparks-nv | 306 | City guide |

**Pattern:** Programmatic city guides ("best neighborhoods to invest in [City]") dominate. Comparison content gets minimal traffic. City SEO is Ark7's main acquisition channel.

### Fundrise
| URL | Traffic | Pattern |
|-----|---------|---------|
| fundrise.com/ | 31,100 | Homepage (brand) |
| /education/reits-101-a-beginners-guide | 476 | REIT education |
| /guides/real-estate-investing-guide | 212 | Beginner guide |
| /how-it-works | 160 | Product page |

**Pattern:** Brand traffic dominates (73%). Education content drives the rest. No programmatic content.

### Arrived
| URL | Traffic | Pattern |
|-----|---------|---------|
| arrived.com/ | 34,381 | Homepage (brand) |
| /blog/section-8 | 192 | Niche topic |
| /blog/how-to-finance-a-vacation-rental-property | 121 | Vacation rental |
| /blog/arbitrage | 116 | Arbitrage |
| /blog/fractional-real-estate-investing | 100 | Core topic |
| /blog/types-of-real-estate-investments | 92 | Education |

**Pattern:** Brand traffic dominates (92%). Niche topics outperform core topics on the blog.

### Mogul / Realbricks / Lofty / Groundfloor
See git history. Pattern: brand-heavy with one or two outlier articles each. Realbricks's "90% of millionaires own real estate" stat-hook drives 763 traffic - a model worth studying.

---

## Step 2 - Content Gap Analysis: What Competitors Are NOT Covering

| # | Gap Topic | Why It's a Gap | Est. KD | Est. Volume |
|---|-----------|---------------|---------|-------------|
| 1 | Square-foot real estate ownership explained | Unique PSFnetwork model, no competitor addresses it | Low | Definitional |
| 2 | Fractional real estate vs REIT (clear comparison) | Competitors mention both but no one owns the comparison | Low-Med | 880+ |
| 3 | How to invest in real estate with $100 | Realbricks has it weakly; strong keyword signal | Low | 581 traffic |
| 4 | 90% of millionaires own real estate | Realbricks drives 763 traffic with this hook | Low | High CTR hook |
| 5 | Passive income from real estate (beginner guide) | Covered broadly but no definitive version | Low (10 KD) | 320 vol |
| 6 | Best fractional real estate platforms comparison | Competitors avoid objective comparisons | Med | 590+ |
| 7 | Proptech news and trends | 14,800 vol, KD 31, ignored entirely | Low | 14,800 |
| 8 | REITs 101 for beginners | Fundrise has an old version | Med | 4,400+ |
| 9 | Real estate crowdfunding vs fractional | Terms used interchangeably; no clean structural breakdown | Low | Medium |
| 10 | How to invest $10,000 in real estate | Mid-tier capital level; specific dollar anchor | Low-Med | 480 (related kw) |
| 11 | REIT dividends taxation explained | Specific tax-treatment angle, complements REITs vs Fractional | Med | 1,600 |
| 12 | Real estate ETFs vs fractional | VNQ/IYR vs Reg A fractional - liquid vs structured | Low-Med | Medium |
| 13 | Reg A vs Reg D for fractional investors | Regulatory primer; rarely written for non-issuers | Low | Definitional |
| 14 | Single-family vs multifamily fractional | Property-type comparison inside the asset class | Low | Medium |
| 15 | Real estate debt platforms vs equity fractional | Groundfloor-style debt vs Arrived-style equity | Low | Medium |
| 16 | How fractional real estate is taxed (K-1 deep dive) | Tax complexity is a known reader pain point | Low-Med | 590+ (tax keywords) |
| 17 | Fractional real estate platform fees comparison | Fee transparency varies widely; comparison is rare | Low | Medium |
| 18 | What is a real estate operating agreement | LLC-specific deep dive for due diligence | Low | Definitional |
| 19 | How to read a Reg A offering circular | Practical due-diligence guide; no good resource | Low | Definitional |
| 20 | Tokenized real estate vs traditional fractional | Lofty/Algorand vs Reg A LLC structural compare | Low | Medium |
| 21 | Fractional real estate IRA / self-directed IRA | Tax-advantaged path; complex but high-intent | Low-Med | Medium |
| 22 | Real estate vs index funds for retirement | Asset allocation framing; pulls in retirement readers | Med | High |
| 23 | What happens when a fractional property is sold | Exit mechanics; consumer pain point | Low | Definitional |

International / Gulf / UAE gaps are documented in git history but are out of scope under the current US-only operating posture.

**Pool status (2026-05-14):** Items 1-7 published or in pipeline. Items 9-10 published as Stage -2 generations. Items 8, 11-23 remain as future candidates. When the pool drops below 3 unused items, regenerate the gap list via Stage -3 or operator-led SERP audit.

---

## Step 3 - Priority Blog Posts (Phase 1)

Ranked by: gap size + KD + PSFnetwork ICP alignment + pipeline feasibility. Used by Stage -1 topic selection.

| Priority | Slug | Target Keyword | Vol | KD | Type |
|----------|------|---------------|-----|----|------|
| 1 | fractional-real-estate-investing | fractional real estate investing | 880 | 35 | Hub |
| 2 | how-to-build-passive-income-with-real-estate | passive income real estate | 320 | 10 | Spoke |
| 3 | reits-vs-fractional-real-estate | fractional real estate vs reit | Low-comp | ~20 | Spoke |
| 4 | how-to-invest-in-real-estate-with-100 | how to invest in real estate with little money | 110 | 22 | Spoke |
| 5 | best-fractional-real-estate-platforms | best fractional real estate platforms | 590 | 33 | Spoke |
| 6 | what-is-proptech | proptech news | 14,800 | 31 | Spoke |

Hub-before-spoke dependency: Priority 1 must publish before Priorities 2-6 since each spoke links back to the hub.

---

## Step 4 - Template Structure (from PSFnetwork blog template)

See `brand/template-structure.md` for the canonical component order. The pipeline produces drafts that map cleanly onto these components.

### Chart and table rules

- File format: `.tsx` (Framer-compatible TypeScript)
- File name: `[slug]-chart.tsx` (or `[slug]-table-N.tsx` for multiples)
- Location: `blog/[slug]/`
- Component: default export, self-contained, no external chart library, SVG rendering
- Brand tokens inline: `#FF7141` rust, `#4F8FA3` teal, `#1C1C1C` ink, `#F7F5F0` cream
- Component name: PascalCase from slug + Chart or Table suffix
- Typed props interface (Framer Code Components expect it)

---

## Pipeline Execution Order (v2)

For each post the pipeline runs:

```
[-1] Topic selection             (only if no slug provided)
[0]  State check
[1]  Research & evidence
[2]  Draft
[3]  Expert + editorial review   (dynamic panel: SEC, FINRA, CFPB, Editorial default)
[4]  Revision
[5]  Localization                (no-op while target_markets = ['EN-US'])
[6]  Expert re-check             (no-op if Stage 5 was a no-op)
[7]  Pre-publish QA              (routes by failure type, not blanket restart)
[8]  Publish (GitHub commit)
[9]  Client delivery (Google Drive)
[10] Post-publish QA             (deferred until live URL exists)
```

Full stage definitions in `workflow/pipeline.md`. Trigger and authorization rules in `workflow/trigger-contract.md`.

---

## Phase 1 Execution Tracker

| Slug | Brief | Outline | S1 Research | S2 Draft | S3 Review | S4 Revise | S7 QA | S8 Publish | S9 Drive | Status |
|------|-------|---------|-------------|----------|-----------|-----------|-------|------------|----------|--------|
| fractional-real-estate-investing | done | done | - | - | - | - | - | - | - | Ready |
| how-to-build-passive-income-with-real-estate | done | done | - | - | - | - | - | - | - | Queued |
| reits-vs-fractional-real-estate | done | done | - | - | - | - | - | - | - | Queued |
| how-to-invest-in-real-estate-with-100 | done | done | - | - | - | - | - | - | - | Queued |
| best-fractional-real-estate-platforms | done | done | - | - | - | - | - | - | - | Queued |
| what-is-proptech | done | done | - | - | - | - | - | - | - | Queued |

Status values: `Ready`, `Queued`, `In-flight`, `Rewrite-required`, `Manual-review-required`, `Published`.
