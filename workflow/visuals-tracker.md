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
| 2 | how-to-build-passive-income-with-real-estate | Capital to income ladder at 7% | + | 99.0 | |
| 3 | reits-vs-fractional-real-estate | REIT vs fractional, liquidity against choice | + | 95.5 | |
| 4 | best-fractional-real-estate-platforms | 8 platforms, minimum bars + structure table | + | 99.3 | |
| 5 | fractional-real-estate-investing | Fractional vs whole property, 7 dimensions | + | 98.4 | |
| 6 | how-to-invest-10k-in-real-estate | 3 structures, 3 different failure modes | + | 94.1 | |
| 7 | how-to-invest-in-real-estate-with-100 | 4 ways in at $100, tax form focus | + | 94.3 | |
| 8 | real-estate-crowdfunding-vs-fractional | Category vs subset, equity against debt | + | 99.0 | |
| 9 | 90-percent-millionaires-real-estate | Claim vs research, myth panel | + | 100.0 | |
| 10 | how-fractional-real-estate-is-taxed | K-1 flow in 4 steps | + | 95.4 | |
| 11 | reg-a-vs-reg-d-for-fractional-investors | Two frameworks, who gets to invest | + | 98.6 | |
| 12 | what-is-proptech | Market size + AI adoption 5 to 92% | + | 94.6 | |

Batch 1: 12 of 12 produced.

## Notes

- Every figure in every visual traces to the article body. No new claims.
- Palette floor is 48 colours, PSNR-verified at 53+ dB on the densest
  visuals. Below 48, re-measure before shipping.
- 90-percent-millionaires landed at exactly 100.0 KB, inside budget.
- Deliverables are mirrored to ~/Desktop/psfnetwork-paste-kit/visuals/
  for Framer entry.

## Batch 2 (not started)

Visuals for the 15 June-2026 articles follow once Batch 1 is placed in
Framer. Same stylesheet, same tracker format, rows to be added here.
