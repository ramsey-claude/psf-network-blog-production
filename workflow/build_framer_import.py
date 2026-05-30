#!/usr/bin/env python3
"""Build a Framer-ready import set from the blog drafts.

Reads every ``blog/*/draft.md``, splits its YAML frontmatter from the markdown
body, strips production-only markers, and emits two things into
``framer-export/``:

1. ``framer-import.csv`` - one row per post, columns map 1:1 to Framer CMS
   collection fields. Import this directly via the Framer CMS "Import CSV"
   button.
2. ``bodies/<slug>.md`` - the cleaned markdown body for each post. Open the
   file, copy everything, and paste it into the post's rich-text field in
   Framer. Framer converts pasted markdown into formatted blocks
   (headings, bold, lists, links) automatically.

Cleaning rules applied to the body:
  - the leading ``# H1`` is lifted out into the ``display_title`` column
    (the CMS title field renders the on-page H1, so we avoid a duplicate)
  - the ``**Dek:**`` line is lifted into the ``dek`` column (subtitle field)
  - ``[VISUAL-HERO-01]`` placeholders are removed (the hero image is a
    separate CMS image field; alt text is kept in ``hero_visual_alt``)
  - the standalone ``**Stat cards:**`` label is removed but its bullet list
    is kept as real content
  - runs of blank lines / leading separators are collapsed

No wording inside the posts is changed.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
OUT = ROOT / "framer-export"
BODIES = OUT / "bodies"

# Order of columns in the CSV. The first 16 are scalar fields; "content"
# carries the cleaned markdown body for anyone who prefers a single-file import.
COLUMNS = [
    "slug",
    "title",
    "display_title",
    "dek",
    "type",
    "topic",
    "author",
    "reviewer",
    "read_time",
    "published",
    "updated",
    "focus_keyword",
    "secondary_keywords",
    "meta_description",
    "canonical",
    "hero_visual_alt",
    "content",
]


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_block, body) for a ``---`` fenced document."""
    if not text.startswith("---"):
        raise ValueError("no frontmatter fence found")
    end = text.index("\n---", 3)
    fm = text[3:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    return fm, body


def parse_frontmatter(fm: str) -> dict[str, str]:
    """Minimal YAML reader: ``key: value`` plus ``- item`` list members.

    Sufficient for these drafts; avoids a PyYAML dependency.
    """
    data: dict[str, str] = {}
    current_list_key: str | None = None
    items: list[str] = []
    for raw in fm.splitlines():
        if re.match(r"^\s*-\s+", raw):
            items.append(re.sub(r"^\s*-\s+", "", raw).strip().strip('"'))
            continue
        if current_list_key is not None:
            data[current_list_key] = ", ".join(items)
            current_list_key, items = None, []
        m = re.match(r"^([a-z_]+):\s*(.*)$", raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            current_list_key = key
        else:
            data[key] = val.strip().strip('"')
    if current_list_key is not None:
        data[current_list_key] = ", ".join(items)
    return data


def clean_body(body: str) -> tuple[str, str, str]:
    """Return (cleaned_body, display_title, dek)."""
    display_title = ""
    dek = ""
    out: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not display_title and stripped.startswith("# "):
            display_title = stripped[2:].strip()
            continue
        if stripped.startswith("**Dek:**"):
            dek = stripped[len("**Dek:**") :].strip()
            continue
        if stripped == "[VISUAL-HERO-01]":
            continue
        if stripped == "**Stat cards:**":
            continue
        out.append(line)

    text = "\n".join(out)
    # Drop a leading horizontal rule left dangling after the H1/dek removal.
    text = re.sub(r"\A\s*(?:---\s*\n)+", "", text)
    # Collapse 3+ blank lines into a single blank line.
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text, display_title, dek


def main() -> None:
    BODIES.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    for draft in sorted(BLOG.glob("*/draft.md")):
        fm, body = split_frontmatter(draft.read_text(encoding="utf-8"))
        meta = parse_frontmatter(fm)
        cleaned, display_title, dek = clean_body(body)

        slug = meta.get("slug", draft.parent.name)
        (BODIES / f"{slug}.md").write_text(cleaned, encoding="utf-8")

        rows.append(
            {
                "slug": slug,
                "title": meta.get("title", ""),
                "display_title": display_title,
                "dek": dek,
                "type": meta.get("type", ""),
                "topic": meta.get("topic", ""),
                "author": meta.get("author", ""),
                "reviewer": meta.get("reviewer", ""),
                "read_time": meta.get("read_time", ""),
                "published": meta.get("published", ""),
                "updated": meta.get("updated", ""),
                "focus_keyword": meta.get("focus_keyword", ""),
                "secondary_keywords": meta.get("secondary_keywords", ""),
                "meta_description": meta.get("meta_description", ""),
                "canonical": meta.get("canonical", ""),
                "hero_visual_alt": meta.get("hero_visual_alt", ""),
                "content": cleaned,
            }
        )

    csv_path = OUT / "framer-import.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {csv_path.relative_to(ROOT)} ({len(rows)} posts)")
    print(f"Wrote {len(rows)} body files to {BODIES.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
