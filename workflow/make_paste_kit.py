#!/usr/bin/env python3
"""
Build paste-ready HTML files for manual Framer entry.

The Framer API is not available, so articles are transferred by copy-paste.
Pasting from Google Docs has been losing every hyperlink (see
workflow/live-site-audit-2026-07-21.md, finding 2). These files give a clean
alternative source: minimal semantic HTML with real anchors, rendered in a
browser, with a button that selects and copies only the article body.

Usage:
    python3 workflow/make_paste_kit.py --out ~/Desktop/psfnetwork-paste-kit
    python3 workflow/make_paste_kit.py --out DIR --slug proptech-future-of-real-estate

Each article produces one HTML file containing:
  - an SEO panel with the fields that must be typed into Framer by hand
    (title, slug, meta description, canonical, hero alt), each with its own
    copy button and a character count
  - a "Copy article body" button that puts rich HTML on the clipboard
  - the rendered body, with the Production Notes block excluded

An index.html links to all of them and tracks which are done.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOG = REPO / 'blog'

# The notes heading may be plain or wrapped in bold, depending on how the
# source Google Doc styled it. Tolerate both.
PROD_NOTES_RE = re.compile(
    r'^\s*\**\s*PRODUCTION NOTES.*?(?=^#\s)', re.MULTILINE | re.DOTALL
)


YAML_FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.DOTALL)


def split_notes(md: str):
    """Return (metadata_block, body_markdown).

    Batch 1 drafts carry YAML frontmatter. Batch 2 drafts, which came out of
    Google Docs, carry a PRODUCTION NOTES bullet list instead. Handle both.
    """
    m = YAML_FM_RE.match(md)
    if m:
        return m.group(1), md[m.end():]
    m = PROD_NOTES_RE.search(md)
    if not m:
        return '', md
    return m.group(0), md[m.end():]


# Field labels are inconsistent across the June 2026 batch. Normalise them.
ALIASES = {
    'title tag (seo)': 'title', 'meta title (seo)': 'title', 'meta title': 'title',
    'title tag': 'title', 'title': 'title',
    'meta description': 'meta_description', 'meta desc': 'meta_description',
    'description': 'meta_description',
    'slug': 'slug',
    'canonical url': 'canonical', 'canonical': 'canonical',
    'hero visual alt text': 'hero_alt', 'hero alt': 'hero_alt',
    'hero image alt': 'hero_alt', 'hero alt text': 'hero_alt',
    'focus keyword': 'focus_keyword',
    'author': 'author', 'reviewer': 'reviewer', 'read time': 'read_time',
    # YAML frontmatter keys used by Batch 1 drafts
    'meta_description': 'meta_description', 'hero_visual_alt': 'hero_alt',
    'focus_keyword': 'focus_keyword', 'read_time': 'read_time',
}


def parse_notes(notes: str) -> dict:
    """Pull SEO fields out of the Production Notes list.

    Handles two quirks in the June 2026 batch: label wording varies between
    articles, and some lines pack two fields separated by a middle dot.
    """
    out = {}
    for line in notes.split('\n'):
        line = line.strip()
        if not line:
            continue
        if not line.startswith('-'):
            # YAML frontmatter form: key: value
            m = re.match(r'([a-z_]{3,25}):\s*(.+)', line)
            if m:
                key = ALIASES.get(m.group(1).strip().lower())
                if key and key not in out:
                    out[key] = m.group(2).strip().strip('"')
            continue
        line = line.lstrip('-').strip()
        for chunk in re.split(r'\s+·\s+', line):
            m = re.match(r'([^:]{2,40}):\s*(.+)', chunk.strip())
            if not m:
                continue
            # Labels may be bolded ("**Meta description:** ..."); the go-live
            # QA on 2026-08-11 found six drafts whose fields silently parsed
            # to nothing because of the asterisks. Strip them from both sides.
            key = ALIASES.get(m.group(1).strip().strip('*').strip().lower())
            if key and key not in out:
                out[key] = m.group(2).strip().lstrip('*').strip()
    return out


def inline(text: str) -> str:
    """Convert inline markdown (links, bold, italic) to HTML."""
    text = html.escape(text, quote=False)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
                  text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    return text


def md_to_html(md: str) -> str:
    """Minimal markdown to HTML for headings, paragraphs, lists, tables."""
    lines = md.split('\n')
    out, i = [], 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        # table
        if line.lstrip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            head = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2
            body = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                body.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            out.append('<table><thead><tr>' +
                       ''.join(f'<th>{inline(c)}</th>' for c in head) +
                       '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body) +
                       '</tbody></table>')
            continue

        # horizontal rule, used as a section separator in the drafts
        if re.match(r'^-{3,}$', line.strip()):
            i += 1
            continue

        # blockquote
        if line.lstrip().startswith('>'):
            quote = []
            while i < len(lines) and lines[i].lstrip().startswith('>'):
                quote.append(re.sub(r'^\s*>\s?', '', lines[i].rstrip()))
                i += 1
            out.append(f'<blockquote><p>{inline(" ".join(quote).strip())}</p></blockquote>')
            continue

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>')
            i += 1
            continue

        # unordered list
        if re.match(r'^\s*[-*]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append(inline(re.sub(r'^\s*[-*]\s+', '', lines[i].rstrip())))
                i += 1
            out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>')
            continue

        # ordered list
        if re.match(r'^\s*\d+\.\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append(inline(re.sub(r'^\s*\d+\.\s+', '', lines[i].rstrip())))
                i += 1
            out.append('<ol>' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>')
            continue

        # paragraph
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,6}\s|\s*[-*]\s|\s*\d+\.\s|\s*\|)', lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append(f'<p>{inline(" ".join(buf))}</p>')

    return '\n'.join(out)


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{slug} · paste kit</title>
<style>
:root{{--cream:#F7F5F0;--ink:#1C1C1C;--orange:#FF7141;--blue:#4F8FA3;--line:#1C1C1C22}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cream);color:var(--ink);
 font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}}
.wrap{{max-width:860px;margin:0 auto;padding:32px 24px 80px}}
.bar{{position:sticky;top:0;background:var(--cream);padding:14px 0;border-bottom:1px solid var(--line);
 display:flex;gap:10px;align-items:center;flex-wrap:wrap;z-index:5}}
.bar a{{color:var(--blue);font-size:13px;text-decoration:none}}
button{{background:var(--orange);color:#fff;border:0;border-radius:7px;padding:9px 15px;
 font-size:14px;font-weight:600;cursor:pointer;font-family:inherit}}
button:hover{{opacity:.9}}
button.ghost{{background:#fff;color:var(--ink);border:1px solid var(--line);padding:4px 10px;font-size:12px;font-weight:500}}
.panel{{background:#fff;border:1px solid var(--line);border-radius:11px;padding:20px;margin:22px 0}}
.panel h2{{margin:0 0 4px;font-size:15px}}
.panel .hint{{margin:0 0 16px;font-size:13px;color:#1C1C1C99}}
.f{{display:grid;grid-template-columns:150px 1fr auto;gap:10px;align-items:start;
 padding:9px 0;border-top:1px solid #1C1C1C11}}
.f:first-of-type{{border-top:0}}
.f .k{{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#1C1C1C99;padding-top:3px}}
.f .v{{font-size:14px;word-break:break-word}}
.count{{font-size:11px;color:#1C1C1C88;margin-left:6px;white-space:nowrap}}
.count.bad{{color:var(--orange);font-weight:600}}
.links{{background:#fff;border:1px solid var(--line);border-radius:11px;padding:20px;margin:22px 0}}
.links table{{width:100%;border-collapse:collapse;font-size:13px}}
.links td{{padding:6px 8px;border-top:1px solid #1C1C1C11;vertical-align:top}}
.links td:first-child{{font-weight:600;width:45%}}
#body{{background:#fff;border:1px solid var(--line);border-radius:11px;padding:32px 34px}}
#body h1{{font-size:30px;line-height:1.2;margin:0 0 18px}}
#body h2{{font-size:22px;margin:32px 0 10px}}
#body h3{{font-size:17px;margin:24px 0 8px}}
#body p{{margin:0 0 14px}}
#body a{{color:var(--blue)}}
#body table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}}
#body th,#body td{{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}}
#body th{{background:var(--cream);font-weight:600}}
#body ul,#body ol{{margin:0 0 14px;padding-left:22px}}
#body blockquote{{margin:18px 0;padding:14px 20px;border-left:3px solid var(--orange);
 background:var(--cream);border-radius:0 8px 8px 0;font-style:italic}}
#body blockquote p{{margin:0}}
#body li{{margin:0 0 6px}}
.ok{{color:var(--blue);font-weight:600;font-size:13px}}
</style></head><body><div class="wrap">

<div class="bar">
  <button onclick="copyBody()">Copy article body</button>
  <span id="msg" class="ok"></span>
  <span style="flex:1"></span>
  <a href="index.html">All articles</a>
</div>

<div class="panel">
  <h2>SEO fields, type these into Framer by hand</h2>
  <p class="hint">These are not part of the body. Meta description is empty on all 13 live articles, so this panel exists to stop that repeating.</p>
  {fields}
</div>

{linkpanel}

<div id="body">
{body}
</div>

<script>
function flash(t){{var m=document.getElementById('msg');m.textContent=t;setTimeout(function(){{m.textContent=''}},2200)}}
function copyBody(){{
  var el=document.getElementById('body');
  var r=document.createRange();r.selectNodeContents(el);
  var s=window.getSelection();s.removeAllRanges();s.addRange(r);
  try{{document.execCommand('copy');flash('Copied with formatting and links. Paste into Framer now.')}}
  catch(e){{flash('Copy failed, select manually')}}
}}
function copyText(t,label){{
  navigator.clipboard.writeText(t).then(function(){{flash(label+' copied')}});
}}
</script>
</div></body></html>
"""


