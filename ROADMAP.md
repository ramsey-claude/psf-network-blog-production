# psfnetwork Blog Production — Master Roadmap

Last updated: May 2026

---

## Step 0 — Repository Structure

Every blog post lives at:

```
blog/
└── [post-slug]/
    ├── brief.md              Keyword targets, audience, angle, competitors
    ├── outline.md            Section-by-section content plan
    ├── draft.md              Full content draft (pipeline output)
    ├── expert-reviews/       One .md per expert, Stage 1 + Stage 4
    ├── localization-notes.md Stage 3 output
    └── [slug]-chart.jsx      Framer component (if charts/tables present)
```

---

## Step 1 — Competitor Top Traffic Pages (Semrush, May 2026)

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

**Pattern:** Brand traffic dominates (73%). Education content (REITs 101, investing guide) drives the rest. No programmatic content.

### Arrived
| URL | Traffic | Pattern |
|-----|---------|---------|
| arrived.com/ | 34,381 | Homepage (brand) |
| /blog/section-8 | 192 | Niche topic |
| /blog/how-to-finance-a-vacation-rental-property | 121 | Vacation rental |
| /blog/arbitrage | 116 | Arbitrage |
| /blog/fractional-real-estate-investing | 100 | Core topic |
| /blog/types-of-real-estate-investments | 92 | Education |

**Pattern:** Brand traffic dominates (92%). Blog drives ~7% of traffic. Niche topics (Section 8, arbitrage) outperform core topics.

### Mogul
| URL | Traffic | Pattern |
|-----|---------|---------|
| mogul.club/ | 1,924 | Homepage |
| /blogposts/what-is-steve-harveys-net-worth | 685 | Celebrity net worth |
| /blogposts/how-much-do-twitch-streamers-make | 492 | Pop culture |
| /blogposts/what-is-katt-williams-net-worth | 370 | Celebrity net worth |

**Pattern:** Celebrity/pop culture content drives most blog traffic — completely off-topic from their product. Only 1 comparison article (Arrived vs Fundrise) in top 20.

### Realbricks
| URL | Traffic | Pattern |
|-----|---------|---------|
| realbricks.com/ | 1,247 | Homepage |
| /articles/90-of-millionaires-own-real-estate | 763 | Stat-driven hook |
| /articles/how-to-invest-in-real-estate-with-100 | 581 | Low-barrier entry |
| /articles/why-is-princeton-texas-growing-so-fast | 385 | Local market |

**Pattern:** Stat-hook articles and low-barrier-entry content drive traffic. "90% of millionaires" and "$100 investing" articles are strongest.

### Lofty
| URL | Traffic | Pattern |
|-----|---------|---------|
| lofty.ai/ | 9,228 | Homepage (brand) |
| /reviews/groundfloor | 125 | Competitor review |
| /compare/fundrise-vs-arrived-homes | 39 | Comparison |

**Pattern:** Nearly all traffic is brand. Content almost nonexistent.

### Groundfloor
| URL | Traffic | Pattern |
|-----|---------|---------|
| groundfloor.com/ | 12,651 | Homepage (brand) |
| /blog/private-market-credit-opportunities | 41 | Thought leadership |
| /blog/market-trends-charlotte | 39 | Local market |

**Pattern:** Brand-heavy. Minimal content contribution.

---

## Step 2 — Content Gap Analysis: What Competitors Are NOT Covering

These are high-opportunity topics with search demand that none (or few) of the 10 competitors have substantive content on:

| # | Gap Topic | Why It's a Gap | Est. KD | Est. Volume |
|---|-----------|---------------|---------|-------------|
| 1 | International fractional real estate investing | All competitors are US-only. Zero content for non-US investors or US investors wanting international exposure | Low | Growing |
| 2 | Real estate investing for Gulf/UAE investors | No competitor targets this segment at all | Low | Untapped |
| 3 | Square-foot real estate ownership explained | Unique psfnetwork model - no competitor addresses this concept | Low | Definitional |
| 4 | Fractional real estate vs REIT (clear comparison) | Competitors mention both but no one owns the definitive comparison | Low-Med | 880+ |
| 5 | How to invest in real estate with $100 | Realbricks has it but weakly covered; strong keyword signal | Low | 581 traffic |
| 6 | 90% of millionaires own real estate — what that means for you | Realbricks drives 763 traffic with this hook; no other competitor has it | Low | High CTR hook |
| 7 | Passive income from real estate (beginner guide) | Covered broadly but no one owns a clean, definitive version | Low (10 KD) | 320 vol |
| 8 | Best fractional real estate platforms comparison | Every competitor avoids objective comparisons. psfnetwork can be neutral + honest | Med | 590+ |
| 9 | Proptech news and trends (evergreen) | 14,800 vol, KD 31 — Ark7/Arrived ignore this entirely | Low | 14,800 |
| 10 | REITs 101 for beginners | Fundrise has it (476 traffic) but it's old. GEO-optimized version is winnable | Med | 4,400+ |

