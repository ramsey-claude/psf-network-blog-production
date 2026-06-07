#!/usr/bin/env python3
"""Render each cleaned body markdown to a standalone HTML file.

Framer's CMS rich-text editor does NOT parse raw markdown on paste - it inserts
it literally. But it DOES preserve structure when you paste *formatted* content
(text/html on the clipboard). So we render the bodies to HTML; the user opens
each .html in a browser, selects all, copies, and pastes into the Content field
with headings, bold, lists, and links intact.

Requires: pip install markdown
Output: framer-export/html/<slug>.html
"""
from __future__ import annotations

from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
BODIES = ROOT / "framer-export" / "bodies"
OUT = ROOT / "framer-export" / "html"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ max-width: 760px; margin: 40px auto; padding: 0 20px;
          font: 17px/1.6 -apple-system, Segoe UI, Roboto, sans-serif; color: #1c1c1c; }}
  h1,h2,h3 {{ line-height: 1.25; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for md_path in sorted(BODIES.glob("*.md")):
        html_body = markdown.markdown(
            md_path.read_text(encoding="utf-8"),
            extensions=["tables", "fenced_code", "sane_lists"],
        )
        slug = md_path.stem
        (OUT / f"{slug}.html").write_text(
            TEMPLATE.format(title=slug, body=html_body), encoding="utf-8"
        )
        count += 1
    print(f"Wrote {count} HTML files to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