def field_row(label, value, key=''):
    limits = {'title': (55, 60), 'meta_description': (150, 160)}
    n = len(value)
    cls, note = '', ''
    if key in limits:
        lo, hi = limits[key]
        cls = '' if lo <= n <= hi else ' bad'
        note = f'{n} chars, target {lo}-{hi}'
    else:
        note = f'{n} chars'
    esc = html.escape(value)
    js = json.dumps(value)
    return (f'<div class="f"><div class="k">{html.escape(label)}</div>'
            f'<div class="v">{esc}<span class="count{cls}">{note}</span></div>'
            f'<button class="ghost" onclick=\'copyText({js},"{html.escape(label)}")\'>copy</button></div>')


def build(slug: str, out_dir: Path) -> dict:
    # Prefer a humanized v2 when one exists.
    src = BLOG / slug / 'draft-v2-humanized.md'
    if not src.exists():
        src = BLOG / slug / 'draft.md'
    md = src.read_text(encoding='utf-8')
    notes_raw, body_md = split_notes(md)
    notes = parse_notes(notes_raw)

    wanted = [('title', 'Title tag (SEO)'), ('slug', 'Slug'),
              ('meta_description', 'Meta description'), ('canonical', 'Canonical URL'),
              ('hero_alt', 'Hero image alt'), ('focus_keyword', 'Focus keyword'),
              ('author', 'Author'), ('reviewer', 'Reviewer'), ('read_time', 'Read time')]
    required = {'title', 'meta_description', 'slug', 'canonical'}
    rows, missing = [], []
    for key, label in wanted:
        if key in notes:
            rows.append(field_row(label, notes[key], key))
        elif key in required:
            missing.append(label)
            rows.append(
                f'<div class="f"><div class="k">{label}</div>'
                f'<div class="v" style="color:#FF7141;font-weight:600">'
                f'NOT WRITTEN, needs to be authored before this article ships</div>'
                f'<div></div></div>')
    fields = ''.join(rows)

    body_html = md_to_html(body_md)

    links = re.findall(r'\[([^\]]+)\]\((https://www\.psfnetwork\.com/blog/[a-z0-9-]+)\)', body_md)
    if links:
        rows = ''.join(
            f'<tr><td>{html.escape(a)}</td><td>{html.escape(u.replace("https://www.psfnetwork.com",""))}</td></tr>'
            for a, u in links)
        linkpanel = (f'<div class="links"><h2 style="margin:0 0 4px;font-size:15px">'
                     f'Internal links in this article ({len(links)})</h2>'
                     f'<p class="hint">If the paste drops them, add these back in Framer. '
                     f'Find the anchor text, select it, apply the link.</p>'
                     f'<table>{rows}</table></div>')
    else:
        linkpanel = ''

    page = PAGE.format(slug=html.escape(slug), fields=fields, body=body_html, linkpanel=linkpanel)
    (out_dir / f'{slug}.html').write_text(page, encoding='utf-8')

    return {'slug': slug, 'title': notes.get('title') or slug,
            'links': len(links), 'meta_len': len(notes.get('meta_description', '')),
            'missing': missing}


