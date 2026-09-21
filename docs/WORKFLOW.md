# Workflow: from design export to live page

## 1. Add the design export

1. Export the page from the design tool (mobile or desktop).
2. Save it as `design/<breakpoint>/<page>.html`, lowercase with hyphens
   (`index`, `quiz`, `portal`, `alabama`, `contact`).
3. Commit it as-is. Exports are the reference; never edit them.

## 2. Unpack it

Exports are self-contained bundles. Unpack one into editable HTML plus an
`assets/` folder:

```bash
python3 tools/unbundle.py design/mobile/<page>.html /tmp/unpacked/<page>
```

Named assets (from the export's resource map) come out as
`assets/<name>.<ext>`; everything else keeps its UUID filename.

## 3. Convert it into a site page

What the unpacked HTML still contains, and what to do with it:

| In the export | In `site/` |
|---|---|
| Inline `@font-face` blocks with woff2 data | Removed. Pages link `assets/css/fonts.css` (fonts are in `assets/fonts/`). |
| `<x-dc>`, `<helmet>`, `<sc-if>`, `{{ bindings }}`, `<script type="text/x-dc">` and the `dc-runtime` script | Design-tool runtime that loads React from a CDN. Replaced with plain HTML and a small inline `<script>` at the bottom of the page. |
| `<image-slot>` elements and their script | Editor-only placeholders. Removed. |
| Tweaks panel (React, ReactDOM, Babel, `text/babel` scripts) | Editor-only. Removed. Its default values are baked into the page's CSS variables. |
| Logo PNGs (8000px wide, mostly transparent padding) | Replaced by cropped, resized files in `assets/images/`. Because the padding is gone, logo heights and negative margins in the markup were recalculated (header logo: 17px tall). |
| Hero photo (`tort-law-…png`, 3.8 MB) | `assets/images/hero-mobile.jpg` (1080px wide, ~100 KB). |
| Footer `<style>` + markup repeated on every page | Shared `.footer` styles in `assets/css/main.css`. |
| Hamburger `<details>` menu with inline styles | Shared `.menu` styles in `assets/css/main.css`. |
| Google Fonts `preconnect` links | Removed (fonts are self-hosted). |

Keep page-specific CSS in a `<style>` block in the page for now; it mirrors
the export and makes diffing against the next export easy.

## 4. Check it

```bash
cd site && python3 -m http.server 8080
```

Open http://localhost:8080 and check at 390px wide (phone) and, once the
desktop designs are in, 1280px+. Browser dev tools → device toolbar.

Things worth clicking through:

- Home: carousel dots, gauge animations on scroll, hamburger menu.
- Quiz: full flow to the score screen, then "Go to My Case Portal".
- Portal: with a Good/Very Good result the "Your path forward" choices appear.
- Contact: submit with empty fields (validation), then a full submit.

## 5. Commit and push

```bash
git add .
git commit -m "Add <page> page"
git push
```

## Adding the desktop breakpoint (next step)

Upload the desktop exports to `design/desktop/`. The plan is to keep the
mobile markup as the base and add desktop rules under
`@media (min-width: 1024px)`, moving shared rules into `assets/css/main.css`
as they emerge.
