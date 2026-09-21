# Workflow: from design export to live page

This is the repeatable process for every page on the site.

## 1. Add the design files

1. Export the page from the design tool for **mobile** and **desktop**.
2. Save them to `design/mobile/<page>.html` and `design/desktop/<page>.html`.
3. Any images, CSS or fonts that came with the export go in an `assets/`
   folder beside the HTML.
4. Commit them as-is. Do not edit the exports.

## 2. Build the site page

1. Create `site/<page>.html` (the home page is `site/index.html`).
2. Start from the mobile design (mobile-first), then layer the desktop layout
   on top with a media query:

   ```css
   /* mobile styles are the default */

   @media (min-width: 1024px) {
     /* desktop overrides go here */
   }
   ```

3. Move shared styles into `site/assets/css/main.css` and page-specific
   styles into `site/assets/css/<page>.css`.
4. Copy any images into `site/assets/images/` and update the paths.
5. Fonts go in `site/assets/fonts/` (or link them from Google Fonts).

## 3. Check it

```bash
cd site
python3 -m http.server 8080
```

Open http://localhost:8080 and check the page at a phone width (about 375px)
and a desktop width (1280px+). The browser dev tools device toolbar makes
this easy.

## 4. Commit and push

```bash
git add .
git commit -m "Add <page> page"
git push
```

## Branching

- `main` is the deployable site.
- Do day-to-day work on a feature branch and open a pull request into `main`.