INDEX = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>PSFnetwork paste kit</title>
<style>
:root{{--cream:#F7F5F0;--ink:#1C1C1C;--orange:#FF7141;--blue:#4F8FA3;--line:#1C1C1C22}}
body{{margin:0;background:var(--cream);color:var(--ink);
 font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}}
.wrap{{max-width:900px;margin:0 auto;padding:44px 24px 80px}}
h1{{font-size:28px;margin:0 0 6px}}
.sub{{color:#1C1C1C99;margin:0 0 28px;font-size:15px}}
table{{width:100%;border-collapse:collapse;background:#fff;
 border:1px solid var(--line);border-radius:11px;overflow:hidden}}
th,td{{padding:11px 14px;text-align:left;border-top:1px solid var(--line);font-size:14px}}
th{{background:var(--cream);font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#1C1C1C99;border-top:0}}
a{{color:var(--blue);text-decoration:none;font-weight:600}}
a:hover{{text-decoration:underline}}
.n{{text-align:right;color:#1C1C1C99}}
.live{{color:var(--orange);font-weight:600;font-size:12px}}
.note{{background:#fff;border:1px solid var(--line);border-left:3px solid var(--orange);
 border-radius:9px;padding:16px 18px;margin:0 0 26px;font-size:14px}}
</style></head><body><div class="wrap">
<h1>PSFnetwork paste kit</h1>
<p class="sub">Batch 2, {n} articles. Open one, click "Copy article body", paste into Framer.</p>
<div class="note"><strong>Two of these are already live with the old content:</strong>
how-to-choose-fractional-real-estate-platform and proptech-future-of-real-estate.
Update those first. Every live article is also missing its meta description, so
fill that field from the SEO panel while you are in there.</div>
<table><tr><th>Article</th><th>Slug</th><th class="n">Links</th><th class="n">Meta</th></tr>
{rows}
</table>
</div></body></html>
"""

# Articles already published on psfnetwork.com, per the 2026-07-21 sitemap audit.
LIVE = {
    'how-to-choose-fractional-real-estate-platform', 'proptech-future-of-real-estate',
    'fractional-real-estate-investing', '90-percent-millionaires-real-estate',
    'best-fractional-real-estate-platforms', 'how-fractional-real-estate-is-taxed',
    'how-to-build-passive-income-with-real-estate', 'how-to-invest-10k-in-real-estate',
    'how-to-invest-in-real-estate-with-100', 'real-estate-crowdfunding-vs-fractional',
    'reg-a-vs-reg-d-for-fractional-investors', 'square-foot-real-estate-ownership-explained',
    'what-is-proptech',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--slug', action='append',
                    help='Limit to specific slugs. Repeatable. Default: all Batch 2.')
    args = ap.parse_args()

    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    if args.slug:
        slugs = args.slug
    else:
        # Default scope: everything ready for Framer entry. That means any
        # article with a humanized v2, plus the Batch 2 set, which arrived
        # from Google Docs with a PRODUCTION NOTES block.
        ready = {p.parent.name for p in BLOG.glob('*/draft-v2-humanized.md')}
        ready |= {p.parent.name for p in BLOG.glob('*/draft.md')
                  if 'PRODUCTION NOTES' in p.read_text(encoding='utf-8')[:3000]}
        slugs = sorted(ready)

    results = []
    for s in slugs:
        if not (BLOG / s / 'draft.md').exists():
            print(f'  skip, no draft: {s}', file=sys.stderr)
            continue
        results.append(build(s, out))
        print(f'  {s}')

    rows = ''.join(
        f'<tr><td><a href="{r["slug"]}.html">{html.escape(r["title"])}</a>'
        f'{" <span class=live>LIVE</span>" if r["slug"] in LIVE else ""}</td>'
        f'<td>{r["slug"]}</td><td class="n">{r["links"]}</td>'
        f'<td class="n">{("<span style=color:#FF7141;font-weight:600>missing</span>" if r["missing"] else r["meta_len"])}</td></tr>'
        for r in results)
    (out / 'index.html').write_text(INDEX.format(n=len(results), rows=rows), encoding='utf-8')

    print(f'\n{len(results)} files + index.html in {out}')


if __name__ == '__main__':
    main()