---

## Step 3 — Priority Blog Posts (6 Posts, Phase 1)

Ranked by: gap size + KD + psfnetwork ICP alignment + pipeline feasibility

| Priority | Post Slug | Target Keyword | Vol | KD | Type |
|----------|-----------|---------------|-----|----|------|
| 1 | fractional-real-estate-investing | fractional real estate investing | 880 | 35 | Hub |
| 2 | how-to-build-passive-income-with-real-estate | passive income real estate | 320 | 10 | Spoke |
| 3 | reits-vs-fractional-real-estate | fractional real estate vs reit | Low-comp | ~20 | Spoke |
| 4 | how-to-invest-in-real-estate-with-100 | how to invest in real estate with little money | 110 | 22 | Spoke |
| 5 | best-fractional-real-estate-platforms | best fractional real estate platforms | 590 | 33 | Spoke |
| 6 | what-is-proptech | proptech news | 14,800 | 31 | Spoke |

---

## Step 4 — Template Structure (from psfnetwork-blog-template)

Every post must follow this component order, pulled from `blog-post.jsx`:

```
ReadingProgress bar
Nav
ArticleHero          (type tag, topic tag, h1, dek, author, dates, read time)
HeroVisual           (1200x630 illustration placeholder — [VISUAL-HERO-XX])
TOC (sticky sidebar) (section links + reviewer credit)
QuickAnswer          (60-second summary + 4 stat cards)
Opening              (2-paragraph hook, no headers)
[Section H2s]        (each: h2 in question format, answer capsule first 75 words, body, optional chart/pull quote)
FAQ                  (accordion, minimum 5 Q&As, schema-ready)
Sources              (numbered, linked)
AuthorCard           (name, credential, bio)
Disclaimer           (standard psfnetwork disclaimer)
CTABlock             (full-width, above footer)
Related              (3 related posts)
Footer
```

### Chart/Table Rules
- Every chart or table in a post gets a corresponding Framer JSX component
- File name: `[post-slug]-chart.jsx`
- Saved in: `blog/[post-slug]/[post-slug]-chart.jsx`
- Component must be self-contained (no external deps beyond React)
- Uses psfnetwork design tokens: `--rust (#FF7141)`, `--teal (#4F8FA3)`, `--ink (#1C1C1C)`, `--cream (#F7F5F0)`

---

## Pipeline Execution Order

For each post:

```
1. brief.md created (keyword targets, ICP, angle, competitor gap)
2. outline.md created (template-mapped section plan)
3. Stage 1: 8 expert reviews (expert-reviews/stage1-[expert].md)
4. Stage 2: draft.md revised based on expert feedback
5. Stage 3: localization-notes.md created
6. Stage 4: expert re-check (expert-reviews/stage4-[expert].md if triggered)
7. Stage 5: QA gate (checklist/qa-gate.md filled for post)
8. If chart/table: [slug]-chart.jsx created and committed
9. GitHub push with passing QA sign-off
```

---

## Phase 1 Execution Tracker

| Post | Brief | Outline | Stage 1 | Draft | L10n | Stage 4 | QA | Chart | Status |
|------|-------|---------|---------|-------|------|---------|-----|-------|--------|
| fractional-real-estate-investing | - | - | - | - | - | - | - | - | Planned |
| how-to-build-passive-income-with-real-estate | - | - | - | - | - | - | - | - | Planned |
| reits-vs-fractional-real-estate | - | - | - | - | - | - | - | - | Planned |
| how-to-invest-in-real-estate-with-100 | - | - | - | - | - | - | - | - | Planned |
| best-fractional-real-estate-platforms | - | - | - | - | - | - | - | - | Planned |
| what-is-proptech | - | - | - | - | - | - | - | - | Planned |
