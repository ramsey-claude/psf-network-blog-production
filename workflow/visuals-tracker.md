# Article Visuals Tracker

One row per article, nothing ships unnoticed. A plus in "Produced" means the
HTML source, the PNG and the sub-100 KB WebP all exist in the article folder.
"In Framer" is marked by the operator after the image is actually placed.

Regenerate any visual with:

    python3 workflow/render_visual.py blog/<slug>/<slug>-visual-01.html --max-kb 100

Shared styling lives in `workflow/visual-base.css`. Change it there and
re-render; every visual picks it up.

## Batch 1

| # | Article | Visual concept | Produced | WebP KB | In Framer |
|---|---------|----------------|:--------:|--------:|:---------:|
| 1 | square-foot-real-estate-ownership-explained | 1,200-cell grid, your 50 sq ft, share vs sq-ft table | + | 94.0 | + |
| 2 | how-to-build-passive-income-with-real-estate | Capital to income ladder at 7% | + | 99.0 | + |
| 3 | reits-vs-fractional-real-estate | REIT vs fractional, liquidity against choice | + | 95.5 | |
| 4 | best-fractional-real-estate-platforms | 8 platforms, minimum bars + structure table | + | 99.3 | + |
| 5 | fractional-real-estate-investing | Fractional vs whole property, 7 dimensions | + | 98.4 | + |
| 6 | how-to-invest-10k-in-real-estate | 3 structures, 3 different failure modes | + | 94.1 | + |
| 7 | how-to-invest-in-real-estate-with-100 | 4 ways in at $100, tax form focus | + | 94.3 | + |
| 8 | real-estate-crowdfunding-vs-fractional | Category vs subset, equity against debt | + | 99.0 | + |
| 9 | 90-percent-millionaires-real-estate | Claim vs research, myth panel | + | 100.0 | + |
| 10 | how-fractional-real-estate-is-taxed | K-1 flow in 4 steps | + | 95.4 | + |
| 11 | reg-a-vs-reg-d-for-fractional-investors | Two frameworks, who gets to invest | + | 98.6 | + |
| 12 | what-is-proptech | Market size + AI adoption 5 to 92% | + | 94.6 | + |

Batch 1: 12 of 12 produced. 11 of 12 placed in Framer.

## Notes

- Every figure in every visual traces to the article body. No new claims.
- Palette floor is 48 colours, PSNR-verified at 53+ dB on the densest
  visuals. Below 48, re-measure before shipping.
- 90-percent-millionaires landed at exactly 100.0 KB, inside budget.
- Deliverables are mirrored to ~/Desktop/psfnetwork-paste-kit/visuals/
  for Framer entry.
- reits-vs-fractional is the only visual not yet placed. Its article is
  also the only Batch 1 article not published on the live site (absent
  from sitemap.xml, see workflow/live-site-audit-2026-07-21.md). The
  visual is ready; publish package (paste-kit HTML + WebP + PNG) was
  prepared and handed to the operator on 2026-08-11. Both go in together
  when the article ships. That
  publish also closes the 10 dead internal links pointing at the slug.

## Batch 2 (covers replaced 2026-08-18)

This section said "not started" until 2026-08-17, which was wrong and cost
real time: it was read as fact during the Framer import and the operator was
told Batch 2 had no hero images to upload. The operator corrected it, and a
Drive search confirmed all 15 covers exist and have since 2026-07-29.

They are **cover images, not the in-body visuals** Batch 1 has. Batch 1's
rows above track a rendered explanatory graphic per article, produced from
an HTML source in the article folder via `render_visual.py`, with PNG and
WebP beside it. Batch 2's covers are 1200x630 WebP files that live only in
each article's Drive folder, named `cover-<slug>-1200x630.webp`. No HTML
source and no repo copy, so `render_visual.py` cannot regenerate them.

Two consequences worth stating plainly. The covers are the Framer Hero Image
and nothing else; a Batch 2 article still has no in-body graphic, which is a
real gap against Batch 1. And because the only copy is in Drive, the
no-delete rule matters here as much as it does for the docs.

