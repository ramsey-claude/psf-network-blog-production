# Breadcrumbs, 2026-08-29

Two layers, both live and verified:

1. **BreadcrumbList JSON-LD**, injected site-wide from Site Settings >
   Custom Code > End of head (the site's established pattern for schema).
   Builds Home > section > page from location.pathname; skips the home
   page; last crumb takes the document title with the "- PSFnetwork"
   suffix stripped. Canonical copy of the snippet is below - edit here
   first, then paste into Framer.

2. **Visible breadcrumb row** on the Articles template, added via the
   Framer Agent (branch merged to main before publishing - the Agent
   works on a branch, and "Update <branch>" publishes only the branch
   preview, not the site; same trap as the banner fix earlier that day).
   Renders: Home (/) / Blog (/blog) / article title as plain text, above
   the category chip.

```html
<script>
(function () {
  var path = location.pathname.replace(/\/$/, '');
  if (!path) return;
  var base = 'https://www.psfnetwork.com';
  var labels = { 'blog': 'Blog', 'how-it-works': 'How It Works',
    'investors': 'Investors', 'agents': 'Agents', 'waitlist': 'Waitlist',
    'legal-pages': 'Legal' };
  var items = [{ '@type': 'ListItem', position: 1, name: 'Home', item: base + '/' }];
  var segs = path.split('/').filter(Boolean), acc = '';
  for (var i = 0; i < segs.length; i++) {
    acc += '/' + segs[i];
    var name = (i === segs.length - 1)
      ? (document.title.replace(/\s*[-|]\s*PSFnetwork\s*$/, '').trim() || segs[i])
      : (labels[segs[i]] || segs[i].replace(/-/g, ' '));
    items.push({ '@type': 'ListItem', position: i + 2, name: name, item: base + acc });
  }
  var el = document.createElement('script');
  el.type = 'application/ld+json';
  el.textContent = JSON.stringify({ '@context': 'https://schema.org',
    '@type': 'BreadcrumbList', itemListElement: items });
  document.head.appendChild(el);
})();
</script>
```