Hero Image turned out to be CSV-importable after all, which the first pass
here assumed it was not. `framer_batch_csv.py` sends a Drive URL and Framer
fetches the file and re-hosts it: the live og:image is a framerusercontent
asset and the pages do not hotlink Drive. All 15 were placed this way on
2026-08-17, none by hand.

Covers were replaced on 2026-08-18. The July set had its headlines set at
about x=180, inside the listing card's 143 px side crop, so every one read
mid-word on /blog. The replacements are composed to
`brand/cover-image-spec.md`. Sizes below are the new files.

Each article folder now holds exactly one image; the July originals moved to
that folder's `old version` subfolder. A set of PNG "-v2" files from the same
night also sits in those archive folders and is not the live set.

| # | Article | KB (Jul) | KB (Aug 18) | In Framer |
|---|---------|---------:|------------:|:---------:|
| 13 | how-to-sell-fractional-real-estate | 38 | 62 | |
| 15 | real-estate-etfs-vs-fractional | 31 | 71 | |
| 16 | real-estate-vs-index-funds-retirement | 83 | 106 | |
| 19 | single-family-vs-multifamily-fractional | 92 | 106 | |
| 26 | fractional-real-estate-vs-other-investments | 95 | 127 | |
| 27 | legal-tax-guide-fractional-real-estate | 14 | 14 | |
| 29 | proptech-future-of-real-estate | 18 | 72 | |
| - | debt-vs-equity-fractional | 17 | 18 | |
| - | fractional-real-estate-ira | 81 | 123 | |
| - | how-to-choose-fractional-real-estate-platform | 29 | 64 | |
| - | how-to-read-reg-a-offering-circular | 16 | 17 | |
| - | proptech-trends-2026 | 68 | 88 | |
| - | real-estate-as-an-asset-class | 20 | 76 | |
| - | reit-dividend-taxation | 57 | 73 | |
| - | tokenized-vs-traditional-fractional | 93 | 116 | |

Twelve of the fifteen gained weight, which is what a recomposed frame should
do. Three did not: legal-tax-guide at 14 KB, how-to-read-reg-a at 17 KB and
debt-vs-equity at 18 KB are all under the spec's 60 KB floor and are within a
kilobyte of their July sizes. Either they are flat art that genuinely
compresses that small, or they were re-exported at the old quality. Worth a
look before the next batch adopts these settings.

Drive folder numbers are filled in only where this repo has recorded them
(see the operator's numbering directive, incident-log 2026-08-14). The rest
are known by slug; look the folder up rather than guessing a number.

## Cover composition

Full production spec: **`brand/cover-image-spec.md`**.

The short version, found 2026-08-17 after Batch 2 went live with its
headlines cut off on the listing. The card container is 1.44928 and a
1200x630 cover is 1.90476, so `object-fit: cover` with `object-position:
center` discards **143 px from each side**, 12% of the width. Batch 2's
covers set their headline at about x=180, just inside that line.

Keep every word inside **x = 200 to x = 1000**. Nothing is lost vertically.

Batch 1 escapes it because its covers are charts composed centrally. It is
not a WebP problem, though the format split is real: Batch 1 is PNG and
Batch 2 is WebP.

## Batch 3 (cover images done, in Drive only)

Same situation, found in the same 2026-08-17 sweep. All 9 covers exist,
created 2026-08-04, same naming and same 1200x630 WebP form, Drive only.
Batch 3 has not been opened for work yet, so these rows exist to record that
the assets are there and nothing needs producing.

| Article | Cover in Drive | KB | In Framer |
|---------|:--------------:|---:|:---------:|
| diversifying-across-fractional-platforms | + | 83 | |
| fractional-real-estate-401k-rollover | + | 37 | |
| fractional-real-estate-for-retirees | + | 17 | |
| fractional-real-estate-high-income-earners | + | 36 | |
| fractional-real-estate-vs-bonds | + | 23 | |
| how-to-verify-fractional-real-estate-platform | + | 38 | |
| questions-to-ask-fractional-platform | + | 12 | |
| red-flags-fractional-offering-circular | + | 31 | |
| reinvesting-fractional-real-estate-distributions | + | 12 | |
